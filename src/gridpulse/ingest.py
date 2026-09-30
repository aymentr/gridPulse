"""Intake: files → Document / immutable DocumentVersion (one universal intake path).

The benchmark-isolation guard refuses ground truth, investigation bundles and pack metadata, so
production code can never read expected answers.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .dates import parse_date
from .model import Document, DocumentVersion
from .store import Store


class BenchmarkIsolationError(Exception):
    pass


FORBIDDEN_NAMES = {"README.md", "SOURCES.md", "investigation-bundle.md", "GROUND_TRUTH.md"}
FORBIDDEN_PARTS = {"ground-truth", "scoring", "technical-realism-review", "route-b-recruitment"}
SOURCE_FOLDERS = ("baseline", "changed", "supporting", "schedule", "progress-report")

_DOCNO_ROW = re.compile(
    r"^\|\s*(Document no\.|Ref|Transmittal no\.|Purchase order)\s*\|\s*(?P<v>[^|]+?)\s*\|", re.M)
_DOCNO_CSV = re.compile(r"Document no\.:\s*(?P<v>[A-Z0-9-]+)")
_DATE_ROW = re.compile(r"^\|\s*(Issued|Date)\s*\|\s*(?P<v>[^|]+?)\s*\|", re.M)
_DATA_DATE = re.compile(r"[Dd]ata date:?\s*(?P<v>[0-9A-Za-z -]+?\d{2,4})")
_REV = re.compile(r"^(?P<id>.+?)\s+(?P<rev>(Rev|Issue)\s+\S+)$")
_SERIES = re.compile(r"^(?P<series>.+)-(U?\d+)$")


def check_isolation(path: Path) -> None:
    if path.name in FORBIDDEN_NAMES or FORBIDDEN_PARTS & set(path.parts):
        raise BenchmarkIsolationError(f"refusing to ingest benchmark-internal file: {path}")


def _identity(text: str, path: Path) -> tuple[str, str]:
    m = _DOCNO_ROW.search(text) or _DOCNO_CSV.search(text)
    raw = m.group("v").strip() if m else path.stem
    r = _REV.match(raw)
    return (r.group("id"), r.group("rev")) if r else (raw, "")


def _source_date(text: str):
    m = _DATE_ROW.search(text) or _DATA_DATE.search(text)
    return parse_date(m.group("v")) if m else None


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def ingest_file(store: Store, path: Path) -> DocumentVersion:
    path = Path(path)
    check_isolation(path)
    text = path.read_text(encoding="utf-8")
    doc_id, rev = _identity(text, path)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    if doc_id not in store.documents:
        s = _SERIES.match(doc_id)
        store.documents[doc_id] = Document(doc_id, s.group("series") if s else doc_id,
                                           _title(text, doc_id))
    for existing in store.versions[doc_id]:
        if existing.content_hash == digest:
            return existing                       # idempotent re-ingestion

    version = DocumentVersion(
        doc_id=doc_id, version_no=len(store.versions[doc_id]) + 1, revision_label=rev,
        source_path=str(path), source_date=_source_date(text), ingested_at=store.clock(),
        content_hash=digest, lines=tuple(text.splitlines()))
    store.versions[doc_id].append(version)
    store.versions[doc_id].sort(key=lambda v: (v.source_date is None, v.source_date, v.version_no))
    store.log("document.ingested", doc=doc_id, version=version.version_no, revision=rev,
              path=str(path), sha256=digest)
    return version


def scenario_files(scenario_dir: Path, folders=SOURCE_FOLDERS) -> list[Path]:
    """Source documents of a scenario directory; never ground truth or pack metadata."""
    files = []
    for folder in folders:
        d = Path(scenario_dir) / folder
        if d.is_dir():
            files += sorted(p for p in d.iterdir()
                            if p.is_file() and p.name not in FORBIDDEN_NAMES)
    return files


def ingest_paths(store: Store, paths) -> list[DocumentVersion]:
    return [ingest_file(store, Path(p)) for p in paths]

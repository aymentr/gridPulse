"""Versioned prompt templates (architecture: AI boundary; milestone §10).

Templates live as `<name>_v<N>.md` files beside this module. Each AI proposal and each AI-invocation
trace records the template name and version, so a proposal can always be tied to the exact prompt
that produced it. Prompts are never scattered through application code.
"""
from __future__ import annotations

from pathlib import Path

_DIR = Path(__file__).resolve().parent


def get_prompt(name: str) -> tuple[str, str]:
    """Return (text, version) for the highest version of a named template, e.g. ('...', 'v1')."""
    candidates = sorted(_DIR.glob(f"{name}_v*.md"))
    if not candidates:
        raise KeyError(f"no prompt template named {name!r}")
    path = candidates[-1]
    return path.read_text(), path.stem.rsplit("_", 1)[-1]


def prompt_version(name: str) -> str:
    return get_prompt(name)[1]

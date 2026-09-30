"""CLI: `python -m gridpulse run <scenario-dir> [--standard-a] [--json FILE]`."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run

STANDARD_A = ("baseline", "supporting", "schedule", "progress-report")   # excludes variant letter


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gridpulse")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="ingest a scenario directory and produce investigations")
    r.add_argument("scenario_dir")
    r.add_argument("--standard-a", action="store_true",
                   help="Scenario A standard run (exclude the changed/ supplier-letter variant)")
    r.add_argument("--json", help="write bundles and review queue as JSON to this file")
    args = ap.parse_args(argv)

    res = run(Path(args.scenario_dir), folders=STANDARD_A if args.standard_a else None)
    s = res.store
    print(f"# GridPulse spike run — {args.scenario_dir}\n")
    print(f"Documents: {len(s.documents)} · claims: {len(s.claims)} · dependencies: "
          f"{len(s.dependencies)} · evidence verified: "
          f"{sum(e.verified for e in s.evidence.values())}/{len(s.evidence)}\n")
    print("Inference proposer: heuristic stand-in (not an AI model) — see SPIKE.md.\n")
    for b in res.bundles:
        print(b.to_markdown())
    print("## Review queue\n")
    for f in res.queue.pending():
        print(f"- {f.id} [{f.kind.value} · {f.status.value}] {f.summary}")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"bundles": [b.to_dict() for b in res.bundles],
             "review_queue": [res.queue.describe(f.id) for f in res.queue.pending()],
             "audit_events": len(s.audit)}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

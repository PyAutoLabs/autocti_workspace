"""
Run the workspace smoke test suite: the scripts listed in `smoke_tests.txt`.

Nothing about discovery, exclusion, environment resolution, per-script timeouts
or reporting is implemented here. This is a thin shim over PyAutoHands'
`autohands/run_python.py` — the same entry point PyAutoHeart's
workspace-validation uses — so the PR gate and the validation runner cannot
drift apart.

It is deliberately a shim and not a copy. The sibling repos each carried a
198-line copy of that machinery, and every fix to it — the env-resolver fork
(PyAutoHands#185), the per-script timeout and process-group kill
(PyAutoHands#226/#227), the jupyter guard — had to be swept across all of them
by hand. This file holds no logic, so it needs none of those sweeps. It mirrors
`autocti_workspace_test/.github/scripts/run_smoke.py`; keep the two in step.

What the shared runner provides:

  * the allowlist in `smoke_tests.txt`, run in that file's own order
  * per-script env from `config/build/profile_smoke.yaml`, via the one resolver
  * the `BUILD_SCRIPT_TIMEOUT` cap and the process-group kill on expiry
  * a structured JSON report, and a non-zero exit when anything failed

`--report-dir` is REQUIRED, not cosmetic. run_python.py only propagates failures
(`sys.exit(1)`) when a report was built; without it the suite runs to completion
and always exits 0 — a vacuously green gate.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
PROJECT = "autocti_workspace"

# CI puts PyAutoHands/autohands on PYTHONPATH (PyAutoHeart's reusable
# smoke-tests.yml clones it alongside the dependency chain); for local runs,
# fall back to the sibling checkout.
try:
    import build_util
except ImportError:  # pragma: no cover - local-run fallback
    sys.path.insert(0, str(WORKSPACE.parent / "PyAutoHands" / "autohands"))
    import build_util

AUTOHANDS = Path(build_util.__file__).resolve().parent


def main() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (str(AUTOHANDS), env.get("PYTHONPATH", "")) if p
    )

    cmd = [
        sys.executable,
        str(AUTOHANDS / "run_python.py"),
        PROJECT,
        "scripts",
        "--list",
        str(WORKSPACE / "smoke_tests.txt"),
        "--report-dir",
        str(WORKSPACE / "test-results"),
    ]
    # run_python.py resolves config/build/ relative to the cwd.
    return subprocess.run(cmd, cwd=str(WORKSPACE), env=env).returncode


if __name__ == "__main__":
    sys.exit(main())

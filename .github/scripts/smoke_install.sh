#!/usr/bin/env bash
# Workspace-owned install epilogue for the reusable Smoke Tests workflow
# (PyAutoHeart/.github/workflows/smoke-tests.yml). Runs with cwd at the
# checkout root (the dependency chain is cloned beside `workspace/`).
set -e

# arcticpy is NOT installed here. It is a hard import of autocti but not a pip
# dependency, and its recipe (source-only C++ sdist, libgsl-dev, a
# numpy-downgrade trap, --no-build-isolation build deps) belongs to the organ
# that owns the reusable workflows:
#
#   PyAutoHeart/.github/actions/install-arcticpy
#
# This workspace asks for it with `arcticpy: true` in
# .github/workflows/smoke_tests.yml, which runs it before this epilogue.

pip install ./PyAutoNerves ./PyAutoFit ./PyAutoArray ./PyAutoCTI
pip install "./PyAutoArray[optional]"
# The re-resolution above can upgrade autonerves to the stale PyPI release;
# pin the local source last so recent autonerves APIs are importable.
pip install --force-reinstall --no-deps ./PyAutoNerves

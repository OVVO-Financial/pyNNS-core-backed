# Parity plan

This plan tracks the public R NNS behavior that must remain covered before any
future NNS-python migration. The migration itself is out of scope for this
repository branch: the package continues to expose `pynns`, and no files from
NNS-python are edited here.

## Ground rules

- Treat the installed R `NNS` package as the parity oracle where behavior is
  stable, documented, and useful.
- Keep R invocation isolated to the test harness in `tests/_r.py` and committed
  offline cache data in `tests/_r_cache.json`.
- Prefer semantic assertions over internal algorithm matching.
- Preserve the native extension as an optional acceleration path only; every
  public wrapper covered by native tests must continue to match the pure Python
  fallback.
- Do not reintroduce stale native expectations. The canonical direct native LPM
  check for `[-2.0, -1.0, 0.5, 3.0]`, degree `2.0`, and target `0.0` is `1.25`.
- Import implementation modules with `importlib.import_module(...)` in tests
  that monkeypatch module internals, so a public function export named like a
  module cannot shadow the actual module object.

## Coverage layers

1. **Parity tests** (`tests/parity/`): compare public Python behavior against R
   NNS outputs, using the committed cache when Rscript is unavailable.
2. **Invariants** (`tests/invariants/`): enforce Python-native mathematical,
   shape, guard, and API contracts, including optional native-backend behavior.
3. **Property tests** (`tests/property/`): exercise general laws and generated
   examples that should hold independently from one exact fixture.
4. **Benchmark tests** (`tests/benchmarks/`): keep performance-sensitive public
   workflows measurable without making benchmarks part of the default test run.
5. **Native-vs-fallback tests**: require optional native paths to match the pure
   Python fallback rather than stale hand-written constants, especially for ratio
   helpers.

## Suite completion checklist

- [x] Core partial moments and ratio parity, including scalar and vector targets.
- [x] Co-moment and PM matrix parity fixtures.
- [x] Public-wrapper parity coverage for implemented modules.
- [x] Practical workflow parity coverage for regression, distance, stack, boost,
      stochastic dominance, and related public examples.
- [x] Offline cache support for CI and local environments without Rscript.
- [x] Optional native backend coverage against direct bindings and public
      fallback behavior.
- [x] Parity CI that runs invariant and parity suites in cache-only mode before
      linting, typing, and distribution builds.

## Regeneration workflow

Use the optional cache regeneration script only when intentionally refreshing R
fixtures from an environment with Rscript and the R `NNS` package installed:

```bash
python scripts/regenerate_r_cache.py --tests tests/parity
```

The script runs pytest with R calls enabled by default. Passing `--offline`
checks that the committed cache is complete without trying to refresh it.
Review any changes to `tests/_r_cache.json` before committing.

# evals

A minimal harness for learning [`pydantic-evals`](https://ai.pydantic.dev/evals/). It
demonstrates the three moving parts of an eval — dataset, task function, evaluators —
wired together end to end, with no framing beyond that.

## Core concept

A `pydantic-evals` run has three pieces:

1. **Dataset** — a list of `Case`s. Each case has `inputs` (what gets passed to the
   task function) and `expected_output` (what the evaluators grade against).
2. **Task function** — the thing under test. It receives a case's `inputs` and returns
   a value.
3. **Evaluators** — graders. Each evaluator receives an `EvaluatorContext` with
   `ctx.output` (the task function's return value) and `ctx.expected_output` (from the
   case), and returns a score.

`dataset.evaluate_sync(task_fn)` wires these together: for every `Case` in the dataset,
it calls `task_fn(case.inputs)`, captures the return value as `ctx.output`, and runs
every attached evaluator against `(ctx.output, case.expected_output)`. The result is a
`report` you can print as a table.

## Layout

- `src/evals/simple_eval_dataset.py` — the dataset: one `Case` ('what is the capital
  of denmark' -> 'copenhagen') wrapped in a `Dataset`.
- `src/evals/simple_agent.py` — the task function, `guess_city`. Shells out to the
  `claude` CLI (`claude -p <question>`) rather than calling an API directly.
- `src/evals/simple_eval_evaluator.py` — attaches two evaluators to the dataset
  (`IsInstance(type_name='str')` and a custom `MyEvaluator`), then runs
  `dataset.evaluate_sync(guess_city)` and prints the report.

## Evaluators

- `IsInstance(type_name='str')` — checks the task function returned a `str`.
- `MyEvaluator` — compares `ctx.output` to `ctx.expected_output`:
  - `1.0` on exact match
  - `0.8` if `expected_output` is a case-insensitive substring of `output`
  - `0.0` otherwise

## Running it

```
uv run python -m evals.simple_eval_evaluator
```

Requirements:

- Python >= 3.14
- [`uv`](https://docs.astral.sh/uv/)
- the `claude` CLI on `PATH` — `simple_agent.py` shells out to `claude -p`, not an
  API key, so the CLI must be installed and authenticated

Each case spawns a fresh `claude -p` subprocess, which costs a full CLI boot
(roughly 5-15s). That's fine for the single case here but means this harness does not
scale to large datasets as written.

## Known rough edge

`simple_eval_evaluator.py` calls `dataset.evaluate_sync(...)` at module top level.
Importing the module (rather than running it as `__main__`) triggers the full eval as
a side effect. Not yet guarded with `if __name__ == '__main__':`.

## License

MIT — see [LICENSE](LICENSE).

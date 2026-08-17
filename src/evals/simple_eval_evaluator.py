from dataclasses import dataclass
from typing import override

from pydantic_evals.evaluators import Evaluator, EvaluatorContext, IsInstance

from evals.simple_agent import guess_city
from evals.simple_eval_dataset import dataset

dataset.add_evaluator(IsInstance(type_name='str'))

@dataclass
class MyEvaluator(Evaluator):
    @override
    async def evaluate(self, ctx: EvaluatorContext[str, str]) -> float:
        if ctx.output == ctx.expected_output:
            return 1.0
        elif (
           ctx.expected_output is not None and ctx.expected_output.lower() in ctx.output.lower()):
                return 0.8
        else:
            return 0.0


dataset.add_evaluator(MyEvaluator())

report = dataset.evaluate_sync(guess_city)
report.print(include_input=True, include_output=True)
from pydantic_evals import Case, Dataset

case1 = Case(
    name='simple_case',
    inputs='what is the capital of denmark',
    expected_output='copenhagen',
    metadata={'difficulty': 'easy'},
)

dataset = Dataset(name='capital_quiz', cases=[case1])

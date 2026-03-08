import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from ragas import EvaluationDataset, evaluate
from ragas.metrics import Faithfulness, FactualCorrectness, LLMContextRecall
from ragas.llms import llm_factory
from openai import OpenAI


def load_results(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def to_ragas_rows(results):
    rows = []
    for row in results:
        rows.append(
            {
                "user_input": row["question"],
                "response": row["answer"],
                "reference": row["ground_truth"],
                # Za sada koristimo ground truth kao retrieved_contexts placeholder
                # da dobijemo prvi automatizirani scoring run.
                "retrieved_contexts": [row["ground_truth"]],
            }
        )
    return rows


def run_eval(results_path: str, label: str):
    rows = to_ragas_rows(load_results(results_path))
    dataset = EvaluationDataset.from_list(rows)

    evaluator_llm = llm_factory(
        "gpt-4o-mini",
        client=OpenAI()
    )

    result = evaluate(
        dataset=dataset,
        metrics=[
            LLMContextRecall(),
            Faithfulness(),
            FactualCorrectness(),
        ],
        llm=evaluator_llm,
    )

    df = result.to_pandas()
    out_csv = f"ragas_scores_{label}.csv"
    df.to_csv(out_csv, index=False)

    print(f"\nSaved: {out_csv}")
    print(df.mean(numeric_only=True))


if __name__ == "__main__":
    run_eval("eval_results_fireworks.json", "fireworks")
    run_eval("eval_results_openai.json", "openai")
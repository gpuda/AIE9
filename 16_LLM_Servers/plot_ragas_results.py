import pandas as pd
import matplotlib.pyplot as plt

fw = pd.read_csv("ragas_scores_fireworks.csv")
oa = pd.read_csv("ragas_scores_openai.csv")

fw_mean = fw.mean(numeric_only=True)
oa_mean = oa.mean(numeric_only=True)

metrics = fw_mean.index

fw_scores = fw_mean.values
oa_scores = oa_mean.values

x = range(len(metrics))

plt.figure(figsize=(8,5))

plt.bar(x, fw_scores, width=0.4, label="Fireworks", align="center")
plt.bar([i + 0.4 for i in x], oa_scores, width=0.4, label="OpenAI")

plt.xticks([i + 0.2 for i in x], metrics, rotation=20)
plt.ylabel("Score")
plt.title("RAGAS Evaluation Comparison")
plt.legend()

plt.tight_layout()
plt.savefig("ragas_comparison.png")

print("Saved: ragas_comparison.png")
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from doe.bounds import INPUT_BOUNDS
from scipy.stats import qmc
import pandas as pd

def generate_lhs(n_samples: int, seed: int = 42):
	names = list(INPUT_BOUNDS.keys())
	lower = [INPUT_BOUNDS[name][0] for name in names]
	upper = [INPUT_BOUNDS[name][1] for name in names]
	sampler = qmc.LatinHypercube(d=len(names), seed=seed)
	samples = sampler.random(n=n_samples)
	samples = qmc.scale(samples, lower, upper)
	return pd.DataFrame(samples, columns=names).round(2)

if __name__ == "__main__":
	output_path = PROJECT_ROOT / "doe" / "lhs_samples.csv"
	df = generate_lhs(n_samples=250, seed=42)
	df.insert(0, "Sample_ID", range(1, len(df) + 1))
	print(df.duplicated().sum())
	df.to_csv(output_path, index=False)
	
	print(f"Saved {len(df)} samples to {output_path}")
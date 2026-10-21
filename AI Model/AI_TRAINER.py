
import pandas as pd

df = pd.read_csv("Dsa_Video.csv")

print("Total rows:", len(df))
print("Columns:", df.columns.tolist())

for col in ["transcript", "tags", "label_verified"]:
    if col in df.columns:
        print(f"\n{col}:")
        print("Non-empty:", df[col].notna().sum())
        print(df[col].value_counts(dropna=False).head(10))
    else:
        print(f"\nMISSING COLUMN: {col}")

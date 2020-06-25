import pandas as pd

df = pd.read_csv('summary.csv')

summary = df[df['model'].str.contains('Qtime=0-150') & df['model'].str.contains('MultFQ4')].describe()

for col in summary.columns:
    print(col)
    print(summary[col])

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import numpy as np

#Connect to DuckDB
con = duckdb.connect('ELT_pipe/elt_data.duckdb')
query = "SELECT * FROM market_trends"
df = con.execute(query).df()

#Ensure sale_date is a datetime object so the x-axis spaces chronologically
df['sale_date'] = pd.to_datetime(df['sale_date'])


# Sort data so the red 'Outlier' dots are plotted visibly on top
df = df.sort_values(by='risk_category')

#Create the Scatterplot
plt.figure(figsize=(12, 6))
colors = {'NORMAL': 'tab:blue', 'ANOMALY': 'red'}

sns.scatterplot(
    data=df, 
    x='sale_date', 
    y='z_score', 
    hue='risk_category', 
    palette=colors,
    alpha=0.6,
    edgecolor=None
)

plt.axhline(y=3, color='red', linestyle='--', alpha=0.5)
plt.axhline(y=-3, color='red', linestyle='--', alpha=0.5)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

plt.title('Normalized Risk Profile: Rolling Z-Scores by Sale Date', fontsize=14, fontweight='bold')
plt.xlabel('Sale Date', fontsize=12)
plt.ylabel('Z-Score (Standard Deviations from Local Mean)', fontsize=12)

plt.legend(title='Data Point Classification', loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("ELT_pipe/analyses/Anomalies.png")
plt.show()
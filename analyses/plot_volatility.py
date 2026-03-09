#plotting rolling volatility
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import duckdb
import pandas as pd

# Connect to the database
con = duckdb.connect('ELT_pipe/elt_data.duckdb')

# Query the final table created by your dbt model
query = "select * from suburb_rolling_volatility"
df = con.execute(query).df()

#plot the volatilitty
plt.figure(figsize=(12,8))
ax = sns.lineplot(x='sale_month',
             y='rolling_3m_volatility',
             data=df,
             hue='suburb',
             marker='o'               
            )

#format the axis labels
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

plt.title('3-month rolling price volatility by suburb')
plt.xlabel('Sale Month')
plt.ylabel('Rolling volatility')
plt.legend(title='Suburb', loc = 'upper left')
plt.tight_layout()

plt.savefig("ELT_pipe/analyses/Volatility.png")
plt.show()

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Settings
np.random.seed(42)
n_rows = 50000
suburbs = ['Ponsonby', 'Grey Lynn', 'Remuera', 'Epsom', 'Mount Eden', 'Albany', 'Manukau']

data = []

for _ in range(n_rows):
    suburb = np.random.choice(suburbs)
    # Random date within the last 5 years
    days_ago = np.random.randint(0, 365 * 5)
    date = datetime(2026, 2, 16) - timedelta(days=days_ago)
    
    # Base price logic + some "market growth" trend
    base_price = {'Ponsonby': 1500000, 'Remuera': 1800000, 'Albany': 900000}.get(suburb, 1100000)
    growth = (days_ago / 365) * 50000  # Price was lower in the past
    noise = np.random.normal(0, 100000) # Market volatility
    
    # Add occasional "outliers"
    if np.random.random() > 0.99:
        price = base_price * 2.5
    else:
        price = base_price - growth + noise
        
    data.append([suburb, date.strftime('%Y-%m-%d'), round(price, 2)])

df = pd.DataFrame(data, columns=['suburb', 'sale_date', 'price'])
df.to_csv('raw_sales.csv', index=False)
print(f"Generated {n_rows} rows in data/raw_sales.csv")
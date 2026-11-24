import os  #Creates folders and manages files.
import pandas as pd 	#Loads, cleans, and analyzes data.
import matplotlib.pyplot as plt 	#Creates graphs and charts.
from matplotlib.ticker import FuncFormatter    #Formats numbers on charts, such as 3500000 into $3.5M.

os.makedirs("Output", exist_ok = True)
df = pd.read_csv("sales_data_sample.csv", encoding="latin1")

print(df.head())

print(df.tail())

print(df.info())

print(df.shape)

df = df.drop_duplicates()

for col in ["SALES", "QUANTITYORDERED"]:
    df[col] = pd.to_numeric(df[col], errors = "coerce")
    df.loc[df[col] < 0, col] = None
    df[col] = df[col].fillna(df[col].median())

df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors ="coerce")
df["PRODUCTLINE"] = df["PRODUCTLINE"].fillna(df["PRODUCTLINE"].mode()[0])

df = df.drop(columns=["unnamed: 0"], errors ="ignore")
df.to_csv("Output/cleaned_sales_data.csv", index=False)

money = FuncFormatter(lambda x, _: f"${x/1e6:.1f}M")
color = "#122B39"

product_sales = df.groupby("PRODUCTLINE")["SALES"].sum().sort_values(ascending=False)

product_sales.plot(kind="bar", color=color, figsize=(10, 5))
plt.title("Sales by Product Line")
plt.ylabel("Revenue")
plt.gca().yaxis.set_major_formatter(money)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/1_sales_by_product_line.png")
plt.close()

monthly = df.groupby(df["ORDERDATE"].dt.to_period("M"))["SALES"].sum()

monthly.index = monthly.index.to_timestamp()

plt.figure(figsize=(10, 5))
plt.plot(monthly.index, monthly.values, marker="o", color=color)
plt.title("Monthly Sales Trend")
plt.ylabel("Revenue")
plt.gca().yaxis.set_major_formatter(money)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("output/2_monthly_sales_trend.png")
plt.close()

countries = df.groupby("COUNTRY")["SALES"].sum().nlargest(10).sort_values()

countries.plot(kind="barh", color=color, figsize=(10, 5))
plt.title("Top 10 Countries by Sales")
plt.xlabel("Revenue")
plt.gca().xaxis.set_major_formatter(money)
plt.tight_layout()
plt.savefig("output/3_top_10_countries.png")
plt.close()

total = df["SALES"].sum()

print("Total Revenue:", round(total, 2))
print("Top Product:", product_sales.idxmax())
print("Top Country:", countries.idxmax())
print("Best Month:", monthly.idxmax())
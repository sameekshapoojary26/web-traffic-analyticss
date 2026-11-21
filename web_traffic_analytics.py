import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Generate synthetic website traffic data (900 visits)
n = 900
sources = np.random.choice(
    ["Organic", "Ads", "Social", "Direct"],
    n, p=[0.35, 0.25, 0.20, 0.20]
)

pages = np.random.choice(
    ["Home", "Products", "Pricing", "Checkout"],
    n, p=[0.35, 0.30, 0.20, 0.15]
)

data = pd.DataFrame({
    "Source": sources,
    "Page": pages,
    "Duration": np.random.randint(10, 600, n),
    "Pageviews": np.random.randint(1, 8, n),
    "Registered": np.random.choice([0, 1], n, p=[0.75, 0.25])
})

# Calculate metrics
bounce_rate = (data["Pageviews"] == 1).mean() * 100
avg_duration = data["Duration"].mean()
avg_pageviews = data["Pageviews"].mean()
conversion_rate = data["Registered"].mean() * 100

source_analysis = data.groupby("Source").agg(
    Visits=("Source", "count"),
    Conversions=("Registered", "sum"),
    Avg_Duration=("Duration", "mean")
)

source_analysis["Conversion_Rate"] = (
    source_analysis["Conversions"] / source_analysis["Visits"] * 100
)

dropoff = data.groupby("Page")["Registered"].apply(
    lambda x: (1 - x.mean()) * 100
)

print("WEB TRAFFIC ANALYTICS")
print("-------------------")
print(f"Total Visits: {n}")
print(f"Bounce Rate: {bounce_rate:.2f}%")
print(f"Average Session Duration: {avg_duration:.2f} seconds")
print(f"Average Pageviews per Visit: {avg_pageviews:.2f}")
print(f"Conversion Rate: {conversion_rate:.2f}%")

print("\nTraffic Source Analysis:")
print(source_analysis.round(2))

print("\nPage Drop-off Analysis:")
print(dropoff.round(2))

# Create dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

source_analysis["Visits"].plot(
    kind="bar", ax=axes[0, 0], title="Visits by Traffic Source"
)

source_analysis["Conversion_Rate"].plot(
    kind="bar", ax=axes[0, 1], title="Conversion Rate by Source"
)

data.groupby("Page")["Duration"].mean().plot(
    kind="bar", ax=axes[1, 0], title="Average Duration by Page"
)

dropoff.plot(
    kind="bar", ax=axes[1, 1], title="Page Drop-off Rate"
)

plt.tight_layout()
plt.savefig("web_traffic_dashboard.png", dpi=300)

# Export data and report
data.to_csv("web_traffic_data.csv", index=False)
source_analysis.to_csv("traffic_source_analysis.csv")

with open("web_traffic_report.txt", "w") as f:
    f.write("WEB TRAFFIC ANALYTICS REPORT\n")
    f.write(f"Total Visits: {n}\n")
    f.write(f"Bounce Rate: {bounce_rate:.2f}%\n")
    f.write(f"Average Session Duration: {avg_duration:.2f} seconds\n")
    f.write(f"Average Pageviews: {avg_pageviews:.2f}\n")
    f.write(f"Conversion Rate: {conversion_rate:.2f}%\n")
    f.write("\nTraffic Source Analysis:\n")
    f.write(source_analysis.round(2).to_string())
    f.write("\n\nPage Drop-off Analysis:\n")
    f.write(dropoff.round(2).to_string())

plt.show()

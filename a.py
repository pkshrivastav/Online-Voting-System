import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load JSON data from a file
with open("data.json", "r") as file:
    data = json.load(file)

users = data["users"]
df = pd.DataFrame(users)

# Convert data types
df["age"] = df["age"].astype(int)
df["has_voted"] = df["has_voted"].astype(bool)

# Pie Chart - Voting Participation
plt.figure(figsize=(6, 6))
df["has_voted"].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'red'], labels=["Voted", "Not Voted"], startangle=90)
plt.title("Voting Participation")
plt.show()

# Bar Chart - Voting Status
plt.figure(figsize=(6, 4))
sns.countplot(x="has_voted", data=df, palette=['green', 'red'])
plt.xlabel("Voting Status")
plt.ylabel("Count")
plt.title("Voter Participation Bar Chart")
plt.show()

# Histogram - Age Distribution
plt.figure(figsize=(6, 4))
sns.histplot(df["age"], bins=5, kde=True, color='blue')
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title("Age Distribution")
plt.show()

# Box Plot - Age Distribution
plt.figure(figsize=(6, 4))
sns.boxplot(x=df["age"], color='cyan')
plt.title("Age Distribution Box Plot")
plt.show()

# Count Plot - Candidate Choice
plt.figure(figsize=(6, 4))
sns.countplot(y="candidate", data=df, palette='coolwarm')
plt.xlabel("Count")
plt.ylabel("Candidate")
plt.title("Candidate Preference Count")
plt.show()

# Violin Plot - Age vs Voting Status
plt.figure(figsize=(6, 4))
sns.violinplot(x="has_voted", y="age", data=df, palette=['green', 'red'])
plt.xlabel("Voting Status")
plt.ylabel("Age")
plt.title("Age vs Voting Status Violin Plot")
plt.show()

# Heatmap - Correlation Matrix
plt.figure(figsize=(6, 4))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

# KDE Plot - Age Distribution by Voting Status
plt.figure(figsize=(6, 4))
sns.kdeplot(df[df["has_voted"] == True]["age"], label="Voted", shade=True, color='green')
sns.kdeplot(df[df["has_voted"] == False]["age"], label="Not Voted", shade=True, color='red')
plt.xlabel("Age")
plt.ylabel("Density")
plt.title("Age Distribution by Voting Status")
plt.legend()
plt.show()

# Pair Plot - Numerical Data
sns.pairplot(df, hue="has_voted", palette=['green', 'red'])
plt.show()

# Candidate Distribution Plot
plt.figure(figsize=(6, 4))
sns.histplot(df["candidate"], color='purple', kde=True)
plt.xlabel("Candidate")
plt.ylabel("Frequency")
plt.title("Candidate Distribution")
plt.xticks(rotation=45)
plt.show()

# State-wise Voting Plot
plt.figure(figsize=(6, 4))
sns.countplot(y="state", data=df, hue="has_voted", palette=['red', 'green'])
plt.xlabel("Count")
plt.ylabel("State")
plt.title("State-wise Voting Participation")
plt.show()

# Gender-wise Voting Plot
plt.figure(figsize=(6, 4))
sns.countplot(x="sex", data=df, hue="has_voted", palette=['red', 'green'])
plt.xlabel("Gender")
plt.ylabel("Count")
plt.title("Gender-wise Voting Participation")
plt.show()

# Swarm Plot - Age vs Candidate
plt.figure(figsize=(6, 4))
sns.swarmplot(x="candidate", y="age", data=df, palette='coolwarm')
plt.xlabel("Candidate")
plt.ylabel("Age")
plt.title("Age Distribution Across Candidates")
plt.xticks(rotation=45)
plt.show()

# Joint Plot - Age vs Voting Status
sns.jointplot(x="age", y="has_voted", data=df, kind="kde", fill=True, cmap="coolwarm")
plt.show()

# Boxen Plot - Age vs State
plt.figure(figsize=(6, 4))
sns.boxenplot(x="state", y="age", data=df, palette='coolwarm')
plt.xlabel("State")
plt.ylabel("Age")
plt.title("Age Distribution Across States")
plt.xticks(rotation=45)
plt.show()

# Count Plot - Age Grouping
plt.figure(figsize=(6, 4))
df["age_group"] = pd.cut(df["age"], bins=[18, 25, 35, 50, 70], labels=["18-25", "26-35", "36-50", "51+"])
sns.countplot(x="age_group", data=df, hue="has_voted", palette=['red', 'green'])
plt.xlabel("Age Group")
plt.ylabel("Count")
plt.title("Age Group vs Voting Status")
plt.show()

# Print summary
print(f"Total Users: {len(users)}")
print(f"Users Voted: {df['has_voted'].sum()}")
print(f"Users Not Voted: {(~df['has_voted']).sum()}")
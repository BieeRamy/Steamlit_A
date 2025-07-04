import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("customer_data_with_clusters.csv")

df = load_data()

st.title("Customer Segmentation & Churn Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

cluster_options = sorted(df['cluster'].unique())
selected_cluster = st.sidebar.multiselect("Select Cluster(s)", cluster_options, default=cluster_options)

age_min, age_max = int(df['age'].min()), int(df['age'].max())
selected_age = st.sidebar.slider("Select Age Range", age_min, age_max, (age_min, age_max))

salary_min, salary_max = int(df['estimated_salary'].min()), int(df['estimated_salary'].max())
selected_salary = st.sidebar.slider("Select Estimated Salary Range", salary_min, salary_max, (salary_min, salary_max))

# Filter dataframe based on user input
filtered_df = df[
    (df['cluster'].isin(selected_cluster)) &
    (df['age'] >= selected_age[0]) & (df['age'] <= selected_age[1]) &
    (df['estimated_salary'] >= selected_salary[0]) & (df['estimated_salary'] <= selected_salary[1])
]

st.write(f"### Showing {filtered_df.shape[0]} customers")

# Show basic stats
st.write(filtered_df.describe())

# Churn distribution plot
fig, ax = plt.subplots()
sns.countplot(x='churn', data=filtered_df, ax=ax)
ax.set_title("Churn Distribution")
st.pyplot(fig)

# Cluster churn rate
cluster_churn = filtered_df.groupby('cluster')['churn'].mean().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(data=cluster_churn, x='cluster', y='churn', ax=ax2)
ax2.set_title("Churn Rate by Cluster")
ax2.set_ylim(0, 1)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
st.pyplot(fig2)

# Show filtered data table (optional)
if st.checkbox("Show data table"):
    st.dataframe(filtered_df)
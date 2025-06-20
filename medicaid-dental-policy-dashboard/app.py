
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Medicaid Dental Policy Dashboard", layout="wide")
st.title("💰 Medicaid Dental Reimbursement Dashboard (Simulated Data)")
st.markdown("This dashboard simulates CMS dental reimbursement rates across U.S. states and procedure types for policy analysis and advocacy.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/synthetic_medicaid_dental_fees.csv")

df = load_data()

# Sidebar filters
states = st.sidebar.multiselect("Select States", df["State"].unique(), default=df["State"].unique())
categories = st.sidebar.multiselect("Select Categories", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[df["State"].isin(states) & df["Category"].isin(categories)]

# Bar chart: Reimbursement by category and state
st.subheader("📊 Average Reimbursement by Category and State")
chart_data = filtered_df.groupby(["State", "Category"])["ReimbursementRate"].mean().reset_index()
chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X("Category:N", title="Procedure Category"),
    y=alt.Y("ReimbursementRate:Q", title="Avg. Reimbursement ($)", scale=alt.Scale(domain=[0, 300])),
    color="Category:N",
    column="State:N"
).properties(height=300).interactive()
st.altair_chart(chart, use_container_width=True)

# Table: Utilization vs. Reimbursement
st.subheader("📄 Top Procedures by Utilization")
util_table = filtered_df.sort_values(by="AnnualUtilization", ascending=False).head(10)
st.dataframe(util_table)

st.markdown("**Disclaimer:** This is simulated data for demonstration purposes based on publicly available CMS methodology.")

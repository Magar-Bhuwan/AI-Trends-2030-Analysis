import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="AI Job Trends Dashboard (2024-2030)", layout="wide")

@st.cache_data
def load_data():
    candidates = ["ai_job_trends_dataset(2024-2030).csv", "ai_job_trends_dataset(2024-230).csv"]
    path = next((c for c in candidates if os.path.exists(c)), candidates[0])
    return pd.read_csv(path)

st.title("AI Job Trends Dashboard (2024-2030)")
st.caption("Interactive exploration of AI impact, automation risk, and workforce projections.")

data = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")
industries = st.sidebar.multiselect("Industry", sorted(data["Industry"].unique()), default=list(data["Industry"].unique()))
countries = st.sidebar.multiselect("Location", sorted(data["Location"].unique()), default=list(data["Location"].unique()))
impact_levels = st.sidebar.multiselect("AI Impact Level", ["Low", "Moderate", "High"], default=["Low", "Moderate", "High"])

filtered = data[
    data["Industry"].isin(industries)
    & data["Location"].isin(countries)
    & data["AI Impact Level"].isin(impact_levels)
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Records", f"{len(filtered):,}")
col2.metric("Avg Salary", f"${filtered['Median Salary (USD)'].mean():,.0f}")
col3.metric("Avg Automation Risk", f"{filtered['Automation Risk (%)'].mean():.1f}%")
col4.metric("Job Openings 2024 -> 2030", f"{filtered['Job Openings (2024)'].sum():,} -> {filtered['Projected Openings (2030)'].sum():,}")

tab1, tab2, tab3, tab4 = st.tabs(["AI Impact", "Automation Risk", "Industry Trends", "Future Projections"])

with tab1:
    fig = px.histogram(filtered, x="Industry", color="AI Impact Level", barmode="group",
                        title="AI Impact Level by Industry")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.box(filtered, x="Industry", y="Automation Risk (%)",
                 title="Automation Risk Distribution by Industry")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    trend = filtered.groupby("Industry").agg(
        Avg_Salary=("Median Salary (USD)", "mean"),
        Avg_Remote_Ratio=("Remote Work Ratio (%)", "mean"),
    ).reset_index()
    fig = px.bar(trend, x="Industry", y="Avg_Salary", title="Average Salary by Industry")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    proj = filtered.groupby("Industry")[["Job Openings (2024)", "Projected Openings (2030)"]].sum().reset_index()
    proj_melted = proj.melt(id_vars="Industry", var_name="Year", value_name="Openings")
    fig = px.bar(proj_melted, x="Industry", y="Openings", color="Year", barmode="group",
                 title="Job Openings: 2024 vs Projected 2030")
    st.plotly_chart(fig, use_container_width=True)

st.dataframe(filtered.head(200))

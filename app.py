import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EcoPulse Analytics", layout="wide", page_icon="🌱")

st.title("🌱 EcoPulse Analytics: Global Climate & Energy Tracker")
st.markdown("Interactive platform tracking carbon emissions and energy trends globally.")

# Loading data with caching to improve performance
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(url)
    
    # Filter the data for relevant years and non-null countries
    df = df[(df['year'] >= 2000) & (df['country'].notna())]
    return df

with st.spinner("Loading global data..."):
    df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
countries = st.sidebar.multiselect(
    "Select Countries", 
    options=df['country'].unique(), 
    default=["Iraq", "United States", "China", "Germany", "United Kingdom"]
)

year_range = st.sidebar.slider(
    "Select Year Range", 
    int(df['year'].min()), int(df['year'].max()), (2006, 2022)
)

filtered_df = df[(df['country'].isin(countries)) & (df['year'].between(year_range[0], year_range[1]))]

# Key Metrics Display
col1, col2, col3 = st.columns(3)
col1.metric("Selected Countries", len(countries))
col2.metric("Start Year", year_range[0])
col3.metric("End Year", year_range[1])

st.divider()

# Tabs for Visualizations
tab1, tab2 = st.tabs(["CO2 Emissions Trends", "Primary Energy Consumption"])

with tab1:
    st.subheader("CO2 Emissions Over Time (Million Tonnes)")
    fig_co2 = px.line(filtered_df, x="year", y="co2", color="country", markers=True)
    st.plotly_chart(fig_co2, use_container_width=True)

with tab2:
    st.subheader("Primary Energy Consumption (TWh)")
    fig_energy = px.bar(filtered_df, x="year", y="primary_energy_consumption", color="country", barmode="group")
    st.plotly_chart(fig_energy, use_container_width=True)
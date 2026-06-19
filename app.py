import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Quarterly Census Dashboard",
    layout="wide"
)
st.title("Quarterly Census Employment and Wage Dashboard")

st.markdown("""
Analyze employment, establishments, wages, industries, and regional trends using
Quarterly Census of Employment and Wages data.
""")

@st.cache_data(show_spinner=True)
def load_data(file):
    df = pd.read_csv(
        file,
        low_memory=False,
        on_bad_lines="skip"
    )

    df.columns = df.columns.str.strip()

    return df

file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if file is not None:

    df = load_data(file)

    st.subheader("Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", f"{df.shape[0]:,}")

    with col2:
        st.metric("Columns", f"{df.shape[1]:,}")
    st.divider()
    st.subheader("Key Metrics")

    col1, col2 , col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Establishments",
            f"{int(df['Establishments'].sum()):,}"
        )

    with col2:
        st.metric(
            "Total Employment",
            f"{int(df['Month 1 Employment'].sum()):,}"
        )
    with col3:
        st.metric(
            "Total Wage",
            f"{df['Total Wage'].sum():,.0f}"
    )
    st.divider()
    
    st.subheader("Employment Trend by Year")

    employment_by_year = (
        df.groupby("Year")["Month 1 Employment"]
        .sum()
        .reset_index()
        .sort_values("Year")
    )

    st.line_chart(
        employment_by_year.set_index("Year")
    )
    st.divider()
    st.subheader("Year-Based Analysis")

    selected_year = st.selectbox(
        "Choose Year",
        sorted(df["Year"].dropna().unique())
    )

    filtered_df = df[df["Year"] == selected_year]
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
       st.subheader("Top Industries by Employment")
 
       industry_employment = (
            filtered_df.groupby("NAICS Title")["Month 1 Employment"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            )
       st.bar_chart(industry_employment)

    with col2:
        st.subheader("Top Areas by Total Wages")

        top_areas_wages = (
            filtered_df.groupby("Area")["Total Wage"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(top_areas_wages)
    st.divider()
    st.subheader("Top Areas by Employment")

    area_employment = (
        filtered_df.groupby("Area")["Month 1 Employment"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(area_employment)
    st.divider()
    st.subheader("Interactive Data Explorer")
    column = st.selectbox(
        "Select Column",
        df.columns
    )
    if df[column].dtype == "object":
      
        st.subheader("Top Values")

        st.bar_chart(
            df[column].value_counts().head(20)
        )
        st.subheader("Filter Data")

        unique_values = (
            df[column]
            .dropna()
            .unique()[:100]
        )

        selected_value = st.selectbox(
            "Select Value",
            unique_values
        )

        filtered_data = df[
            df[column] == selected_value
        ]

        st.dataframe(
            filtered_data.head(100)
        )

    else:
        st.subheader("Statistical Summary")

        st.write(
            df[column].describe()
        )
        st.subheader("Distribution")

        st.line_chart(
            df[column]
            .dropna()
            .head(1000)
        )
    st.divider()
    with st.expander("Raw Dataset Preview"):
        st.dataframe(df.head(100))
else:
    st.info(
        "Upload a CSV file to begin analysis"
    )
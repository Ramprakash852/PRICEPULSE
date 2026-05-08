import os

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PricePulse Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== SIDEBAR CONTROLS ==========
st.sidebar.title("⚙️ Dashboard Controls")

# Auto-refresh interval
refresh_interval = st.sidebar.selectbox(
    "Auto-refresh interval",
    options=[5, 10, 30, 60],
    index=1,
    help="Seconds between data refreshes"
)

# Minimum rating filter
min_rating = st.sidebar.slider(
    "Minimum rating filter",
    min_value=1,
    max_value=5,
    value=1,
    help="Filter products by minimum rating"
)

# Price range filter
price_range = st.sidebar.slider(
    "Price range (£)",
    min_value=0.0,
    max_value=100.0,
    value=(0.0, 100.0),
    step=1.0,
    help="Filter products by price range"
)

# Show/hide availability
show_unavailable = st.sidebar.checkbox(
    "Show unavailable products",
    value=True
)

st.sidebar.info(
    f"🔄 Data refreshes every {refresh_interval} seconds"
)

# ========== FETCH DATA ==========
@st.cache_data(ttl=refresh_interval)
def fetch_data():
    """Fetch product data from API"""
    try:
        API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/products")
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to fetch data: {e}")
        return pd.DataFrame()

df = fetch_data()

if df.empty:
    st.error("No data available. Please ensure the API is running.")
    st.stop()

# ========== APPLY FILTERS ==========
filtered_df = df[
    (df["rating"] >= min_rating) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

if not show_unavailable:
    filtered_df = filtered_df[filtered_df["availability"].str.contains("available", case=False, na=False)]

# ========== HEADER ==========
st.title("💰 PricePulse Dashboard")
st.markdown("Competitor Price Intelligence Platform")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# ========== METRICS CARDS ==========
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Products",
        value=len(df),
        help="Total number of products tracked"
    )

with col2:
    avg_price = df["price"].mean()
    st.metric(
        label="Average Price",
        value=f"£{avg_price:.2f}",
        help="Mean product price"
    )

with col3:
    highest_rated = df["rating"].max()
    st.metric(
        label="Highest Rating",
        value=highest_rated,
        help="Maximum product rating"
    )

with col4:
    lowest_price = df["price"].min()
    st.metric(
        label="Lowest Price",
        value=f"£{lowest_price:.2f}",
        help="Minimum product price"
    )

# ========== CHARTS SECTION ==========
st.subheader("📈 Price & Rating Analysis")

chart_col1, chart_col2 = st.columns(2)

# Price distribution chart
with chart_col1:
    st.subheader("Price Distribution")
    fig_price = px.histogram(
        filtered_df,
        x="price",
        nbins=20,
        labels={"price": "Price (£)"},
        title="Product Price Distribution",
        color_discrete_sequence=["#1f77b4"]
    )
    fig_price.update_layout(
        showlegend=False,
        height=400,
        hovermode="x unified"
    )
    st.plotly_chart(fig_price, use_container_width=True)

# Rating distribution chart
with chart_col2:
    st.subheader("Rating Distribution")
    rating_counts = filtered_df["rating"].value_counts().sort_index()
    fig_rating = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        labels={"x": "Rating", "y": "Count"},
        title="Product Rating Distribution",
        color_discrete_sequence=["#ff7f0e"]
    )
    fig_rating.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Rating",
        yaxis_title="Number of Products"
    )
    st.plotly_chart(fig_rating, use_container_width=True)

# ========== PRICE TREND (if available) ==========
st.subheader("💹 Price Trends by Rating")
if "scraped_at" in filtered_df.columns:
    fig_trend = px.scatter(
        filtered_df,
        x="rating",
        y="price",
        size="rating",
        color="rating",
        hover_data=["title", "availability"],
        title="Price vs Rating Analysis",
        labels={"price": "Price (£)", "rating": "Rating"},
        color_continuous_scale="Viridis"
    )
    fig_trend.update_layout(height=450)
    st.plotly_chart(fig_trend, use_container_width=True)

# ========== DETAILED TABLES ==========
st.subheader("📋 All Products")
st.dataframe(
    filtered_df[["title", "price", "availability", "rating", "created_at"]].sort_values("price"),
    use_container_width=True,
    height=300
)

st.subheader("⭐ Top Rated Products (Rating ≥ 4)")
top_rated = filtered_df[filtered_df["rating"] >= 4].sort_values("rating", ascending=False)
if not top_rated.empty:
    st.dataframe(
        top_rated[["title", "price", "availability", "rating"]],
        use_container_width=True,
        height=250
    )
else:
    st.info("No top-rated products match your filters.")

st.subheader("💰 Best Discounts (Lowest Prices)")
best_discounts = filtered_df.nsmallest(5, "price")
if not best_discounts.empty:
    fig_discounts = px.bar(
        best_discounts,
        x="title",
        y="price",
        title="Top 5 Lowest Prices",
        labels={"price": "Price (£)", "title": "Product"},
        color_discrete_sequence=["#2ca02c"]
    )
    fig_discounts.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    st.plotly_chart(fig_discounts, use_container_width=True)

# ========== STATISTICS ==========
st.subheader("📊 Price Statistics")
st.write(filtered_df["price"].describe())

# ========== FOOTER ==========
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <small>PricePulse • Competitor Price Intelligence Platform</small>
    </div>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="E-Commerce Streaming Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Streaming Data Dashboard")
st.caption("Assignment 3 – Analysis of Kafka-consumed e-commerce data")

# MongoDB Atlas connection
load_dotenv(".env", override=True)

try:
    client = MongoClient(
        os.getenv("MONGODB_URI"),
        serverSelectionTimeoutMS=10000
    )
    client.admin.command("ping")
    db = client["sda_assignment3"]
except Exception as e:
    st.error(f"MongoDB connection failed: {e}")
    st.stop()

# Load data from MongoDB
orders = pd.DataFrame(list(db["orders"].find({}, {"_id": 0})))
payments = pd.DataFrame(list(db["payments"].find({}, {"_id": 0})))
inventory = pd.DataFrame(list(db["inventory"].find({}, {"_id": 0})))
deliveries = pd.DataFrame(list(db["deliveries"].find({}, {"_id": 0})))

# Data cleaning
if not orders.empty:
    orders["Total_Amount"] = pd.to_numeric(
        orders["Total_Amount"], errors="coerce"
    )
    orders["Quantity"] = pd.to_numeric(
        orders["Quantity"], errors="coerce"
    )

if not payments.empty:
    payments["Amount"] = pd.to_numeric(
        payments["Amount"], errors="coerce"
    )

st.success("Connected to MongoDB Atlas")

# KPIs
total_orders = len(orders)

total_revenue = (
    orders["Total_Amount"].sum()
    if "Total_Amount" in orders.columns else 0
)

units_ordered = (
    orders["Quantity"].sum()
    if "Quantity" in orders.columns else 0
)

successful_payments = (
    len(
        payments[
            payments["Payment_Status"]
            .astype(str)
            .str.lower()
            .isin(["success", "successful", "completed"])
        ]
    )
    if "Payment_Status" in payments.columns else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Units Ordered", f"{units_ordered:,.0f}")
col4.metric("Successful Payments", f"{successful_payments:,}")

st.divider()

# Orders by City
col1, col2 = st.columns(2)

with col1:
    st.subheader("Orders by City")

    city_data = orders["City"].value_counts().reset_index()
    city_data.columns = ["City", "Orders"]

    fig = px.bar(
        city_data,
        x="City",
        y="Orders",
        text="Orders",
        title="Number of Orders by City"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Order Status")

    status_data = orders["Order_Status"].value_counts().reset_index()
    status_data.columns = ["Order_Status", "Count"]

    fig = px.pie(
        status_data,
        names="Order_Status",
        values="Count",
        title="Order Status Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Revenue + Payment Methods
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product Category")

    category_data = (
        orders.groupby("Category", as_index=False)["Total_Amount"]
        .sum()
    )

    fig = px.bar(
        category_data,
        x="Category",
        y="Total_Amount",
        text_auto=".2s",
        title="Revenue by Product Category"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Payment Methods")

    payment_data = payments["Payment_Method"].value_counts().reset_index()
    payment_data.columns = ["Payment_Method", "Count"]

    fig = px.bar(
        payment_data,
        x="Payment_Method",
        y="Count",
        text="Count",
        title="Orders by Payment Method"
    )

    st.plotly_chart(fig, use_container_width=True)

# Inventory
st.subheader("Inventory Status")

inventory_data = inventory["Stock_Status"].value_counts().reset_index()
inventory_data.columns = ["Stock_Status", "Count"]

fig = px.bar(
    inventory_data,
    x="Stock_Status",
    y="Count",
    text="Count",
    title="Inventory Stock Status"
)

st.plotly_chart(fig, use_container_width=True)

# Delivery
st.subheader("Delivery Status")

delivery_data = deliveries["Delivery_Status"].value_counts().reset_index()
delivery_data.columns = ["Delivery_Status", "Count"]

fig = px.pie(
    delivery_data,
    names="Delivery_Status",
    values="Count",
    title="Delivery Status Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Recent Orders
st.subheader("Recent Orders")

display_columns = [
    "Order_ID",
    "Timestamp",
    "Customer_ID",
    "Product_Name",
    "Category",
    "Quantity",
    "Total_Amount",
    "City",
    "Order_Status"
]

available_columns = [
    col for col in display_columns
    if col in orders.columns
]

st.dataframe(
    orders[available_columns].tail(10),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    "Dashboard developed using Python, Streamlit, Pandas, "
    "Plotly, Kafka and MongoDB Atlas."
)

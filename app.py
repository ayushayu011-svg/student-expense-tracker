import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE = "expenses.csv"

st.title("💰 Student Expense Tracker")

# Create CSV if not exists
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Date","Amount","Category","Description"])
    df.to_csv(FILE,index=False)

# Load data
df = pd.read_csv(FILE)

# Sidebar
st.sidebar.header("Add Expense")

amount = st.sidebar.number_input("Amount", min_value=0.0)
category = st.sidebar.selectbox(
    "Category",
    ["Food","Travel","Shopping","Entertainment","Education","Other"]
)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    new_data = pd.DataFrame({
        "Date":[datetime.now().strftime("%Y-%m-%d")],
        "Amount":[amount],
        "Category":[category],
        "Description":[description]
    })
    
    df = pd.concat([df,new_data],ignore_index=True)
    df.to_csv(FILE,index=False)
    
    st.success("Expense added!")

st.subheader("📋 Expense Data")
st.dataframe(df)

if not df.empty:

    st.subheader("📊 Expense by Category")
    category_total = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_total)

    st.subheader("📈 Spending Trend")
    daily = df.groupby("Date")["Amount"].sum()
    st.line_chart(daily)
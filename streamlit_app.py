import streamlit as st
import requests

st.title("Sales Prediction App")

st.write("Enter the details below to get a sales prediction:")

shop_id = st.number_input("Shop ID", min_value=0, step=1)
item_id = st.number_input("Item ID", min_value=0, step=1)
month_num = st.number_input("Month Number", min_value=1, max_value=12, step=1)
year = st.number_input("Year", min_value=2000, max_value=2100, step=1)
item_cnt_month_lag_1 = st.number_input("Item Count Month Lag 1", value=0.0)
item_cnt_month_lag_2 = st.number_input("Item Count Month Lag 2", value=0.0)
item_cnt_month_lag_3 = st.number_input("Item Count Month Lag 3", value=0.0)

if st.button("Predict"):
    data = {
        "shop_id": shop_id,
        "item_id": item_id,
        "month_num": month_num,
        "year": year,
        "item_cnt_month_lag_1": item_cnt_month_lag_1,
        "item_cnt_month_lag_2": item_cnt_month_lag_2,
        "item_cnt_month_lag_3": item_cnt_month_lag_3
    }
    try:
        response = requests.post("http://localhost:8000/predict", json=data)
        if response.status_code == 200:
            prediction = response.json()["prediction"]
            st.success(f"Predicted Sales: {prediction:.2f}")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to API: {e}") 
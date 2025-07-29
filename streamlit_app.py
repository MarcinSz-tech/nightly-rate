# streamlit_app.py

import streamlit as st

def calculate_nightly_rate(take_home, mgmt_fee, guest_clean_fee, client_clean_fee, linen_charge):
    # Stage 1: Adjust take-home if owner covers more than guest
    extra_cleaning_cost = (client_clean_fee + linen_charge) - guest_clean_fee
    if extra_cleaning_cost > 0:
        take_home += extra_cleaning_cost * 7  # assuming 7 cleans/month at 70% occupancy

    # Stage 2: Apply management fee multiplier
    fee_multipliers = {
        10: 100 / 69,
        15: 100 / 64,
        17: 100 / 60,
        18: 100 / 59
    }

    if mgmt_fee not in fee_multipliers:
        return None

    return take_home * fee_multipliers[mgmt_fee] / 21  # 21 nights per month (70% occupancy)


# Streamlit UI
st.title("Average Nightly Rate Calculator")
st.markdown("This calculator assumes **70% occupancy** (about 21 nights/month and 7 cleans/month).")

take_home = st.slider("Desired Monthly Take-home (£)", 500.0, 5000.0, 2000.0, step=50.0)
mgmt_fee = st.selectbox("Management Fee (%)", options=[10, 15, 17, 18])
guest_clean_fee = st.slider("Cleaning Fee Paid by Guest (£)", 20.0, 120.0, 60.0, step=5.0)
client_clean_fee = st.slider("Cleaning Fee Paid by Client (£, incl. VAT)", 20.0, 120.0, 70.0, step=5.0)
linen_charge = st.slider("Linen Charge per Clean (£, incl. VAT)", 0.0, 30.0, 16.8, step=0.5)

if st.button("Calculate"):
    result = calculate_nightly_rate(take_home, mgmt_fee, guest_clean_fee, client_clean_fee, linen_charge)
    if result:
        st.success(f"To achieve this goal, average nightly rate should be around: **£{result:.2f}**")
    else:
        st.error("Invalid management fee selected.")

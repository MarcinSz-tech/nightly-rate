import streamlit as st

# --- Function for live calculation ---
def calculate_required_nightly_rate(take_home, mgmt_fee, guest_clean_fee, client_clean_fee, linen_charge):
    try:
        # Step 1: Add extra cost if owner pays more for cleaning
        extra_clean_cost = (client_clean_fee + linen_charge) - guest_clean_fee
        if extra_clean_cost > 0:
            take_home += extra_clean_cost * 7  # 7 cleans/month at 70% occupancy

        # Step 2: Apply management fee multiplier
        multipliers = {
            10: 100 / 69,
            15: 100 / 64,
            17: 100 / 60,
            18: 100 / 59
        }

        if mgmt_fee not in multipliers:
            return None, "Invalid management fee selected."

        adjusted = take_home * multipliers[mgmt_fee]
        nightly_rate = adjusted / 21  # 70% occupancy = 21 nights/month

        return nightly_rate, None
    except Exception as e:
        return None, str(e)

# --- UI Layout ---
st.title("📊 Average Nightly Rate Calculator")
st.markdown("Estimate the nightly rate needed to meet your target income, based on occupancy and fees.")

# --- Section 3: Live What-If Calculator with Sliders ---
st.header("🎛️ What-If: Interactive Nightly Rate Estimator")
st.markdown("Adjust the sliders and inputs below to instantly see the nightly rate required to reach your goal.")

col1, col2 = st.columns(2)
with col1:
    take_home_slider = st.slider(
        "Desired monthly take-home pay (£):",
        min_value=500,
        max_value=4000,
        step=50,
        value=2000
    )
with col2:
    mgmt_fee_slider = st.select_slider(
        "Management fee (%):",
        options=[10, 15, 17, 18],
        value=15
    )

st.markdown("#### Cleaning & Linen Fees (per clean)")

guest_clean_fee_slider = st.number_input("Cleaning fee paid by guest (£):", min_value=0.0, step=1.0, value=50.0)
client_clean_fee_slider = st.number_input("Cleaning fee paid by owner (incl. VAT) (£):", min_value=0.0, step=1.0, value=70.0)
linen_charge_slider = st.number_input("Linen charge (incl. VAT) (£):", min_value=0.0, step=1.0, value=20.0)

# --- Live Calculation ---
nightly_rate_slider, error_slider = calculate_required_nightly_rate(
    take_home_slider,
    mgmt_fee_slider,
    guest_clean_fee_slider,
    client_clean_fee_slider,
    linen_charge_slider
)

if error_slider:
    st.error(error_slider)
else:
    st.success(
        f"To take home £{take_home_slider:.2f} with a {mgmt_fee_slider}% management fee, "
        f"you need an average nightly rate of **£{nightly_rate_slider:.2f}**."
    )

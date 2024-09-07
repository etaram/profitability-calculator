import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Input parameters
st.title('מחשבון השקעה דינאמי')

# User Inputs
num_villas = st.number_input('מספר וילות', min_value=1, value=10)
villa_size_sqm = st.number_input('גודל וילה (מ"ר)', min_value=1, value=200)
price_per_night = st.number_input('מחיר ללילה (₪)', min_value=1, value=3500)
occupancy_rate = st.slider('שיעור תפוסה (%)', min_value=0, max_value=100, value=40) / 100
land_cost_per_villa = st.number_input('עלות קרקע לוילה (₪)', min_value=0, value=500000)
construction_cost_per_sqm = st.number_input('עלות בנייה למ"ר (₪)', min_value=0, value=15000)
monthly_operational_cost_per_villa = st.number_input('עלות תפעול חודשית לוילה (₪)', min_value=0, value=4000)
annual_marketing_cost = st.number_input('עלות שיווק שנתית (₪)', min_value=0, value=600000)
land_development_cost = st.number_input('עלות פיתוח קרקע (₪)', min_value=0, value=200000)
public_area_development_cost = st.number_input('עלות פיתוח שטח ציבורי וחניות (₪)', min_value=0, value=1000000)
reception_and_logistics_cost = st.number_input('עלות מבנה קבלה ולוגיסטיקה (₪)', min_value=0, value=700000)
small_event_hall_cost = st.number_input('עלות אולם אירועים קטן (₪)', min_value=0, value=700000)
planning_and_consultants_cost = st.number_input('עלות תכנון ויועצים (₪)', min_value=0, value=150000)
cleaning_cost_per_night = st.number_input('עלות ניקיון ללילה (₪)', min_value=0, value=200)
accessories_cost_per_night = st.number_input('עלות אביזרים ללילה (₪)', min_value=0, value=50)
annual_insurance_cost_per_villa = st.number_input('עלות ביטוח שנתית לוילה (₪)', min_value=0, value=5000)
annual_inflation_rate = st.slider('שיעור אינפלציה שנתי (%)', min_value=0, max_value=100, value=2) / 100
discount_rate = st.slider('שיעור היוון (%)', min_value=0, max_value=100, value=8) / 100
prime_interest_rate = st.slider('ריבית פריים (%)', min_value=0.0, max_value=100.0, value=3.5) / 100
additional_interest_rate = st.number_input('ריבית נוספת מעל הפריים (%)', min_value=0.0, value=0.0) / 100

# Subsidy and tax rates
subsidy_min = 20 / 100
subsidy_max = 30 / 100
tax_rate = 7.5 / 100

# Calculations
total_land_construction_cost = (land_cost_per_villa * num_villas) + (construction_cost_per_sqm * villa_size_sqm * num_villas)
annual_revenue = price_per_night * (365 * occupancy_rate) * num_villas

annual_operational_cost = (
    (monthly_operational_cost_per_villa * 12 * num_villas) +
    annual_marketing_cost +
    (cleaning_cost_per_night * (365 * occupancy_rate) * num_villas) +
    (accessories_cost_per_night * (365 * occupancy_rate) * num_villas) +
    (annual_insurance_cost_per_villa * num_villas)
)

pre_tax_subsidy_profit = annual_revenue - annual_operational_cost
post_tax_profit_min = pre_tax_subsidy_profit * (1 - tax_rate) + total_land_construction_cost * subsidy_min
post_tax_profit_max = pre_tax_subsidy_profit * (1 - tax_rate) + total_land_construction_cost * subsidy_max

# Data for visualization
years = np.arange(1, 11)
cash_flow_min = [post_tax_profit_min / ((1 + discount_rate) ** year) for year in years]
cash_flow_max = [post_tax_profit_max / ((1 + discount_rate) ** year) for year in years]

# Display results in a table
results_df = pd.DataFrame({
    'Year': years,
    'Discounted Cash Flow (Min Subsidy)': cash_flow_min,
    'Discounted Cash Flow (Max Subsidy)': cash_flow_max
})

st.write("### Project Cash Flow Analysis")
st.dataframe(results_df)

# Plotting the graphs
st.write("### Discounted Cash Flow Analysis over 10 Years")
fig, ax = plt.subplots()
ax.plot(years, cash_flow_min, label='Discounted Cash Flow (Min Subsidy)', marker='o')
ax.plot(years, cash_flow_max, label='Discounted Cash Flow (Max Subsidy)', marker='o')
ax.set_title('Discounted Cash Flow Analysis over 10 Years')
ax.set_xlabel('Years')
ax.set_ylabel('Discounted Cash Flow (₪)')
ax.legend()
ax.grid(True)

st.pyplot(fig)

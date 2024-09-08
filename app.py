import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf
from fpdf import FPDF

# עיצוב כותרת האפליקציה והסגנון הכללי
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        color: #d04f30;
        text-align: center;
        margin-bottom: 30px;
    }
    .stApp {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        height: 40px;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .css-1cpxqw2, .css-1kyxreq, .css-14xtw13, .css-1lcbmhc, .css-2trqyj, .css-1vbd788, .css-1b0ba9k, .css-10trblm {
        color: #000000 !important;
        font-size: 20px !important;
        text-align: right;
    }
    .dataframe {
        background-color: #ffffff;
        color: #000000 !important;
        font-size: 20px !important;
        border: 1px solid #dddddd;
        text-align: right;
        padding: 5px;
        border-radius: 5px;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# כותרת ראשית
st.markdown('<p class="main-title">מחשבון השקעה דינאמי לפרויקט וילות</p>', unsafe_allow_html=True)
st.image("קבוצת מעיינות.png", use_column_width=True)

# פונקציה לחישוב תוצאות פיננסיות לפרויקט
def calculate_financial_metrics(villas, size):
    # חישוב עלויות הקמה
    construction_cost = construction_cost_per_sqm * size * villas
    land_cost = land_cost_per_villa * villas
    total_construction_cost = (
        construction_cost +
        land_cost +
        land_development_cost +
        public_area_development_cost +
        reception_and_logistics_cost +
        small_event_hall_cost +
        planning_and_consultants_cost
    )

    # חישוב הכנסות שנתיות מהשכרת וילות
    annual_revenue = price_per_night * occupancy_rate * 365 * villas

    # חישוב רווח גולמי שנתי (ברוטו)
    gross_annual_profit = annual_revenue

    # חישוב עלויות תפעול משתנות (ניקיון ואביזרים)
    total_cleaning_cost = cleaning_cost_per_night * 365 * occupancy_rate * villas
    total_accessories_cost = accessories_cost_per_night * 365 * occupancy_rate * villas

    # חישוב עלויות תפעול קבועות (תפעול חודשי לוילה, ביטוח ושיווק)
    operational_cost_per_villa = monthly_operational_cost_per_villa * 12
    total_insurance_cost = annual_insurance_cost_per_villa * villas
    total_operational_fixed_cost = (operational_cost_per_villa * villas + total_insurance_cost + annual_marketing_cost)

    # חישוב רווח תפעולי שנתי
    operating_annual_profit = gross_annual_profit - (total_cleaning_cost + total_accessories_cost + total_operational_fixed_cost)

    # חישוב רווח נקי שנתי לפני סובסידיה (כולל מס שנתי)
    net_annual_profit_before_subsidy = operating_annual_profit * (1 - tax_rate)

    # חישוב חלק שנתי של הסובסידיה
    annual_subsidy_min = (total_construction_cost * subsidy_min) / loan_term
    annual_subsidy_max = (total_construction_cost * subsidy_max) / loan_term

    # חישוב רווח נקי שנתי כולל סובסידיה (מחולק לאורך כל תקופת ההלוואה)
    net_annual_profit_with_subsidy_min = net_annual_profit_before_subsidy + annual_subsidy_min
    net_annual_profit_with_subsidy_max = net_annual_profit_before_subsidy + annual_subsidy_max

    # חישוב NPV עם סובסידיה
    cash_flow_min = [-total_construction_cost] + [net_annual_profit_with_subsidy_min] * loan_term
    cash_flow_max = [-total_construction_cost] + [net_annual_profit_with_subsidy_max] * loan_term
    total_npv_min = npf.npv(discount_rate, cash_flow_min)
    total_npv_max = npf.npv(discount_rate, cash_flow_max)

    # חישוב ROI עם סובסידיה מינימלית ומקסימלית
    roi_min = ((net_annual_profit_with_subsidy_min * loan_term) - (total_construction_cost * (1 - subsidy_min))) / (total_construction_cost * (1 - subsidy_min)) * 100
    roi_max = ((net_annual_profit_with_subsidy_max * loan_term) - (total_construction_cost * (1 - subsidy_max))) / (total_construction_cost * (1 - subsidy_max)) * 100

    # חישוב IRR
    irr_min = npf.irr(cash_flow_min) * 100
    irr_max = npf.irr(cash_flow_max) * 100

    # חישוב תקופת החזר
    payback_period_min = (total_construction_cost * (1 - subsidy_min)) / net_annual_profit_with_subsidy_min
    payback_period_max = (total_construction_cost * (1 - subsidy_max)) / net_annual_profit_with_subsidy_max

    # החזרת ערכי המדדים הפיננסיים
    return {
        'Gross Annual Profit': gross_annual_profit,
        'Operating Annual Profit': operating_annual_profit,
        'Net Annual Profit (Before Subsidy)': net_annual_profit_before_subsidy,
        'Net Annual Profit with Min Subsidy': net_annual_profit_with_subsidy_min,
        'Net Annual Profit with Max Subsidy': net_annual_profit_with_subsidy_max,
        'NPV Min': total_npv_min,
        'NPV Max': total_npv_max,
        'ROI Min': roi_min,
        'ROI Max': roi_max,
        'IRR Min': irr_min,
        'IRR Max': irr_max,
        'Payback Period Min': payback_period_min,
        'Payback Period Max': payback_period_max,
        'Total Construction Cost': total_construction_cost,
        'Annual Operational Cost': total_operational_fixed_cost + total_cleaning_cost + total_accessories_cost
    }

# קלטים מהמשתמש
num_villas = st.slider('מספר וילות', min_value=5, max_value=40, value=10, step=1)
villa_size_sqm = st.slider('גודל וילה (מ"ר)', min_value=120, max_value=250, value=200, step=10)
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
equity_amount = st.number_input('הון עצמי (₪)', min_value=0, value=1000000)
loan_term = st.slider('תקופת הלוואה (שנים)', min_value=5, max_value=15, value=15, step=1)
repayment_type = st.selectbox('סוג סילוקין', ['שפיצר', 'קרן שווה', 'בוליט'])

# שיעור מס וסובסידיות
subsidy_min = 20 / 100
subsidy_max = 30 / 100
tax_rate = 7.5 / 100

# פונקציה לחישוב החזר חודשי לפי סוג סילוקין
def calculate_loan_repayment(total_loan, annual_rate, loan_term_years, repayment_type):
    monthly_rate = annual_rate / 12
    num_payments = loan_term_years * 12
    payments = []

    if repayment_type == 'שפיצר':
        monthly_payment = npf.pmt(monthly_rate, num_payments, -total_loan)
        for n in range(1, num_payments + 1):
            interest_payment = total_loan * monthly_rate
            principal_payment = monthly_payment - interest_payment
            total_loan -= principal_payment
            payments.append({
                'תשלום': n,
                'קרן לתשלום': round(principal_payment),
                'ריבית לתשלום': round(interest_payment),
                'תשלום חודשי': round(monthly_payment),
                'יתרת הלוואה': round(total_loan)
            })

    elif repayment_type == 'קרן שווה':
        monthly_principal = total_loan / num_payments
        for n in range(1, num_payments + 1):
            interest_payment = total_loan * monthly_rate
            total_payment = monthly_principal + interest_payment
            total_loan -= monthly_principal
            payments.append({
                'תשלום': n,
                'קרן לתשלום': round(monthly_principal),
                'ריבית לתשלום': round(interest_payment),
                'תשלום חודשי': round(total_payment),
                'יתרת הלוואה': round(total_loan)
            })

    elif repayment_type == 'בוליט':
        for n in range(1, num_payments + 1):
            interest_payment = total_loan * monthly_rate
            payments.append({
                'תשלום': n,
                'קרן לתשלום': 0 if n < num_payments else total_loan,
                'ריבית לתשלום': round(interest_payment),
                'תשלום חודשי': round(interest_payment) if n < num_payments else round(interest_payment + total_loan),
                'יתרת הלוואה': total_loan if n < num_payments else 0
            })

    return payments

# חישוב עלות ההשקעה בניכוי הון עצמי
total_project_cost = (
    construction_cost_per_sqm * villa_size_sqm * num_villas +
    land_cost_per_villa * num_villas +
    land_development_cost +
    public_area_development_cost +
    reception_and_logistics_cost +
    small_event_hall_cost +
    planning_and_consultants_cost
)

loan_amount = total_project_cost - equity_amount

# חישוב תשלומי הלוואה
loan_payments = calculate_loan_repayment(loan_amount, prime_interest_rate + additional_interest_rate, loan_term, repayment_type)
loan_payments_df = pd.DataFrame(loan_payments)

# חישוב תוצאות פיננסיות לפרויקט
metrics = calculate_financial_metrics(num_villas, villa_size_sqm)

# הצגת תוצאות פיננסיות מפורטות
st.write(f"**רווח גולמי שנתי:** {int(metrics['Gross Annual Profit']):,} ₪")
st.write(f"**רווח תפעולי שנתי:** {int(metrics['Operating Annual Profit']):,} ₪")
st.write(f"**רווח נקי שנתי לפני סובסידיה:** {int(metrics['Net Annual Profit (Before Subsidy)']):,} ₪")
st.write(f"**רווח נקי שנתי עם סובסידיה מינימלית:** {int(metrics['Net Annual Profit with Min Subsidy']):,} ₪")
st.write(f"**רווח נקי שנתי עם סובסידיה מקסימלית:** {int(metrics['Net Annual Profit with Max Subsidy']):,} ₪")
st.write(f"**החזר על השקעה (ROI) מינימלי:** {metrics['ROI Min']:.2f}%")
st.write(f"**החזר על השקעה (ROI) מקסימלי:** {metrics['ROI Max']:.2f}%")
st.write(f"**ערך נוכחי נקי (NPV) מינימלי:** {int(metrics['NPV Min']):,} ₪")
st.write(f"**ערך נוכחי נקי (NPV) מקסימלי:** {int(metrics['NPV Max']):,} ₪")
st.write(f"**שיעור תשואה פנימית (IRR) מינימלי:** {metrics['IRR Min']:.2f}%")
st.write(f"**שיעור תשואה פנימית (IRR) מקסימלי:** {metrics['IRR Max']:.2f}%")
st.write(f"**תקופת החזר מינימלית:** {metrics['Payback Period Min']:.2f} שנים")
st.write(f"**תקופת החזר מקסימלית:** {metrics['Payback Period Max']:.2f} שנים")

# הצגת טבלת תשלומי הלוואה
st.markdown("<div dir='rtl'>### תשלומי הלוואה לפי סוג סילוקין</div>", unsafe_allow_html=True)
st.dataframe(loan_payments_df.style.set_properties(**{'text-align': 'right'}))

# גרפים נוספים
st.markdown("<div dir='rtl'>### גרפים נוספים</div>", unsafe_allow_html=True)
fig1, ax1 = plt.subplots()
years = list(range(1, loan_term + 1))
cash_flows_subsidy_min = [metrics['Net Annual Profit with Min Subsidy'] / ((1 + discount_rate) ** y) for y in years]
cash_flows_subsidy_max = [metrics['Net Annual Profit with Max Subsidy'] / ((1 + discount_rate) ** y) for y in years]
ax1.plot(years, cash_flows_subsidy_min, label='Cash Flows with Minimum Subsidy')
ax1.plot(years, cash_flows_subsidy_max, label='Cash Flows with Maximum Subsidy')
ax1.set_title('Comparison of Cash Flows with and without Subsidy')
ax1.set_xlabel('Years')
ax1.set_ylabel('Cash Flows (₪)')
ax1.legend()
st.pyplot(fig1)

# גרף השוואת ROI לפי מספר וילות
fig3, ax3 = plt.subplots(figsize=(10, 6))
villa_range = range(5, 41)
roi_results = [calculate_financial_metrics(v, villa_size_sqm)['ROI Min'] for v in villa_range]
ax3.plot(villa_range, roi_results, marker='o', label='ROI (Return on Investment)', color='blue')
ax3.set_title('ROI by Number of Villas')
ax3.set_xlabel('Number of Villas')
ax3.set_ylabel('ROI (%)')
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)


# פונקציה לניתוח רגישות עבור ROI מול תקופת ההחזר
def sensitivity_analysis_roi_vs_time(base_villas, base_size, variable_name, variable_range):
    roi_results = []
    payback_results = []

    for value in variable_range:
        # הגדרת ערך משתנה בהתאם למשתנה לניתוח רגישות
        if variable_name == 'Number of Villas':
            metrics = calculate_financial_metrics(value, base_size)
        elif variable_name == 'Occupancy Rate':
            global occupancy_rate
            occupancy_rate = value / 100
            metrics = calculate_financial_metrics(base_villas, base_size)
        elif variable_name == 'Price per Night':
            global price_per_night
            price_per_night = value
            metrics = calculate_financial_metrics(base_villas, base_size)

        # הוספת תוצאות ה-ROI ותקופת ההחזר לרשימות
        roi_results.append(metrics['ROI Min'])
        payback_results.append(metrics['Payback Period Min'])

    return roi_results, payback_results


# הצגת תפריט ניתוח רגישות
st.markdown("### Sensitivity Analysis: ROI vs. Payback Period")
variable_to_analyze = st.selectbox('Select Variable for Sensitivity Analysis',
                                   ['Number of Villas', 'Occupancy Rate', 'Price per Night'])

# הגדרת טווחים מעודכנים
if variable_to_analyze == 'Number of Villas':
    variable_range = st.slider('Select Range for Number of Villas', min_value=5, max_value=40, value=(10, 20))
elif variable_to_analyze == 'Occupancy Rate':
    variable_range = st.slider('Select Range for Occupancy Rate (%)', min_value=0, max_value=100, value=(20, 80))
elif variable_to_analyze == 'Price per Night':
    variable_range = st.slider('Select Range for Price per Night (₪)', min_value=2000, max_value=8000,
                               value=(3500, 5000))

# חישוב תוצאות ניתוח רגישות
roi_results_sensitivity, payback_results_sensitivity = sensitivity_analysis_roi_vs_time(num_villas, villa_size_sqm,
                                                                                        variable_to_analyze,
                                                                                        range(variable_range[0],
                                                                                              variable_range[1] + 1))

# הצגת גרף ניתוח רגישות: ROI מול תקופת ההחזר
fig_sensitivity, ax_sensitivity = plt.subplots(figsize=(10, 6))
ax_sensitivity.plot(payback_results_sensitivity, roi_results_sensitivity, marker='o', linestyle='-', color='b',
                    label='ROI vs. Payback Period')
ax_sensitivity.set_title(f'Sensitivity Analysis: ROI vs. Payback Period by {variable_to_analyze}')
ax_sensitivity.set_xlabel('Payback Period (Years)')
ax_sensitivity.set_ylabel('ROI (%)')
ax_sensitivity.legend()
st.pyplot(fig_sensitivity)

import pandas as pd
import streamlit as st


# פונקציה ליצירת דוח Excel
def generate_excel_report():
    # יצירת מילון עם הנתונים הפיננסיים
    data = {
        "Metric": [
            "Gross Annual Profit", "Operating Annual Profit",
            "Net Annual Profit before Subsidy", "Net Annual Profit with Minimum Subsidy",
            "Net Annual Profit with Maximum Subsidy", "Net Present Value (NPV) Minimum",
            "Net Present Value (NPV) Maximum", "Internal Rate of Return (IRR) Minimum",
            "Internal Rate of Return (IRR) Maximum", "Return on Investment (ROI) Minimum",
            "Return on Investment (ROI) Maximum", "Payback Period Minimum",
            "Payback Period Maximum"
        ],
        "Value": [
            f"{int(metrics['Gross Annual Profit']):,} ₪",
            f"{int(metrics['Operating Annual Profit']):,} ₪",
            f"{int(metrics['Net Annual Profit (Before Subsidy)']):,} ₪",
            f"{int(metrics['Net Annual Profit with Min Subsidy']):,} ₪",
            f"{int(metrics['Net Annual Profit with Max Subsidy']):,} ₪",
            f"{int(metrics['NPV Min']):,} ₪",
            f"{int(metrics['NPV Max']):,} ₪",
            f"{metrics['IRR Min']:.2f}%",
            f"{metrics['IRR Max']:.2f}%",
            f"{metrics['ROI Min']:.2f}%",
            f"{metrics['ROI Max']:.2f}%",
            f"{metrics['Payback Period Min']:.2f} years",
            f"{metrics['Payback Period Max']:.2f} years"
        ]
    }

    # יצירת DataFrame
    df = pd.DataFrame(data)

    # שמירת DataFrame כקובץ Excel
    excel_filename = "investment_report.xlsx"
    df.to_excel(excel_filename, index=False)

    # הצגת הודעה למשתמש והורדת הקובץ
    with open(excel_filename, "rb") as file:
        st.download_button(label='Download Excel Report', data=file, file_name=excel_filename)


# כפתור ליצירת דוח Excel
if st.button('Generate Excel Report'):
    generate_excel_report()

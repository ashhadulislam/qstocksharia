import streamlit as st
import pickle
import os

import os
import pickle
import re
import pandas as pd
import matplotlib.pyplot as plt

import sys
import plotly.graph_objects as go
import streamviz 



sys.path.append("/Users/dr.ashhadulislam/projects/social/musaffaScraper")
import config

qat_categories=config.qat_categories
qat_company_categorised=config.qat_company_categorised


# Helper function to convert formatted strings to float
def parse_value(value):
    value = value.replace(",", "").upper()
    if value.endswith("B"):
        return float(value[:-1]) * 1e9
    elif value.endswith("M"):
        return float(value[:-1]) * 1e6
    elif value.endswith("K"):
        return float(value[:-1]) * 1e3
    return float(value)


def load_company_data(company_code):
    path = f"reports/{company_code.replace('.', '_')}.pkl"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def color_status(text):
    if "NOT HALAL" in text.upper() or "FAIL" in text.upper():
        return f"❌ **{text}**"
    elif "DOUBTFUL" in text.upper():
        return f"⚠️ **{text}**"
    else:
        return f"✅ **{text}**"

st.title("📊 Shariah Compliance Report")

# Category Dropdown
selected_cat = st.selectbox("Select Company Category", options=qat_categories.keys(), format_func=lambda x: qat_categories[x])

# Company Dropdown
selected_company = st.selectbox("Select Company", options=qat_company_categorised[selected_cat])

# Load data
data = load_company_data(selected_company)

if data:
    st.header("📌 Shariah Compliance Overview")
    for k, v in data['shariah_compliance_info_level1'].items():
        if k=='History Link' or k=='Action Button':
            continue
        st.markdown(f"**{k}**: {color_status(v) if k == 'Compliance Status' else v}")

    st.header("📦 Business Screening")
    st.markdown(f"**Business Activity**: {color_status(data['business_screening']['business_activity'])}")

    st.header("💰 Absolute Halal Calculation")
    # Extract values from dictionary
    
    calc_data = data["absolute_halal_calculation"]
    # Parse and calculate
    halal=parse_value(calc_data["Halal Sales & Income"])
    doubtful = parse_value(calc_data["Doubtful Sales & Income"])
    non_halal = parse_value(calc_data["Non Halal Sales & Income"])
    total_revenue = parse_value(calc_data["Total Revenue"])

    # Calculate percentages
    halal_percentage = round(halal / total_revenue * 100, 2)
    doubtful_percentage = round(doubtful / total_revenue * 100, 2)
    non_halal_percentage = round(non_halal / total_revenue * 100, 2)

    # Data setup
    sizes = [halal_percentage, doubtful_percentage, non_halal_percentage]
    labels = [
        f"Halal ({halal_percentage}%)",
        f"Doubtful ({doubtful_percentage}%)",
        f"Not Halal ({non_halal_percentage}%)"
    ]
    colors = ['#1b5e20', '#ff9800', '#c62828']

    # Plot
    fig, ax = plt.subplots()
    wedges, texts = ax.pie(
        sizes,
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.4),  # makes it a donut
        pctdistance=0.85,
        textprops={'fontsize': 12}
    )

    # Equal aspect for circular pie
    ax.axis('equal')

    # Legend at the bottom
    plt.legend(
        wedges,
        labels,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False
    )

    # Title & show
    st.header("🍩 Halal Revenue Breakdown")
    st.pyplot(fig)


    st.write('''The combined value of Non Halal and Doubtful sources should not exceed 5% of the Total Revenue (Gross Sales + Other Income). ''')
    st.header("Calculation")

    numerator = doubtful + non_halal
    percent = (numerator / total_revenue) * 100

    # Layout
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("### 📊 Breakdown")
        st.table({
            "Description": [
                "Halal Sales & Income",
                "Doubtful Sales & Income",
                "Non Halal Sales & Income",
                "**Total Revenue**"
            ],
            "Value": [
                calc_data["Halal Sales & Income"],
                calc_data["Doubtful Sales & Income"],
                calc_data["Non Halal Sales & Income"],
                f"**{calc_data['Total Revenue']}**"
            ]
        })

    with col2:
        st.markdown("### 📐 Not Halal Business Activity %")
        st.markdown(
            f"""
            <div style='border: 2px dashed orange; padding: 16px; border-radius: 8px; background-color: #fff7ed; font-family: monospace'>
            Not Halal Business Activity Percentage =<br><br>
            <strong>( Non Halal Sales & Income + Doubtful Sales & Income )</strong><br>
            <span style='font-weight: bold;'>÷</span><br>
            <strong>( Total Revenue )</strong><br><br>

            {calc_data["Non Halal Sales & Income"]} + {calc_data["Doubtful Sales & Income"]}<br>
            = <strong>{calc_data["Non Halal Sales & Income"]} + {calc_data["Doubtful Sales & Income"]}</strong><br>
            ÷ {calc_data["Total Revenue"]}<br><br>
            = <strong style="color:orange;">{percent:.2f}%</strong>
            </div>
            """,
            unsafe_allow_html=True
        ) 

    

    # Map to emojis and text colors
    style_map = {
        "Halal Revenue": {"emoji": "🟢", "bg": "#e6f4ea"},
        "Doubtful Income": {"emoji": "🟠", "bg": "#fff4e5"},
        "Not Halal Income": {"emoji": "🔴", "bg": "#fde8e8"},
    }

    st.header("🧾 Detailed Report")

    for category, details in data["detailed_report"].items():
        styles = style_map.get(category, {"emoji": "📄", "bg": "#f0f2f6"})

        label = f"{styles['emoji']} {category}"

        with st.expander(label):
            keys = [k for k in details if k != "_total"]
            total = details.get("_total")

            block = f'<div style="background-color:{styles["bg"]}; padding:1em; border-radius:8px;">'
            for subk in keys:
                block += f"<p><strong>{subk}</strong>: {details[subk]}</p>"
            if total:
                block += f"<p><strong>Total</strong>: {total}</p>"
            block += "</div>"

            st.markdown(block, unsafe_allow_html=True)



    st.header("💼 Financial Screening")
    for k, v in data["financial_screening"].items():
        st.markdown(f"- **{k.replace('_', ' ').title()}**: {color_status(v)}")

    st.header("📉 Interest-bearing securities and assets (% & Absolute)")

    # Value to show
    gauge_value=data['interest_bearing_percentage']['Interest-bearing securities and assets'].replace("%","")
    gauge_value=gauge_value.replace(",","")
    gauge_value = float(gauge_value)/100
    
    # Show the gauge (without unsupported keywords)
    streamviz.gauge(
        gVal=gauge_value,
        gTitle="Interest-bearing securities and assets", 
       # Optional: "" or a short title like "Compliance"
        gMode="gauge+number",     # Show both gauge and number
        gSize="FULL",              # Use "SML", "MED", "LRG", or "FULL" depending on layout
        grLow=0.3,                 # Low range ends at 30%
        grMid=0.7,                 # Mid range ends at 70% (not shown in image, but needed by API)
        gcLow="#00ff00",          # Pale red for compliant (<30%)
        gcMid="#FFA500",          # Keep same as low to match your image
        gcHigh="#ff0000",         # Strong red for non-compliant (>30%)
        sFix="%",                 # Percentage suffix
        gTheme="black",           # Gauge tick color and pointer theme
    )


    




    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div style="font-size:24px;"><b>Shariah-compliant</b><br><span style="color:grey;">Less than 30%</span></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div style="font-size:24px;"><b>Non-shariah compliant</b><br><span style="color:grey;">Greater than 30%</span></div>',
            unsafe_allow_html=True,
        )
    
    st.markdown('''Total amount of interest-bearing securities and assets, whether short or long term, **should not exceed 30% of the market capitalization** of the company to be Shariah compliant.''')

    # Add a caption manually
    st.markdown("**Interest-bearing Securities and Assets Percentage**")


    ibsa_toggler = st.toggle("Absolute/Percentage")

    if ibsa_toggler:        
        st.subheader("Percentage Calculation")
        col1, col2 = st.columns(2)
        with col1:            
            st.markdown(f"**Short-term:** {data['interest_bearing_percentage']['Short-term']}")
            st.markdown(f"**Long-term:** {data['interest_bearing_percentage']['Long-term']}")
            st.markdown(f"**Interest-bearing securities and assets:** {data['interest_bearing_percentage']['Interest-bearing securities and assets']}")            
        with col2:            
            numerator = data['interest_bearing_absolute']['Short-term']
            denominator = data['trailing_36_month_avg_market_cap']
            result = data['interest_bearing_percentage']['Interest-bearing securities and assets']

            st.markdown(f"""
            <div style="text-align: center; font-size: 16px; line-height: 1.6; font-family: monospace;">
            <b>Interest-bearing securities and assets percentage =</b><br><br>

            ( Interest-bearing securities and assets )<br>
            <hr style="border: 1px solid black; width: 80%; margin: 0 auto 5px auto;">
            ( Trailing 36-month average market capitalization )<br><br>

            <span style="display:inline-block;">
              {numerator}<br>
              <span style="border-top:2px solid black; display:inline-block; width:100%;">{denominator}</span><br>
              = <b>{result}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)            


    else:
        st.subheader("Absolute Calculation")
        col1, col2 = st.columns(2)
        with col1:            
            st.markdown(f"**Short-term:** {data['interest_bearing_absolute']['Short-term']}")
            st.markdown(f"**Long-term:** {data['interest_bearing_absolute']['Long-term']}")
            st.markdown(f"**Interest-bearing securities and assets:** {data['interest_bearing_absolute']['Interest-bearing securities and assets']}")            
        with col2:            
            numerator = data['interest_bearing_absolute']['Short-term']
            denominator = data['trailing_36_month_avg_market_cap']
            result = data['interest_bearing_percentage']['Interest-bearing securities and assets']

            st.markdown(f"""
            <div style="text-align: center; font-size: 16px; line-height: 1.6; font-family: monospace;">
            <b>Interest-bearing securities and assets percentage =</b><br><br>

            ( Interest-bearing securities and assets )<br>
            <hr style="border: 1px solid black; width: 80%; margin: 0 auto 5px auto;">
            ( Trailing 36-month average market capitalization )<br><br>

            <span style="display:inline-block;">
              {numerator}<br>
              <span style="border-top:2px solid black; display:inline-block; width:100%;">{denominator}</span><br>
              = <b>{result}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)            






    st.header("📉 Interest-bearing debt (% & Absolute)")

    # add gauge here

    # Value to show
    gauge_value = data['interest_bearing_debt_percentage']['Total Interest-bearing debt'].replace("%","")
    gauge_value=gauge_value.replace(",","")
    gauge_value = float(gauge_value)/100
    
    # Show the gauge (without unsupported keywords)
    streamviz.gauge(
        gVal=gauge_value,
        gTitle="Interest-bearing debt", 
       # Optional: "" or a short title like "Compliance"
        gMode="gauge+number",     # Show both gauge and number
        gSize="FULL",              # Use "SML", "MED", "LRG", or "FULL" depending on layout
        grLow=0.3,                 # Low range ends at 30%
        grMid=0.7,                 # Mid range ends at 70% (not shown in image, but needed by API)
        gcLow="#00ff00",          # Pale red for compliant (<30%)
        gcMid="#FFA500",          # Keep same as low to match your image
        gcHigh="#ff0000",         # Strong red for non-compliant (>30%)
        sFix="%",                 # Percentage suffix
        gTheme="black",           # Gauge tick color and pointer theme
    )


    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div style="font-size:24px;"><b>Shariah-compliant</b><br><span style="color:grey;">Less than 30%</span></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div style="font-size:24px;"><b>Non-shariah compliant</b><br><span style="color:grey;">Greater than 30%</span></div>',
            unsafe_allow_html=True,
        )
    
    st.markdown('''Interest-bearing debt, whether long-term or short-term debt **should not exceed 30% of the market capitalization** of the company. ''')

    ibd_toggler = st.toggle("Select Absolute/Percentage")
    if ibd_toggler:        
        st.subheader("Percentage Calculation")
        col1, col2 = st.columns(2)
        with col1:            
            st.markdown(f"**Short-term:** {data['interest_bearing_debt_percentage']['Short-term']}")
            st.markdown(f"**Long-term:** {data['interest_bearing_debt_percentage']['Long-term']}")
            st.markdown(f"**Interest-bearing securities and assets:** {data['interest_bearing_debt_percentage']['Total Interest-bearing debt']}")            
        with col2:            
            numerator = data['interest_bearing_debt_absolute']['Total Interest-bearing debt']
            denominator = data['trailing_36_month_avg_market_cap']
            result = data['interest_bearing_debt_percentage']['Total Interest-bearing debt']

            st.markdown(f"""
            <div style="text-align: center; font-size: 16px; line-height: 1.6; font-family: monospace;">
            <b>Interest-bearing securities and assets percentage =</b><br><br>

            ( Total interest-bearing debt )<br>
            <hr style="border: 1px solid black; width: 80%; margin: 0 auto 5px auto;">
            ( Trailing 36-month average market capitalization )<br><br>

            <span style="display:inline-block;">
              {numerator}<br>
              <span style="border-top:2px solid black; display:inline-block; width:100%;">{denominator}</span><br>
              = <b>{result}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)                        

    else:
        st.subheader("Absolute Calculation")
        col1, col2 = st.columns(2)
        with col1:            
            st.markdown(f"**Short-term:** {data['interest_bearing_debt_absolute']['Short-term']}")
            st.markdown(f"**Long-term:** {data['interest_bearing_debt_absolute']['Long-term']}")
            st.markdown(f"**Interest-bearing securities and assets:** {data['interest_bearing_debt_absolute']['Total Interest-bearing debt']}")            
        with col2:            
            numerator = data['interest_bearing_debt_absolute']['Total Interest-bearing debt']
            denominator = data['trailing_36_month_avg_market_cap']
            result = data['interest_bearing_debt_percentage']['Total Interest-bearing debt']

            st.markdown(f"""
            <div style="text-align: center; font-size: 16px; line-height: 1.6; font-family: monospace;">
            <b>Interest-bearing securities and assets percentage =</b><br><br>

            ( Total interest-bearing debt )<br>
            <hr style="border: 1px solid black; width: 80%; margin: 0 auto 5px auto;">
            ( Trailing 36-month average market capitalization )<br><br>

            <span style="display:inline-block;">
              {numerator}<br>
              <span style="border-top:2px solid black; display:inline-block; width:100%;">{denominator}</span><br>
              = <b>{result}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)  





    st.header("📚 Compliance History")
    for history in data["compliance_history"]:
        st.markdown(
            f"**{history['date_range']}** — _{history['report_source']}_ → {color_status(history['status'])}"
        )
else:
    st.warning("No report found for the selected company.")
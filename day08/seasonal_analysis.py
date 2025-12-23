"""
🌍 ECO-PULSE: ULTIMATE CLIMATE REPORT (FIXED PATHS)
Results are saved relative to the script's location.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from scipy import stats
import random
import matplotlib.patches as mpatches
from datetime import datetime

# ==========================================
# Path Configuration - This fixes the "wrong folder" issue
# ==========================================
# Get the absolute path of the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# ==========================================
# Helper Functions
# ==========================================

def get_general_recommendation():
    tips = [
        "🌱 <strong>Reduce Meat Consumption:</strong> The livestock industry is a major source of methane. Reducing meat intake helps lower global emissions.",
        "💡 <strong>Energy Efficiency:</strong> Switch to LED bulbs and energy-efficient appliances to reduce your carbon footprint significantly.",
        "🚗 <strong>Sustainable Transport:</strong> Whenever possible, walk, bike, or use public transportation instead of driving private vehicles.",
        "🗑️ <strong>Minimize Food Waste:</strong> Decomposing food in landfills produces methane. Buy only what you need and compost organic waste.",
        "🌡️ <strong>Smart Heating/Cooling:</strong> Adjusting your thermostat by just 1°C can reduce energy bills and emissions by up to 10%."
    ]
    return random.choice(tips)

def check_and_ask_user(df):
    info_path = os.path.join(OUTPUT_DIR, 'last_run_info.txt')
    if not os.path.exists(info_path):
        return True 
    
    with open(info_path, 'r') as f:
        last_date = f.read().strip()
    
    current_max_date = f"{df['Year'].max()}"
    
    if last_date == current_max_date:
        print(f"\n⚠️  NOTICE: The NASA data has not changed since your last run.")
        user_choice = input("   Do you want to regenerate the report anyway? (y/n): ").strip().lower()
        return user_choice in ['y', 'yes']
    return True

def update_last_run(df):
    info_path = os.path.join(OUTPUT_DIR, 'last_run_info.txt')
    with open(info_path, 'w') as f:
        f.write(f"{df['Year'].max()}")

# ==========================================
# Main Function
# ==========================================

def generate_interactive_report():
    print(f"⏳ Working Directory: {BASE_DIR}")
    print("⏳ Downloading data sources...")
    
    # Ensure output directory exists inside the project folder
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Temp Data
    url_temp = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    try:
        df = pd.read_csv(url_temp, skiprows=1, na_values='***')
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for col in months + ['Year']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['Temp_Avg'] = df[months].mean(axis=1)
    except Exception as e:
        print(f"❌ Error fetching Temp data: {e}")
        return

    # 2. Check Data
    if not check_and_ask_user(df):
        return

    # 3. CO2 Data
    url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        df_co2 = pd.read_csv(url_co2)
        df_co2 = df_co2[df_co2['country'] == 'World'][['year', 'co2']]
        df_co2 = df_co2.rename(columns={'year': 'Year', 'co2': 'CO2'})
    except Exception as e:
        print(f"❌ Error fetching CO2 data: {e}")
        return

    # Merge
    df_merged = pd.merge(df[['Year', 'Temp_Avg']], df_co2, on='Year')
    plt.style.use('seaborn-v0_8-whitegrid')
    
    print("✅ Generating charts & calculating stats...")

    # Chart 1: CO2 vs Temp
    fig, ax1 = plt.subplots(figsize=(12, 6))
    df_chart1 = df_merged[df_merged['Year'] >= 1950]
    correlation, _ = stats.pearsonr(df_chart1['CO2'], df_chart1['Temp_Avg'])
    
    l1 = ax1.plot(df_chart1['Year'], df_chart1['Temp_Avg'], color='#e74c3c', linewidth=3, label='Global Temp (°C)')
    ax2 = ax1.twinx()
    l2 = ax2.plot(df_chart1['Year'], df_chart1['CO2'], color='#34495e', linewidth=2, linestyle='--', label='CO2 Emissions')
    
    plt.title(f'1. The Driver: CO2 vs Temp (Correlation: {correlation:.2f})', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '1_co2_temp.png'), dpi=300)
    plt.close()

    # Chart 2: Stripes
    plt.figure(figsize=(14, 3))
    temps_all = df[df['Year'] >= 1880]['Temp_Avg']
    years_all = df[df['Year'] >= 1880]['Year']
    plt.bar(years_all, height=1, width=1.0, color=plt.cm.RdBu_r((temps_all - temps_all.min()) / (temps_all.max() - temps_all.min())))
    plt.axis('off')
    plt.savefig(os.path.join(OUTPUT_DIR, '2_stripes.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 3: Seasons
    df_bar = df[df['Year'] >= (df['Year'].max() - 20)].copy()
    df_bar_plot = df_bar[['Year', 'Jan', 'Apr', 'Jul', 'Oct']].set_index('Year')
    
    oct_increase = df_bar['Oct'].mean() - df[(df['Year'] >= 1950) & (df['Year'] <= 1980)]['Oct'].mean()
    avg_winter, avg_summer, avg_autumn = df_bar['Jan'].mean(), df_bar['Jul'].mean(), df_bar['Oct'].mean()

    ax = df_bar_plot.plot(kind='bar', figsize=(14, 7), width=0.85, color=['#3498db', '#2ecc71', '#e67e22', '#9b59b6'])
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '3_seasonal_bars.png'), dpi=300)
    plt.close()

    # Chart 4: Heatmap
    df_heat = df[df['Year'] >= (df['Year'].max() - 20)].set_index('Year')[months]
    extreme_count = (df_heat > 1.0).sum().sum()
    percent_extreme = (extreme_count / df_heat.size) * 100
    plt.figure(figsize=(12, 7))
    sns.heatmap(df_heat.T, cmap='RdBu_r', center=0, linewidths=0.5)
    plt.savefig(os.path.join(OUTPUT_DIR, '4_heatmap.png'), dpi=300)
    plt.close()

# --- HTML Report Generation ---
    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Generated here!
    recommendation = get_general_recommendation()
    # HTML Report
    recommendation = get_general_recommendation()
    html_content = f"""
    <html>
    <head><title>EcoPulse Report</title></head>
    <body style="font-family: sans-serif; max-width: 900px; margin: auto; padding: 20px;">
        <h1>🌍 EcoPulse Climate Analysis</h1>
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px;">
            <img src="1_co2_temp.png" style="max-width:100%;">
            <p><strong>Correlation:</strong> {correlation:.2f}</p>
        </div>
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px;">
            <img src="2_stripes.png" style="max-width:100%;">
        </div>
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px;">
            <img src="3_seasonal_bars.png" style="max-width:100%;">
            <p><strong>October warming:</strong> +{oct_increase:.2f}°C</p>
        </div>
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px;">
            <img src="4_heatmap.png" style="max-width:100%;">
            <p><strong>Extreme months:</strong> {percent_extreme:.1f}%</p>
        </div>
        <div style="background: #fcf3cf; padding: 20px; border: 2px solid #f1c40f;">
            <h3>🌱 Recommendation</h3>
            <p>{recommendation}</p>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'Final_Report.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    update_last_run(df)
    print(f"\n✅ Report Generated in: {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_interactive_report()

"""
🌍 ECO-PULSE: ULTIMATE CLIMATE REPORT (FULL VERSION)
Full analysis with 4 charts, seasonal statistics, and absolute path management.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from scipy import stats
import random
import matplotlib.patches as mpatches

# Absolute Path Configuration: Ensures outputs stay within the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

def get_general_recommendation():
    """Returns a randomly selected ecological tip with HTML formatting."""
    tips = [
        "🌱 <strong>Reduce Meat Consumption:</strong> The livestock industry is a major source of methane. Reducing meat intake helps lower global emissions.",
        "💡 <strong>Energy Efficiency:</strong> Switch to LED bulbs and energy-efficient appliances to reduce your carbon footprint significantly.",
        "🚗 <strong>Sustainable Transport:</strong> Whenever possible, walk, bike, or use public transportation instead of driving private vehicles.",
        "🗑️ <strong>Minimize Food Waste:</strong> Decomposing food in landfills produces methane. Buy only what you need and compost organic waste.",
        "🌡️ <strong>Smart Heating/Cooling:</strong> Adjusting your thermostat by just 1°C can reduce energy bills and emissions by up to 10%."
    ]
    return random.choice(tips)

def check_and_ask_user(df):
    """Checks if NASA data has changed and prompts user before re-running."""
    info_path = os.path.join(OUTPUT_DIR, 'last_run_info.txt')
    if not os.path.exists(info_path):
        return True 
    
    with open(info_path, 'r') as f:
        last_date = f.read().strip()
    
    current_max_date = f"{df['Year'].max()}"
    if last_date == current_max_date:
        print("\n⚠️  NOTICE: NASA data has not changed since the last run.")
        choice = input("   Regenerate report anyway? (y/n): ").strip().lower()
        return choice in ['y', 'yes']
    return True

def generate_interactive_report():
    """Main execution flow for full climate data processing and visualization."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"⏳ Project Directory: {BASE_DIR}")
    print("⏳ Downloading NASA and OWID data...")
    
    # 1. Fetch Temperature Data
    url_temp = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    try:
        df = pd.read_csv(url_temp, skiprows=1, na_values='***')
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for col in months + ['Year']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['Temp_Avg'] = df[months].mean(axis=1)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    if not check_and_ask_user(df): return

    # 2. Fetch CO2 Data
    url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        df_co2 = pd.read_csv(url_co2)
        df_co2 = df_co2[df_co2['country'] == 'World'][['year', 'co2']]
        df_co2 = df_co2.rename(columns={'year': 'Year', 'co2': 'CO2'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    df_merged = pd.merge(df[['Year', 'Temp_Avg']], df_co2, on='Year')
    plt.style.use('seaborn-v0_8-whitegrid')
    print("✅ Generating 4 professional charts...")

    # --- Chart 1: CO2 vs Temperature ---
    fig, ax1 = plt.subplots(figsize=(12, 6))
    df_chart1 = df_merged[df_merged['Year'] >= 1950]
    correlation, _ = stats.pearsonr(df_chart1['CO2'], df_chart1['Temp_Avg'])
    ax1.plot(df_chart1['Year'], df_chart1['Temp_Avg'], color='#e74c3c', linewidth=3, label='Temp Anomaly')
    ax2 = ax1.twinx()
    ax2.plot(df_chart1['Year'], df_chart1['CO2'], color='#34495e', linewidth=2, linestyle='--', label='CO2')
    plt.title(f'1. The Driver: CO2 vs Temp (Correlation: {correlation:.2f})', fontweight='bold')
    plt.savefig(os.path.join(OUTPUT_DIR, '1_co2_temp.png'), dpi=300)
    plt.close()

    # --- Chart 2: Warming Stripes ---
    plt.figure(figsize=(14, 3))
    df_stripes = df[df['Year'] >= 1880]
    plt.bar(df_stripes['Year'], height=1, width=1.0, 
            color=plt.cm.RdBu_r((df_stripes['Temp_Avg'] - df_stripes['Temp_Avg'].min()) / 
                                (df_stripes['Temp_Avg'].max() - df_stripes['Temp_Avg'].min())))
    plt.title('2. Visual History (Warming Stripes 1880-2024)', fontweight='bold')
    plt.axis('off')
    plt.savefig(os.path.join(OUTPUT_DIR, '2_stripes.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # --- Chart 3: Seasonal Bars ---
    df_recent = df[df['Year'] >= (df['Year'].max() - 20)].copy()
    oct_increase = df_recent['Oct'].mean() - df[(df['Year'] >= 1950) & (df['Year'] <= 1980)]['Oct'].mean()
    avg_winter, avg_summer, avg_autumn = df_recent['Jan'].mean(), df_recent['Jul'].mean(), df_recent['Oct'].mean()
    
    df_recent[['Year', 'Jan', 'Apr', 'Jul', 'Oct']].set_index('Year').plot(kind='bar', figsize=(14, 7), width=0.85, 
                                                                         color=['#3498db', '#2ecc71', '#e67e22', '#9b59b6'])
    plt.title('3. Seasonal Anomalies: Is Winter Delayed?', fontweight='bold')
    plt.legend(['Jan (Winter)', 'Apr (Spring)', 'Jul (Summer)', 'Oct (Autumn)'], loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '3_seasonal_bars.png'), dpi=300)
    plt.close()

    # --- Chart 4: Heat Intensity Heatmap ---
    df_heat = df_recent.set_index('Year')[months]
    extreme_count = (df_heat > 1.0).sum().sum()
    percent_extreme = (extreme_count / df_heat.size) * 100
    plt.figure(figsize=(12, 7))
    sns.heatmap(df_heat.T, cmap='RdBu_r', center=0, cbar_kws={'label': 'Anomaly (°C)'})
    plt.title('4. Heat Intensity (Last 20 Years)', fontweight='bold')
    plt.savefig(os.path.join(OUTPUT_DIR, '4_heatmap.png'), dpi=300)
    plt.close()

    # Final HTML Generation (Based on your provided design)
    html_content = f"""
    <html>
    <head>
        <title>EcoPulse Climate Report</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: auto; padding: 20px; color: #333; }}
            h1 {{ border-bottom: 4px solid #e74c3c; padding-bottom: 10px; text-align: center; }}
            h2 {{ background: #f4f4f4; padding: 10px; border-left: 5px solid #3498db; margin-top: 40px; }}
            .box {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
            .stat-box {{ background: #eaf2f8; padding: 15px; border-left: 5px solid #2980b9; margin-top: 10px; }}
            .conclusion {{ background: #fcf3cf; padding: 20px; border: 2px solid #f1c40f; border-radius: 10px; margin-top: 50px; }}
            img {{ max-width: 100%; height: auto; display: block; margin: 10px auto; }}
        </style>
    </head>
    <body>
        <h1>🌍 EcoPulse Climate Analysis</h1>
        <h2>1. The Driver: CO2 & Temperature</h2>
        <div class="box">
            <img src="1_co2_temp.png">
            <div class="stat-box"><strong>📊 Statistical Proof:</strong> Correlation Coefficient (R) = <b>{correlation:.2f}</b>.</div>
            <p><strong>Analysis:</strong> This chart tells the story of the "Greenhouse Effect." As CO2 emissions rise (dashed line), they trap more solar heat, causing the global temperature (red line) to rise.</p>
        </div>
        <h2>2. Visual History (Warming Stripes)</h2>
        <div class="box">
            <img src="2_stripes.png">
            <p><strong>Explanation:</strong> Each stripe is a year (1880-2024). Red means warmer than baseline. The dark red on the right shows rapid warming.</p>
        </div>
        <h2>3. Seasonal Analysis (Autumn Focus)</h2>
        <div class="box">
            <img src="3_seasonal_bars.png">
            <div class="stat-box">
                <strong>📊 Insight on Autumn:</strong><br>
                October is <b>{oct_increase:.2f}°C warmer</b> on average compared to the historical baseline.<br><br>
                • Winter Average Anomaly: +{avg_winter:.2f}°C<br>
                • Summer Average Anomaly: +{avg_summer:.2f}°C<br>
                • Autumn Average Anomaly: +{avg_autumn:.2f}°C.
            </div>
        </div>
        <h2>4. Heat Intensity</h2>
        <div class="box">
            <img src="4_heatmap.png">
            <div class="stat-box">
                <strong>📊 Data Check:</strong> Out of {df_heat.size} months analyzed, <b>{extreme_count} months</b> exceeded +1.0°C.<br>
                That means {percent_extreme:.1f}% of the time, we live in extreme heat conditions.
            </div>
        </div>
        <div class="conclusion">
            <h3>🌱 General Ecological Recommendation</h3>
            <p>{get_general_recommendation()}</p>
        </div>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, 'Final_Report.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    with open(os.path.join(OUTPUT_DIR, 'last_run_info.txt'), 'w') as f:
        f.write(f"{df['Year'].max()}")
    print(f"✅ Full report generated: {os.path.join(OUTPUT_DIR, 'Final_Report.html')}")

if __name__ == "__main__":
    generate_interactive_report()
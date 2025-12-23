"""
🌍 ECO-PULSE: ULTIMATE CLIMATE REPORT
Automated Climate Analysis with Absolute Path Management.
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
        "🌱 <strong>Reduce Meat Consumption:</strong> The livestock industry is a major source of methane.",
        "💡 <strong>Energy Efficiency:</strong> Switch to LED bulbs to reduce your carbon footprint significantly.",
        "🚗 <strong>Sustainable Transport:</strong> Use public transportation instead of driving private vehicles.",
        "🗑️ <strong>Minimize Food Waste:</strong> Decomposing food in landfills produces methane.",
        "🌡️ <strong>Smart Heating/Cooling:</strong> Adjusting your thermostat by 1°C can reduce emissions by up to 10%."
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
    """Main execution flow for data processing and visualization."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"⏳ Project Directory: {BASE_DIR}")
    print("⏳ Downloading NASA and OWID data...")
    
    # 1. Temperature Data from NASA
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

    # 2. CO2 Data from Our World in Data
    url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        df_co2 = pd.read_csv(url_co2)
        df_co2 = df_co2[df_co2['country'] == 'World'][['year', 'co2']]
        df_co2 = df_co2.rename(columns={'year': 'Year', 'co2': 'CO2'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Merge and Visualize
    df_merged = pd.merge(df[['Year', 'Temp_Avg']], df_co2, on='Year')
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Chart 1: CO2 vs Temperature Correlation
    fig, ax1 = plt.subplots(figsize=(10, 5))
    df_chart1 = df_merged[df_merged['Year'] >= 1950]
    correlation, _ = stats.pearsonr(df_chart1['CO2'], df_chart1['Temp_Avg'])
    ax1.plot(df_chart1['Year'], df_chart1['Temp_Avg'], color='#e74c3c', linewidth=2, label='Temp')
    ax2 = ax1.twinx()
    ax2.plot(df_chart1['Year'], df_chart1['CO2'], color='#34495e', linestyle='--', label='CO2')
    plt.title(f"CO2 vs Temperature (Correlation: {correlation:.2f})")
    plt.savefig(os.path.join(OUTPUT_DIR, '1_co2_temp.png'))
    plt.close()

    # Final HTML Generation
    html_content = f"<html><body><h1>EcoPulse Climate Report</h1><img src='1_co2_temp.png'><p>{get_general_recommendation()}</p></body></html>"
    with open(os.path.join(OUTPUT_DIR, 'Final_Report.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    with open(os.path.join(OUTPUT_DIR, 'last_run_info.txt'), 'w') as f:
        f.write(f"{df['Year'].max()}")
    print(f"✅ Success! Files saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_interactive_report()
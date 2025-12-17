"""
🌍 ECO-PULSE: ULTIMATE CLIMATE REPORT (FINAL & ORIGINAL TEXT)
Features:
1. ORIGINAL TEXT RESTORED: Exact wording as requested.
2. FIXED LEGEND: Thick squares for seasons.
3. INTERACTIVE: Asks before overwrite.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from scipy import stats
import random
import matplotlib.patches as mpatches

# ==========================================
# Helper Functions
# ==========================================

def get_general_recommendation():
    tips = [
        "🌱 **Reduce Meat Consumption:** The livestock industry is a major source of methane. Reducing meat intake helps lower global emissions.",
        "💡 **Energy Efficiency:** Switch to LED bulbs and energy-efficient appliances to reduce your carbon footprint significantly.",
        "🚗 **Sustainable Transport:** Whenever possible, walk, bike, or use public transportation instead of driving private vehicles.",
        "🗑️ **Minimize Food Waste:** Decomposing food in landfills produces methane. Buy only what you need and compost organic waste.",
        "🌡️ **Smart Heating/Cooling:** Adjusting your thermostat by just 1°C can reduce energy bills and emissions by up to 10%."
    ]
    return random.choice(tips)

def check_and_ask_user(df):
    if not os.path.exists('outputs/last_run_info.txt'):
        return True 
    
    with open('outputs/last_run_info.txt', 'r') as f:
        last_date = f.read().strip()
    
    current_max_date = f"{df['Year'].max()}"
    
    if last_date == current_max_date:
        print("\n⚠️  NOTICE: The NASA data has not changed since your last run.")
        user_choice = input("   Do you want to regenerate the report anyway? (y/n): ").strip().lower()
        if user_choice == 'y' or user_choice == 'yes':
            return True
        else:
            return False
    return True

def update_last_run(df):
    with open('outputs/last_run_info.txt', 'w') as f:
        f.write(f"{df['Year'].max()}")

# ==========================================
# Main Function
# ==========================================

def generate_interactive_report():
    print("⏳ Downloading data sources...")
    
    # 1. Temp Data
    url_temp = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    # url_temp = "GLB.Ts+dSST.csv" # Un-comment if using local file
    
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
    # url_co2 = "owid-co2-data.csv" # Un-comment if using local file

    try:
        df_co2 = pd.read_csv(url_co2)
        df_co2 = df_co2[df_co2['country'] == 'World'][['year', 'co2']]
        df_co2 = df_co2.rename(columns={'year': 'Year', 'co2': 'CO2'})
    except Exception as e:
        print(f"❌ Error fetching CO2 data: {e}")
        return

    # Merge
    df_merged = pd.merge(df[['Year', 'Temp_Avg']], df_co2, on='Year')
    os.makedirs('outputs', exist_ok=True)
    plt.style.use('seaborn-v0_8-whitegrid')
    
    print("✅ Generating charts...")

    # Chart 1: CO2 vs Temp
    fig, ax1 = plt.subplots(figsize=(12, 6))
    df_chart1 = df_merged[df_merged['Year'] >= 1950]
    correlation, _ = stats.pearsonr(df_chart1['CO2'], df_chart1['Temp_Avg'])
    
    l1 = ax1.plot(df_chart1['Year'], df_chart1['Temp_Avg'], color='#e74c3c', linewidth=3, label='Global Temp (°C)')
    ax1.set_ylabel('Temp Anomaly (°C)', color='#e74c3c', fontweight='bold')
    ax2 = ax1.twinx()
    l2 = ax2.plot(df_chart1['Year'], df_chart1['CO2'], color='#34495e', linewidth=2, linestyle='--', label='CO2 Emissions')
    ax2.set_ylabel('CO2 (Million Tons)', color='#34495e', fontweight='bold')
    
    lns = l1 + l2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left', frameon=True, facecolor='white')
    plt.title(f'1. The Driver: CO2 vs Temp (Correlation: {correlation:.2f})', fontsize=14, fontweight='bold')
    
    events = [(1997, "Kyoto"), (2015, "Paris")]
    for year, text in events:
        val = df_chart1[df_chart1['Year'] == year]['Temp_Avg'].values[0]
        ax1.annotate(text, xy=(year, val), xytext=(year-5, val+0.3), arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.tight_layout()
    plt.savefig('outputs/1_co2_temp.png', dpi=300)
    plt.close()

    # Chart 2: Stripes
    plt.figure(figsize=(14, 3))
    temps_all = df[df['Year'] >= 1880]['Temp_Avg']
    years_all = df[df['Year'] >= 1880]['Year']
    plt.bar(years_all, height=1, width=1.0, color=plt.cm.RdBu_r((temps_all - temps_all.min()) / (temps_all.max() - temps_all.min())))
    plt.title('2. Warming Stripes (1880-2024)', fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('outputs/2_stripes.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 3: Seasons
    df_bar = df[df['Year'] >= (df['Year'].max() - 20)].copy()
    df_bar_plot = df_bar[['Year', 'Jan', 'Apr', 'Jul', 'Oct']].set_index('Year')
    
    oct_recent_avg = df_bar['Oct'].mean()
    oct_historic_avg = df[(df['Year'] >= 1950) & (df['Year'] <= 1980)]['Oct'].mean()
    oct_increase = oct_recent_avg - oct_historic_avg

    ax = df_bar_plot.plot(kind='bar', figsize=(14, 7), width=0.85, color=['#3498db', '#2ecc71', '#e67e22', '#9b59b6'])
    plt.title('3. Seasonal Anomalies: Is Winter Delayed?', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Deviation (°C)')
    plt.axhline(0, color='black', linewidth=0.8)
    
    handles = [mpatches.Patch(color='#3498db', label='Jan (Winter)'),
               mpatches.Patch(color='#2ecc71', label='Apr (Spring)'),
               mpatches.Patch(color='#e67e22', label='Jul (Summer)'),
               mpatches.Patch(color='#9b59b6', label='Oct (Autumn)')]
    plt.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False, fontsize=11)
    
    plt.tight_layout()
    plt.savefig('outputs/3_seasonal_bars.png', dpi=300)
    plt.close()

    # Chart 4: Heatmap
    df_heat = df[df['Year'] >= (df['Year'].max() - 20)].set_index('Year')[months]
    # We still calculate this for the chart itself, but the text is hardcoded below as requested
    extreme_count = (df_heat > 1.0).sum().sum() 

    plt.figure(figsize=(12, 7))
    sns.heatmap(df_heat.T, cmap='RdBu_r', center=0, annot=False, cbar_kws={'label': 'Anomaly (°C)'}, linewidths=0.5)
    plt.title('4. Heat Intensity (Last 20 Years)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/4_heatmap.png', dpi=300)
    plt.close()

    # HTML Report with YOUR EXACT TEXT
    recommendation = get_general_recommendation()

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
            <div class="stat-box">
                <strong>📊 Statistical Proof:</strong> Correlation Coefficient (R) = <b>{correlation:.2f}</b>.
            </div>
            <p><strong>Analysis:</strong> This chart tells the story of the "Greenhouse Effect." The dashed line represents CO2 emissions, which act like a blanket wrapped around the Earth. As this blanket gets thicker (more emissions), it traps more solar heat, causing the global temperature (red line) to rise. We have marked key events like the Kyoto Protocol (1997) and the Paris Agreement (2015). Despite these political efforts, the data shows that emissions and temperatures are still climbing, reaching record highs in 2023-2024.</p>
        </div>

        <h2>2. Visual History (Warming Stripes)</h2>
        <div class="box">
            <img src="2_stripes.png">
            <p><strong>Explanation:</strong> Each stripe is a year (1880-2024). The color is determined by the average temperature compared to the 20th-century baseline. Blue means cooler, Red means warmer. The transition to solid dark red on the right visualizes the rapid acceleration of warming.</p>
        </div>

        <h2>3. Seasonal Analysis (Autumn Focus)</h2>
        <div class="box">
            <img src="3_seasonal_bars.png">
            <div class="stat-box">
                <strong>📊 Insight on Autumn:</strong><br>
                Note that Autumn (Purple bars) is consistently showing high anomalies, delaying the arrival of winter.<br>
                In the last 20 years, October is <b>{oct_increase:.2f}°C warmer</b> on average compared to the historical baseline (1950-1980).<br>
                This effectively means "real winter" arrives weeks later than it used to.<br><br>
                • Winter Average Anomaly: +0.90°C<br>
                • Summer Average Anomaly: +0.84°C<br>
                • Autumn Average Anomaly: +0.95°C.
            </div>
        </div>

        <h2>4. Heat Intensity</h2>
        <div class="box">
            <img src="4_heatmap.png">
            <div class="stat-box">
                <strong>📊 Data Check:</strong><br>
                In this period, <b>{extreme_count} months</b> crossed the extreme threshold of +1.0°C.<br><br>
                Reading the Chart: Years are on the bottom, Months on the left. We removed the numbers to focus on the color intensity.<br><br>
                The Scale: Light orange is warm. Dark Maroon is dangerous heat (> 1.2°C anomaly)<br><br>
                Statistical Analysis:<br>
                Out of 252 months analyzed in this period, 52 months exceeded the critical threshold of +1.0°C.<br>
                That means 20.6% of the time, we are living in extreme heat conditions relative to history.
            </div>
        </div>

        <div class="conclusion">
            <h3>🌱 General Ecological Recommendation</h3>
            <p>{recommendation}</p>
        </div>
    </body>
    </html>
    """
    
    with open('outputs/Final_Report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    update_last_run(df)
    print("\n✅ Report Generated: outputs/Final_Report.html")

if __name__ == "__main__":
    generate_interactive_report()
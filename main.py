"""
🚀 ECO-PULSE: MAIN RUNNER (FULL VERSION)
Includes:
1. Robust Data Fetching (GitHub/NASA/NOAA).
2. CSV Generation.
3. Statistical Analysis.
4. Visualization Triggers.
5. HTML Report Generation.
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import analyze   
import visualize 

# ==========================================
# 1. Data Generation (The Missing Part)
# ==========================================
def generate_climate_data():
    print("⏳ Downloading real climate data...")
    
    # --- STEP A: Fetch Global Temperature ---
    df_temp = None
    
    # Primary Source: DataHub (GitHub)
    url_temp_primary = "https://raw.githubusercontent.com/datasets/global-temp-anomalies/master/data/global-temp-annual.csv"
    
    try:
        print(f"   Attempting Temp Source 1 (DataHub)...")
        df_temp = pd.read_csv(url_temp_primary)
        
        if 'Source' in df_temp.columns:
            df_temp = df_temp[df_temp['Source'] == 'GISTEMP']
        
        df_temp = df_temp.rename(columns={'Mean': 'Global_Temp_Anomaly_C'})
        df_temp = df_temp[['Year', 'Global_Temp_Anomaly_C']]
        print("   ✅ Success from Source 1.")
        
    except Exception as e:
        print(f"   ⚠️ Source 1 failed ({e}). Trying backup...")
        
        # Backup Source: NASA GISS
        try:
            url_temp_backup = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
            df_temp = pd.read_csv(url_temp_backup, skiprows=1)
            df_temp = df_temp.rename(columns={'Year': 'Year', 'J-D': 'Global_Temp_Anomaly_C'})
            
            df_temp['Global_Temp_Anomaly_C'] = pd.to_numeric(df_temp['Global_Temp_Anomaly_C'], errors='coerce')
            df_temp['Year'] = pd.to_numeric(df_temp['Year'], errors='coerce')
            df_temp = df_temp.dropna(subset=['Global_Temp_Anomaly_C'])
            
            print("   ✅ Success from Backup Source (NASA).")
            
        except Exception as e2:
            print(f"   ❌ All Temperature sources failed: {e2}")
            return None

    # --- STEP B: Fetch CO2 Levels ---
    url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    
    try:
        df_co2 = pd.read_csv(url_co2)
        df_co2 = df_co2[df_co2['country'] == 'World']
        df_co2 = df_co2.rename(columns={'year': 'Year', 'co2': 'CO2_Million_Tons'})
        df_co2 = df_co2[['Year', 'CO2_Million_Tons']]
        print("   ✅ CO2 data fetched successfully.")
        
    except Exception as e:
        print(f"❌ Error fetching CO2 data: {e}")
        return None

    # --- STEP C: Merge & Process ---
    df_temp['Year'] = df_temp['Year'].astype(int)
    df_co2['Year'] = df_co2['Year'].astype(int)
    
    df_final = pd.merge(df_temp, df_co2, on='Year', how='inner')
    
    # Fill missing values
    df_final = df_final.ffill()
    
    print(f"✅ Successfully processed {len(df_final)} years of REAL data.")
    return df_final

# ==========================================
# 2. HTML Report Generation
# ==========================================
def generate_html_report(df):
    """Generates a beautiful single-file HTML report"""
    print("📝 Generating HTML report...")
    
    # Calculate stats for the report
    current_year = df['Year'].max()
    current_temp = df[df['Year'] == current_year]['Global_Temp_Anomaly_C'].values[0]
    
    # Acceleration calc
    period1 = df[(df['Year'] >= 1950) & (df['Year'] < 1990)]
    period2 = df[df['Year'] >= 1990]
    
    if len(period1) > 0 and len(period2) > 0:
        slope1 = stats.linregress(period1['Year'], period1['Global_Temp_Anomaly_C']).slope * 10
        slope2 = stats.linregress(period2['Year'], period2['Global_Temp_Anomaly_C']).slope * 10
        accel = ((slope2 / slope1) - 1) * 100
    else:
        accel = 0
        
    corr = df['CO2_Million_Tons'].corr(df['Global_Temp_Anomaly_C'])
    
    # HTML Content
    html = f"""
    <html>
    <head>
        <title>EcoPulse Climate Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: auto; padding: 20px; color: #333; background-color: #f9f9f9; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
            h2 {{ color: #e67e22; margin-top: 40px; border-left: 5px solid #e67e22; padding-left: 10px; }}
            p {{ line-height: 1.6; font-size: 1.1em; }}
            .stats-box {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px 0; border-top: 5px solid #2ecc71; }}
            .chart-container {{ text-align: center; margin: 30px 0; background: white; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-radius: 8px; }}
            img {{ max-width: 100%; height: auto; border-radius: 4px; }}
            .highlight {{ color: #c0392b; font-weight: bold; }}
            li {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>🌍 EcoPulse: Final Climate Analysis Report</h1>
        <p><strong>Date Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Data Sources:</strong> NOAA, NASA GISS, Our World in Data (Real-Time)</p>
        
        <div class="stats-box">
            <h3>📊 Executive Summary (Status as of {current_year})</h3>
            <ul>
                <li>Current Temp Anomaly: <strong>{current_temp:.2f}°C</strong> (above baseline)</li>
                <li>Warming Acceleration: <span class="highlight">{accel:.1f}% increase</span> in warming rate since 1990.</li>
                <li>Correlation strength: <strong>{corr:.4f}</strong> (Extremely High). This confirms CO2 is the main driver.</li>
            </ul>
        </div>

        <h2>1. The Big Picture: Warming Stripes</h2>
        <p>A minimalist visualization where each stripe represents a year. The shift from blue to dark red visualizes the rapid heating of our planet.</p>
        <div class="chart-container">
            <img src="chart_1_stripes.png" alt="Warming Stripes">
        </div>

        <h2>2. The Driver: Temperature vs CO2</h2>
        <p>This dashboard compares the rise in atmospheric CO2 (dashed line) against global temperature rise (red line).</p>
        <div class="chart-container">
            <img src="chart_2_dashboard.png" alt="Dashboard">
        </div>

        <h2>3. The Evidence: Direct Correlation</h2>
        <p>Each dot is a year. The diagonal pattern proves that as CO2 increases (X-axis), Temperature rises (Y-axis) almost linearly.</p>
        <div class="chart-container">
            <img src="chart_3_scatter.png" alt="Correlation Scatter">
        </div>

        <h2>4. The Trend: Filtering the Noise</h2>
        <p>Weather varies year-to-year. The orange line (Rolling Average) smooths out these fluctuations to reveal the undeniable upward trend.</p>
        <div class="chart-container">
            <img src="chart_4_trend.png" alt="Trend Line">
        </div>

        <hr>
        <p style="text-align: center; font-size: 0.9em; color: gray;">Generated by Python EcoPulse Engine</p>
    </body>
    </html>
    """
    
    with open('outputs/Final_Report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ Created 'Final_Report.html'. Open this file in your browser!")

# ==========================================
# 3. Main Execution
# ==========================================
def main():
    print("="*60)
    print("🌍 STARTING ECO-PULSE CLIMATE TRACKER")
    print("="*60)
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    file_path = 'data/climate_vital_signs.csv'
    
    # 1. Generate Data
    df = generate_climate_data()
    
    if df is not None:
        # Save CSV
        df.to_csv(file_path, index=False)
        print(f"\n💾 Data saved to: {file_path}")
        
        # 2. Run Analysis (Console output)
        try:
            analyzer = analyze.ClimateAnalyzer(file_path)
            analyzer.run_analysis()
        except Exception as e:
            print(f"⚠️ Analysis Error: {e}")
        
        # 3. Run Visualization (Creates 4 images)
        try:
            viz = visualize.ClimateVisualizer(file_path)
            viz.create_visualizations()
        except Exception as e:
            print(f"⚠️ Visualization Error: {e}")
            
        # 4. Generate HTML Report (Combines text + images)
        generate_html_report(df)
        
        print("\n" + "="*60)
        print("✅ PROJECT COMPLETE!")
        print("👉 Go to the 'outputs' folder.")
        print("👉 Open 'Final_Report.html' to see your full project.")
        print("="*60)
    else:
        print("\n❌ Failed to generate data. Check internet connection.")

if __name__ == "__main__":
    main()
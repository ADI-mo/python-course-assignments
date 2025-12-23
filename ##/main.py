"""
🚀 ECO-PULSE: MAIN RUNNER (HISTORY PRESERVED)
Saves every run as a new file set using timestamps.
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import analyze   
import visualize 

# ==========================================
# 1. Data Generation
# ==========================================
def generate_climate_data():
    print("⏳ Downloading real climate data...")
    
    # --- Fetch Global Temperature ---
    df_temp = None
    url_temp_primary = "https://raw.githubusercontent.com/datasets/global-temp-anomalies/master/data/global-temp-annual.csv"
    
    try:
        df_temp = pd.read_csv(url_temp_primary)
        if 'Source' in df_temp.columns:
            df_temp = df_temp[df_temp['Source'] == 'GISTEMP']
        df_temp = df_temp.rename(columns={'Mean': 'Global_Temp_Anomaly_C'})
        df_temp = df_temp[['Year', 'Global_Temp_Anomaly_C']]
        
    except Exception:
        # Backup Source
        try:
            url_temp_backup = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
            df_temp = pd.read_csv(url_temp_backup, skiprows=1)
            df_temp = df_temp.rename(columns={'Year': 'Year', 'J-D': 'Global_Temp_Anomaly_C'})
            df_temp['Global_Temp_Anomaly_C'] = pd.to_numeric(df_temp['Global_Temp_Anomaly_C'], errors='coerce')
            df_temp['Year'] = pd.to_numeric(df_temp['Year'], errors='coerce')
            df_temp = df_temp.dropna(subset=['Global_Temp_Anomaly_C'])
        except Exception:
            return None

    # --- Fetch CO2 ---
    url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        df_co2 = pd.read_csv(url_co2)
        df_co2 = df_co2[df_co2['country'] == 'World']
        df_co2 = df_co2.rename(columns={'year': 'Year', 'co2': 'CO2_Million_Tons'})
        df_co2 = df_co2[['Year', 'CO2_Million_Tons']]
    except Exception:
        return None

    # --- Merge ---
    df_temp['Year'] = df_temp['Year'].astype(int)
    df_co2['Year'] = df_co2['Year'].astype(int)
    df_final = pd.merge(df_temp, df_co2, on='Year', how='inner')
    df_final = df_final.ffill()
    
    return df_final

# ==========================================
# 2. HTML Report Generation (With Timestamps)
# ==========================================
def generate_html_report(df, timestamp):
    """Generates an HTML report pointing to the specific timestamped images"""
    
    current_year = df['Year'].max()
    current_temp = df[df['Year'] == current_year]['Global_Temp_Anomaly_C'].values[0]
    
    # HTML Content - Note the image filenames include {timestamp}
    html = f"""
    <html>
    <head>
        <title>EcoPulse Report {timestamp}</title>
        <style>
            body {{ font-family: sans-serif; max-width: 900px; margin: auto; padding: 20px; background-color: #f9f9f9; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #e74c3c; }}
            .chart-container {{ text-align: center; margin: 30px 0; background: white; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-radius: 8px; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>🌍 EcoPulse Report</h1>
        <p><strong>Run ID:</strong> {timestamp}</p>
        <p><strong>Current Temp Anomaly:</strong> {current_temp:.2f}°C</p>

        <h2>1. Warming Stripes</h2>
        <div class="chart-container">
            <img src="chart_1_stripes_{timestamp}.png" alt="Warming Stripes">
        </div>

        <h2>2. Temperature vs CO2</h2>
        <div class="chart-container">
            <img src="chart_2_dashboard_{timestamp}.png" alt="Dashboard">
        </div>

        <h2>3. Correlation</h2>
        <div class="chart-container">
            <img src="chart_3_scatter_{timestamp}.png" alt="Scatter">
        </div>

        <h2>4. 10-Year Trend</h2>
        <div class="chart-container">
            <img src="chart_4_trend_{timestamp}.png" alt="Trend">
        </div>
    </body>
    </html>
    """
    
    report_name = f'outputs/Report_{timestamp}.html'
    with open(report_name, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Created report: {report_name}")

# ==========================================
# 3. Main Execution
# ==========================================
def main():
    # 1. יצירת חותמת זמן ייחודית לריצה זו (לדוגמה: 2025-12-15_22-45-12)
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    print("="*60)
    print(f"🌍 STARTING ECO-PULSE (Run ID: {run_timestamp})")
    print("="*60)
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # שמירת קובץ הנתונים עם השם הייחודי
    file_path = f'data/climate_data_{run_timestamp}.csv'
    
    df = generate_climate_data()
    
    if df is not None:
        df.to_csv(file_path, index=False)
        print(f"\n💾 Data saved to: {file_path}")
        
        try:
            analyzer = analyze.ClimateAnalyzer(file_path)
            analyzer.run_analysis()
        except Exception as e:
            print(f"⚠️ Analysis Error: {e}")
        
        try:
            # אנחנו מעבירים את חותמת הזמן לויזואליזטור
            viz = visualize.ClimateVisualizer(file_path, run_timestamp)
            viz.create_visualizations()
        except Exception as e:
            print(f"⚠️ Visualization Error: {e}")
            
        generate_html_report(df, run_timestamp)
        
        print("\n" + "="*60)
        print("✅ DONE! New files created in 'outputs' folder.")
        print(f"👉 Look for files ending in ...{run_timestamp}")
        print("="*60)
    else:
        print("\n❌ Failed to generate data.")

if __name__ == "__main__":
    main()
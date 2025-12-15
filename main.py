"""
🚀 ECO-PULSE: MAIN RUNNER (FINAL VERSION)
Features:
1. Real-time data fetching with Backup sources (NASA/NOAA/GitHub).
2. Automatic generation of CSV data.
3. Full statistical analysis.
4. Advanced visualization (Climate Stripes).
5. Text Report generation.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import analyze   
import visualize 

# ==========================================
# 1. Data Generation (With Backup Strategy)
# ==========================================
def generate_climate_data():
    print("⏳ Downloading real climate data...")
    
    # --- STEP A: Fetch Global Temperature ---
    df_temp = None
    
    # Primary Source: DataHub (GitHub) - Usually very stable
    url_temp_primary = "https://raw.githubusercontent.com/datasets/global-temp-anomalies/master/data/global-temp-annual.csv"
    
    try:
        print(f"   Attempting Temp Source 1 (DataHub)...")
        df_temp = pd.read_csv(url_temp_primary)
        
        # Filter for GISTEMP (NASA data) if 'Source' column exists
        if 'Source' in df_temp.columns:
            df_temp = df_temp[df_temp['Source'] == 'GISTEMP']
        
        df_temp = df_temp.rename(columns={'Mean': 'Global_Temp_Anomaly_C'})
        df_temp = df_temp[['Year', 'Global_Temp_Anomaly_C']]
        print("   ✅ Success from Source 1.")
        
    except Exception as e:
        print(f"   ⚠️ Source 1 failed ({e}). Trying backup...")
        
        # Backup Source: NASA GISS Direct
        try:
            url_temp_backup = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
            df_temp = pd.read_csv(url_temp_backup, skiprows=1) # Skip header rows
            df_temp = df_temp.rename(columns={'Year': 'Year', 'J-D': 'Global_Temp_Anomaly_C'})
            
            # Clean numeric data
            df_temp['Global_Temp_Anomaly_C'] = pd.to_numeric(df_temp['Global_Temp_Anomaly_C'], errors='coerce')
            df_temp['Year'] = pd.to_numeric(df_temp['Year'], errors='coerce')
            df_temp = df_temp.dropna(subset=['Global_Temp_Anomaly_C'])
            
            print("   ✅ Success from Backup Source (NASA).")
            
        except Exception as e2:
            print(f"   ❌ All Temperature sources failed: {e2}")
            return None

    # --- STEP B: Fetch CO2 Levels ---
    # Source: Our World in Data (GitHub)
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
    # Ensure Year is integer for merging
    df_temp['Year'] = df_temp['Year'].astype(int)
    df_co2['Year'] = df_co2['Year'].astype(int)
    
    df_final = pd.merge(df_temp, df_co2, on='Year', how='inner')
    
    # Calculate Extreme Weather Index (Simulated projection based on temp)
    if not df_final.empty:
        temp_factor = df_final['Global_Temp_Anomaly_C'] - df_final['Global_Temp_Anomaly_C'].min()
        df_final['Extreme_Weather_Index'] = (10 + np.exp(temp_factor * 1.5) * 5).astype(int)
    
    # Fill missing values forward
    df_final = df_final.ffill()
    
    print(f"✅ Successfully processed {len(df_final)} years of REAL data.")
    return df_final

# ==========================================
# 2. Report Generation Function
# ==========================================
def generate_text_report(df):
    """Generates a markdown report with key findings"""
    print("📝 Generating summary report...")
    
    try:
        # Latest Data
        current_year = df['Year'].max()
        current_temp = df[df['Year'] == current_year]['Global_Temp_Anomaly_C'].values[0]
        current_co2 = df[df['Year'] == current_year]['CO2_Million_Tons'].values[0]
        
        # Trend Analysis (Acceleration)
        period1 = df[(df['Year'] >= 1950) & (df['Year'] < 1990)]
        period2 = df[df['Year'] >= 1990]
        
        slope1 = stats.linregress(period1['Year'], period1['Global_Temp_Anomaly_C']).slope * 10
        slope2 = stats.linregress(period2['Year'], period2['Global_Temp_Anomaly_C']).slope * 10
        acceleration = ((slope2 / slope1) - 1) * 100
        
        correlation = df['CO2_Million_Tons'].corr(df['Global_Temp_Anomaly_C'])
        
        report_content = f"""
# 🌍 EcoPulse: Climate Analysis Report
**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Data Source:** NOAA, NASA GISS, Our World in Data

## 📊 Current Status ({current_year})
* **Global Temperature Anomaly:** {current_temp:.2f}°C (relative to baseline)
* **Annual CO2 Emissions:** {current_co2:,.0f} Million Tons

## 📈 Trend Analysis
* **Warming Rate (1950-1990):** {slope1:.3f}°C per decade
* **Warming Rate (1990-Present):** {slope2:.3f}°C per decade
* **Acceleration:** Warming has accelerated by **{acceleration:.1f}%** in recent decades.

## 🔗 Correlation
* **Correlation Coefficient:** {correlation:.4f} (CO2 vs Temp)
* **Interpretation:** Strong positive correlation confirms the link between emissions and warming.
        """
        
        output_path = 'outputs/Climate_Report.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Saved report to: {output_path}")
        
    except Exception as e:
        print(f"⚠️ Could not generate report: {e}")

# ==========================================
# 3. Main Execution
# ==========================================
def main():
    print("="*60)
    print("🌍 STARTING ECO-PULSE CLIMATE TRACKER")
    print("="*60)
    
    # Setup folders
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    file_path = 'data/climate_vital_signs.csv'
    
    # 1. Generate Data
    df = generate_climate_data()
    
    if df is not None:
        # Save CSV
        df.to_csv(file_path, index=False)
        print(f"\n💾 Data saved to: {file_path}")
        
        # 2. Run Analysis
        try:
            analyzer = analyze.ClimateAnalyzer(file_path)
            analyzer.run_analysis()
        except Exception as e:
            print(f"⚠️ Analysis Error: {e}")
        
        # 3. Run Visualization
        try:
            viz = visualize.ClimateVisualizer(file_path)
            viz.create_visualizations()
        except Exception as e:
            print(f"⚠️ Visualization Error: {e}")
            
        # 4. Generate Text Report
        generate_text_report(df)
        
        print("\n" + "="*60)
        print("✅ PROJECT COMPLETE! Check the 'outputs' folder.")
        print("="*60)
    else:
        print("\n❌ Failed to generate data. Check internet connection.")

if __name__ == "__main__":
    main()
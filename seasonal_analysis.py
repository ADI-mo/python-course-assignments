"""
❄️☀️ SEASONAL WARMING ANALYZER (CLEAN VERSION)
Fixed: Readable axis labels and cleaner charts.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os

def analyze_seasonality():
    print("⏳ Downloading monthly climate data from NASA...")
    
    url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    
    try:
        df = pd.read_csv(url, skiprows=1, na_values='***')
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df = df[['Year'] + months]
        
        # Clean data
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df[df['Year'] >= 1880]
        
        print("✅ Data fetched. Creating clean charts...")
        os.makedirs('outputs', exist_ok=True)

        # -------------------------------------------------------
        # 1. Heatmap (Fixed: Less crowded Axis)
        # -------------------------------------------------------
        df_heatmap = df.set_index('Year')
        
        plt.figure(figsize=(14, 8))
        
        # יצירת המפה
        ax = sns.heatmap(df_heatmap.T, cmap='RdBu_r', center=0, 
                         cbar_kws={'label': 'Temp Anomaly (°C)'})
        
        plt.title('Global Temperature Heatmap (1880-2024)', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Month', fontsize=12)
        
        # --- התיקון: דילול תוויות השנים (מציג רק כל 20 שנה) ---
        # אנחנו לוקחים את כל השנים, אבל מציגים טקסט רק עבור האינדקסים שמתחלקים ב-20
        xticks = np.arange(0, len(df_heatmap.index), 20)
        xticklabels = df_heatmap.index[::20]
        
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=0, fontsize=10)
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig('outputs/seasonal_heatmap.png', dpi=300)
        print("🔥 Saved cleaned heatmap: outputs/seasonal_heatmap.png")

        # -------------------------------------------------------
        # 2. New: Simple Line Chart (Winter vs Summer)
        # -------------------------------------------------------
        plt.figure(figsize=(12, 6))
        
        # החלקת הנתונים (ממוצע נע של 10 שנים) כדי לראות מגמה ברורה
        df['Jan_Smooth'] = df['Jan'].rolling(window=10).mean()
        df['Jul_Smooth'] = df['Jul'].rolling(window=10).mean()
        
        plt.plot(df['Year'], df['Jan_Smooth'], label='January (Winter)', color='#3498db', linewidth=2)
        plt.plot(df['Year'], df['Jul_Smooth'], label='July (Summer)', color='#e67e22', linewidth=2)
        
        plt.title('Winter vs. Summer Warming Trends (10-Year Average)', fontsize=14, fontweight='bold')
        plt.ylabel('Temp Anomaly (°C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/seasonal_lines.png', dpi=300)
        print("📊 Saved line comparison: outputs/seasonal_lines.png")
        
        print("\n✅ DONE! Charts are much easier to read now.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_seasonality()
"""
🎨 CLIMATE VISUALIZER (FINAL LEGEND FIX)
Forces Seaborn to disable auto-legends to prevent overlap.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ClimateVisualizer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        try:
            plt.style.use('seaborn-v0_8-dark') 
        except:
            plt.style.use('ggplot')
        
        os.makedirs('outputs', exist_ok=True)

    def plot_climate_stripes(self):
        """Generates the warming stripes art"""
        plt.figure(figsize=(14, 3))
        temps = self.df['Global_Temp_Anomaly_C']
        
        plt.bar(self.df['Year'], height=1, width=1.0, 
                color=plt.cm.RdBu_r((temps - temps.min()) / (temps.max() - temps.min())))
        
        plt.title('Global Warming Stripes (Real Data)', fontsize=16, fontweight='bold')
        plt.axis('off')
        
        plt.text(self.df['Year'].min(), -0.1, str(self.df['Year'].min()), fontsize=12)
        plt.text(self.df['Year'].max(), -0.1, str(self.df['Year'].max()), fontsize=12)
        
        plt.tight_layout()
        save_path = 'outputs/climate_stripes_art.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved chart: {save_path}")

    def plot_dashboard(self):
        """Generates the main dashboard with a clean, unified legend"""
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # --- Plot 1: Temperature (Left Axis) ---
        # השינוי החשוב: legend=False כדי למנוע כפילויות
        sns.lineplot(data=self.df, x='Year', y='Global_Temp_Anomaly_C', ax=ax1, 
                     color='#e74c3c', linewidth=2.5, label='Temp Anomaly (°C)', legend=False)
        
        ax1.set_ylabel('Global Temp Anomaly (°C)', color='#e74c3c', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor='#e74c3c')
        ax1.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax1.grid(True, alpha=0.3)
        
        # --- Plot 2: CO2 (Right Axis) ---
        ax2 = ax1.twinx()
        
        # מילוי השטח מתחת לגרף
        ax2.fill_between(self.df['Year'], self.df['CO2_Million_Tons'], color='#34495e', alpha=0.1)
        
        # השינוי החשוב: legend=False
        sns.lineplot(data=self.df, x='Year', y='CO2_Million_Tons', ax=ax2, 
                     color='#34495e', linewidth=2.5, linestyle='--', label='CO2 Emissions', legend=False)
        
        ax2.set_ylabel('Annual CO2 Emissions (Million Tons)', color='#34495e', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='#34495e')
        ax2.grid(False) # ביטול רשת כפולה כדי לא לבלבל
        
        plt.title('The Climate Pulse: Temperature vs. CO2 Emissions', fontsize=16, fontweight='bold', pad=20)
        
        # --- יצירת מקרא ידני מאוחד (Unified Legend) ---
        # אנחנו יוצרים "ידיות" (handles) מדומות כדי לשלוט בדיוק איך המקרא נראה
        from matplotlib.lines import Line2D
        custom_lines = [
            Line2D([0], [0], color='#e74c3c', lw=2.5),
            Line2D([0], [0], color='#34495e', lw=2.5, linestyle='--')
        ]
        
        ax1.legend(custom_lines, ['Temp Anomaly (°C)', 'CO2 Emissions'], 
                   loc='upper left', frameon=True, facecolor='white', framealpha=1, shadow=True, fontsize=10)
        
        plt.tight_layout()
        save_path = 'outputs/climate_dashboard.png'
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"✅ Saved chart: {save_path}")

    def create_visualizations(self):
        print("\n🎨 Generating Visualizations...")
        self.plot_climate_stripes()
        self.plot_dashboard()
"""
🎨 CLIMATE VISUALIZER (FINAL UPGRADE)
Generates multiple chart types with external legends for clarity.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ClimateVisualizer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        try:
            plt.style.use('seaborn-v0_8-whitegrid') # סגנון נקי יותר
        except:
            plt.style.use('ggplot')
        
        os.makedirs('outputs', exist_ok=True)

    def plot_climate_stripes(self):
        """Warming Stripes - The artistic view"""
        fig = plt.figure(figsize=(14, 3))
        temps = self.df['Global_Temp_Anomaly_C']
        
        plt.bar(self.df['Year'], height=1, width=1.0, 
                color=plt.cm.RdBu_r((temps - temps.min()) / (temps.max() - temps.min())))
        
        plt.title('Global Warming Stripes (1880-2024)', fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.text(self.df['Year'].min(), -0.1, str(self.df['Year'].min()), fontsize=12)
        plt.text(self.df['Year'].max(), -0.1, str(self.df['Year'].max()), fontsize=12)
        
        plt.tight_layout()
        plt.savefig('outputs/chart_1_stripes.png', dpi=300, bbox_inches='tight')
        plt.close()

    def plot_dashboard(self):
        """Main Dashboard - Temp vs CO2"""
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Temp (Left)
        sns.lineplot(data=self.df, x='Year', y='Global_Temp_Anomaly_C', ax=ax1, 
                     color='#e74c3c', linewidth=2, label='Temperature Anomaly', legend=False)
        ax1.set_ylabel('Temp Anomaly (°C)', color='#e74c3c', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor='#e74c3c')
        ax1.set_xlabel('Year', fontsize=12)
        
        # CO2 (Right)
        ax2 = ax1.twinx()
        sns.lineplot(data=self.df, x='Year', y='CO2_Million_Tons', ax=ax2, 
                     color='#2c3e50', linewidth=2, linestyle='--', label='CO2 Emissions', legend=False)
        ax2.fill_between(self.df['Year'], self.df['CO2_Million_Tons'], color='#2c3e50', alpha=0.1)
        ax2.set_ylabel('CO2 Emissions (Million Tons)', color='#2c3e50', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='#2c3e50')
        ax2.grid(False)

        plt.title('The Correlation: Temperature vs. CO2 Rise', fontsize=16, fontweight='bold', pad=20)
        
        # --- FIXED LEGEND (Placed OUTSIDE the chart) ---
        from matplotlib.lines import Line2D
        custom_lines = [
            Line2D([0], [0], color='#e74c3c', lw=2),
            Line2D([0], [0], color='#2c3e50', lw=2, linestyle='--')
        ]
        # bbox_to_anchor moves it outside/above
        ax1.legend(custom_lines, ['Temp Anomaly (°C)', 'CO2 Emissions'], 
                   loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False)
        
        plt.tight_layout()
        plt.savefig('outputs/chart_2_dashboard.png', dpi=300)
        plt.close()

    def plot_correlation_scatter(self):
        """NEW: Scatter plot showing direct correlation"""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='CO2_Million_Tons', y='Global_Temp_Anomaly_C', 
                        hue='Year', palette='rocket_r', s=100)
        
        plt.title('Direct Correlation: Higher CO2 = Higher Temp', fontsize=14, fontweight='bold')
        plt.xlabel('Annual CO2 Emissions (Million Tons)', fontsize=12)
        plt.ylabel('Global Temp Anomaly (°C)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/chart_3_scatter.png', dpi=300)
        plt.close()

    def plot_rolling_average(self):
        """NEW: 10-Year Rolling Average (Trend Line)"""
        plt.figure(figsize=(12, 5))
        
        # Original Data (Faint)
        plt.plot(self.df['Year'], self.df['Global_Temp_Anomaly_C'], color='lightgray', label='Annual Data', alpha=0.6)
        
        # Rolling Average (Bold)
        self.df['Rolling_Avg'] = self.df['Global_Temp_Anomaly_C'].rolling(window=10).mean()
        plt.plot(self.df['Year'], self.df['Rolling_Avg'], color='#d35400', linewidth=3, label='10-Year Trend Line')
        
        plt.title('Noise vs. Trend: 10-Year Rolling Average', fontsize=14, fontweight='bold')
        plt.ylabel('Temp Anomaly (°C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/chart_4_trend.png', dpi=300)
        plt.close()

    def create_visualizations(self):
        print("🎨 Generating 4 types of charts...")
        self.plot_climate_stripes()
        self.plot_dashboard()
        self.plot_correlation_scatter()
        self.plot_rolling_average()
        print("✅ Charts created in 'outputs/' folder.")
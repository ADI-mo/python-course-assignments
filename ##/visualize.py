"""
🎨 CLIMATE VISUALIZER (TIMESTAMP VERSION)
Saves files with a unique timestamp to prevent overwriting.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ClimateVisualizer:
    def __init__(self, data_path, timestamp):
        self.df = pd.read_csv(data_path)
        self.timestamp = timestamp  # שמירת הזמן שהתקבל
        
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            plt.style.use('ggplot')
        
        os.makedirs('outputs', exist_ok=True)

    def plot_climate_stripes(self):
        fig = plt.figure(figsize=(14, 3))
        temps = self.df['Global_Temp_Anomaly_C']
        
        plt.bar(self.df['Year'], height=1, width=1.0, 
                color=plt.cm.RdBu_r((temps - temps.min()) / (temps.max() - temps.min())))
        
        plt.title(f'Global Warming Stripes (1880-{self.df["Year"].max()})', fontsize=14, fontweight='bold')
        plt.axis('off')
        
        plt.tight_layout()
        # שמירה עם השם הייחודי
        filename = f'outputs/chart_1_stripes_{self.timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_dashboard(self):
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        sns.lineplot(data=self.df, x='Year', y='Global_Temp_Anomaly_C', ax=ax1, 
                     color='#e74c3c', linewidth=2, label='Temperature Anomaly', legend=False)
        ax1.set_ylabel('Temp Anomaly (°C)', color='#e74c3c', fontsize=12, fontweight='bold')
        
        ax2 = ax1.twinx()
        sns.lineplot(data=self.df, x='Year', y='CO2_Million_Tons', ax=ax2, 
                     color='#2c3e50', linewidth=2, linestyle='--', label='CO2 Emissions', legend=False)
        ax2.fill_between(self.df['Year'], self.df['CO2_Million_Tons'], color='#2c3e50', alpha=0.1)
        ax2.set_ylabel('CO2 Emissions', color='#2c3e50', fontsize=12, fontweight='bold')
        ax2.grid(False)

        plt.title('Temperature vs. CO2 Rise', fontsize=16, fontweight='bold', pad=20)
        
        # Legend setup
        from matplotlib.lines import Line2D
        custom_lines = [Line2D([0], [0], color='#e74c3c', lw=2),
                        Line2D([0], [0], color='#2c3e50', lw=2, linestyle='--')]
        ax1.legend(custom_lines, ['Temp Anomaly', 'CO2 Emissions'], 
                   loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False)
        
        plt.tight_layout()
        filename = f'outputs/chart_2_dashboard_{self.timestamp}.png'
        plt.savefig(filename, dpi=300)
        plt.close()

    def plot_correlation_scatter(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='CO2_Million_Tons', y='Global_Temp_Anomaly_C', 
                        hue='Year', palette='rocket_r', s=100)
        
        plt.title('Direct Correlation: Higher CO2 = Higher Temp', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        filename = f'outputs/chart_3_scatter_{self.timestamp}.png'
        plt.savefig(filename, dpi=300)
        plt.close()

    def plot_rolling_average(self):
        plt.figure(figsize=(12, 5))
        plt.plot(self.df['Year'], self.df['Global_Temp_Anomaly_C'], color='lightgray', alpha=0.6)
        
        self.df['Rolling_Avg'] = self.df['Global_Temp_Anomaly_C'].rolling(window=10).mean()
        plt.plot(self.df['Year'], self.df['Rolling_Avg'], color='#d35400', linewidth=3, label='10-Year Trend')
        
        plt.title('10-Year Rolling Average Trend', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        filename = f'outputs/chart_4_trend_{self.timestamp}.png'
        plt.savefig(filename, dpi=300)
        plt.close()

    def create_visualizations(self):
        print(f"🎨 Generating charts with ID: {self.timestamp}")
        self.plot_climate_stripes()
        self.plot_dashboard()
        self.plot_correlation_scatter()
        self.plot_rolling_average()
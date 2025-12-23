"""
🔍 CLIMATE ANALYZER
Performs statistical analysis on real-world climate data.
"""
import pandas as pd
from scipy import stats

class ClimateAnalyzer:
    def __init__(self, data_path):
        # טעינת קובץ ה-CSV שהוכן על ידי main.py
        self.df = pd.read_csv(data_path)
        
    def calculate_warming_acceleration(self):
        """
        מחשב האם קצב ההתחממות האיץ בשנים האחרונות.
        משווה את השיפוע (Slope) של השנים 1950-1990 לעומת 1990-היום.
        """
        print("\n🔥 Real Warming Acceleration Analysis:")
        
        # חלוקה לשתי תקופות זמן
        period1 = self.df[(self.df['Year'] >= 1950) & (self.df['Year'] < 1990)]
        period2 = self.df[self.df['Year'] >= 1990]
        
        # ביצוע רגרסיה ליניארית לחישוב השיפוע (קצב ההתחממות)
        if len(period1) > 0 and len(period2) > 0:
            slope1 = stats.linregress(period1['Year'], period1['Global_Temp_Anomaly_C']).slope
            slope2 = stats.linregress(period2['Year'], period2['Global_Temp_Anomaly_C']).slope
            
            print(f"   Warming Rate (1950-1990): {slope1*10:.3f}°C per decade")
            print(f"   Warming Rate (1990-Today): {slope2*10:.3f}°C per decade")
            
            # חישוב אחוז השינוי
            if slope1 != 0:
                increase = ((slope2 / slope1) - 1) * 100
                print(f"   🚨 CONCLUSION: Warming has accelerated by {increase:.1f}% in recent decades.")
        else:
            print("   ⚠️ Not enough data for acceleration analysis.")

    def analyze_co2_temp_correlation(self):
        """
        בודק את הקורלציה (הקשר הסטטיסטי) בין פליטות פחמן לטמפרטורה.
        """
        print("\n🔗 Correlation Analysis (Real Data):")
        
        # חישוב מקדם הקורלציה של פירסון
        corr = self.df['CO2_Million_Tons'].corr(self.df['Global_Temp_Anomaly_C'])
        
        print(f"   Correlation (CO2 vs Temp): {corr:.4f}")
        if corr > 0.9:
            print("   (Result: Extremely strong positive relationship)")
        elif corr > 0.7:
            print("   (Result: Strong positive relationship)")

    def run_analysis(self):
        """מריץ את כל הבדיקות"""
        print("-" * 50)
        self.calculate_warming_acceleration()
        self.analyze_co2_temp_correlation()
        print("-" * 50)

# למקרה שמריצים את הקובץ לבד לבדיקה
if __name__ == "__main__":
    # מניח שהקובץ קיים בתיקיית data
    try:
        analyzer = ClimateAnalyzer('data/climate_vital_signs.csv')
        analyzer.run_analysis()
    except FileNotFoundError:
        print("❌ Data file not found. Run main.py first.")
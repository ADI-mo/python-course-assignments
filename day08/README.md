<<<<<<< HEAD


# 🌍 EcoPulse: Ultimate Climate Analysis

**EcoPulse** is an automated tool for analyzing global climate data. The project fetches real-time data from **NASA** and **Our World in Data** to generate an interactive report exploring the relationship between carbon emissions, global warming trends, seasonal variability, and extreme climate events.

---

## 🚀 Key Features

* **Full Automation:** Automatic data download, processing, and visualization with a single command.
* **Smart Interface:** The script checks if data has changed since the last run to save computing resources.
* **Dynamic HTML Report:** Generates a styled report containing interactive graphs and real-time statistical analysis (correlations, seasonal averages, anomaly percentages).
* **Absolute Path Management:** Results are strictly saved within the `outputs/` folder relative to the script's location.
* **Rotating Ecological Tips:** Each run includes a randomly selected eco-friendly recommendation to promote awareness.

---

## 🛠️ Prerequisites & Installation

To run the project, ensure **Python 3.x** is installed.

Install the required libraries using the terminal:

```bash
pip install pandas matplotlib seaborn scipy numpy pytest

```

---

## ▶️ How to Run

1. Ensure the file `seasonal_analysis.py` is located in your working directory (e.g., `day08/`).
2. Open a terminal in that directory.
3. Run the following command:

```bash
python seasonal_analysis.py

```

After execution, an `outputs/` folder will be created containing the final report: `Final_Report.html`.

---

## 🧪 Testing

To verify code integrity, calculation logic, and path accuracy, run the following command:

```bash
pytest test_seasonal.py

```

---

## 🤖 AI-Assisted Development

This project followed an iterative feedback-driven workflow between the user and Generative AI.

### User-Guided Enhancements

* **Absolute Path Fix:** Refactored the code to ensure results are saved within the project folder regardless of the terminal's starting point.
* **Seasonal Focus:** Shifted analysis to the most recent 20–30 years with a full comparison across all four seasons.
* **Dynamic Calculations:** All numerical values in the report (e.g., autumn warming averages, extreme-month percentages) are calculated in real-time.
* **Visualization Refinement:** Implemented custom legends and scientific explanations directly into the HTML report.

---

🌱 **EcoPulse** demonstrates how thoughtful human guidance combined with AI-assisted development can produce a robust and insightful climate analysis tool.

---

### 💡 Quick Explanation of the Code Structure

* **`seasonal_analysis.py`**: The main engine. It uses `os.path.abspath(__file__)` to find its own location on your computer, ensuring the `outputs/` folder is always created in the right place. It merges temperature data (NASA) with CO2 data (OWID) using a common `Year` key to calculate scientific correlations.
* **`test_seasonal.py`**: A safety net that uses `pytest` to confirm that the code's paths and logic haven't been broken during updates.

Would you like me to generate a `requirements.txt` file to bundle all these dependencies for easy sharing?
=======


---

# 🌍 EcoPulse: Ultimate Climate Analysis

**EcoPulse** is an automated tool designed to fetch real-time climate data from **NASA** and **Our World in Data**. It analyzes global warming trends, carbon emissions, and seasonal shifts, generating a professional, dynamic HTML report.

---

## 🚀 Key Features

* **Full Automation:** Downloads, processes, and visualizes climate data with a single command.
* **Absolute Path Management:** Uses smart path detection (`BASE_DIR`) to ensure all results are saved strictly within the project's `outputs/` folder, regardless of where the script is executed.
* **Dynamic Reporting:** Calculates real-time statistical correlations () and extreme heat percentages based on the latest available data.
* **Timestamped Analysis:** Every report includes a "Report generated on" timestamp to track when the analysis was performed.
* **Smart Interaction:** The script checks if data has changed since the last run to save time and computing resources.

---

## 🛠️ Prerequisites & Installation

To run the project, ensure **Python 3.x** is installed.

Install the required libraries using the terminal:

```bash
pip install pandas matplotlib seaborn scipy numpy pytest

```

---

## ▶️ How to Run

1. Ensure `seasonal_analysis.py` and `test_seasonal.py` are in your project directory (e.g., `day08/`).
2. Open a terminal in that directory.
3. Run the following command:

```bash
python seasonal_analysis.py

```

After execution, all charts and the `Final_Report.html` will be available in the **`outputs/`** folder.

---

## 🧪 Testing

To verify the project's integrity, including path accuracy and HTML formatting logic, run the testing suite:

```bash
pytest test_seasonal.py

```

---

## 🤖 AI-Assisted Development

This project was developed through an iterative, human-guided workflow with **Generative AI**. Key enhancements include refactoring for standalone script stability, implementing bold scientific explanations, and fixing visualization bugs like custom legend handles.

---

🌱 **EcoPulse** bridges the gap between raw scientific data and actionable environmental awareness.

---




>>>>>>> 523047f2bd684c57d7b442fc63b1da6a1d448e23

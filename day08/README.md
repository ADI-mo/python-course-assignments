

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





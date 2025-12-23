# 🌍 EcoPulse: Ultimate Climate Analysis

**EcoPulse** is an automated tool for analyzing global climate data.
The project fetches real-time data from **NASA** and **Our World in Data**, then generates an interactive report that explores the relationship between carbon emissions, global warming trends, seasonal variability, and extreme climate events.

---

## 🚀 Key Features

* **Full Automation**
  Automatic data download, processing, and visualization with a single command.

* **Smart Interface**
  The script checks whether the data has changed since the last run.
  If no changes are detected, it prompts the user to decide whether to continue — saving time and computing resources.

* **Dynamic HTML Report**
  Generates a styled HTML report containing:

  * Interactive graphs
  * Real-time statistical analysis (correlations, seasonal averages, anomaly percentages)

* **Rotating Ecological Tips**
  Each run includes a randomly selected eco-friendly recommendation to promote environmental awareness.

---

## 🛠️ Prerequisites

To run the project, make sure **Python 3.x** is installed.

Install the required libraries using the terminal:

```bash
pip install pandas matplotlib seaborn scipy numpy
```

---

## ▶️ How to Run

1. Ensure the file `seasonal_analysis.py` is located in your working directory.
2. Open a terminal in that directory.
3. Run the following command:

```bash
python seasonal_analysis.py
```

After execution, an `outputs` folder will be created containing the final report:

```
Final_Report.html
```

---

## 🤖 AI-Assisted Development & Collaboration

This project was designed and developed with the assistance of **Generative AI**, following an iterative feedback-driven workflow between the user and the AI.

### User-Guided Enhancements

Throughout development, the user directed several critical improvements that significantly increased the project’s professionalism and accuracy:

* **Standalone Script**
  Refactored from a multi-file structure into a single self-contained script to avoid import issues.

* **Seasonal Focus**
  Shifted the analysis to the most recent **20–30 years**, with a full comparison across all **four seasons** (instead of only summer vs. winter).

* **Legend Fix (Visualization Bug)**
  The user identified a visual bug in the seasonal graph and requested:

  * Custom legend handles
  * January displayed as a bold square marker
  * Legend repositioned to the bottom of the chart

* **Dynamic Calculations**
  All numerical values in the report (e.g., autumn warming averages, extreme-month percentages) are calculated in real time — no hardcoded text.

* **Interactive Workflow**
  Added a user prompt (`y/n`) to confirm re-running the analysis if the data has not changed.

* **Text Accuracy & Clarity**
  Embedded precise scientific explanations (e.g., greenhouse effect, delayed winters) directly into the HTML report, using proper formatting (`<strong>` tags).

* **Rotating Recommendations**
  Implemented a bank of ecological tips, randomly selected on each run to keep the report fresh and engaging.

---

🌱 **EcoPulse** demonstrates how thoughtful human guidance combined with AI-assisted development can produce a robust, insightful, and user-friendly climate analysis tool.

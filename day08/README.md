# 🌍 EcoPulse: Ultimate Climate Analysis

[cite_start]**EcoPulse** is an automated tool that fetches real-time data from **NASA** and **Our World in Data** to analyze global warming trends.

## 🚀 Key Features
* [cite_start]**Full Automation:** Fetches, processes, and visualizes climate data in one click.
* [cite_start]**Smart Interaction:** Prompts user if data hasn't changed to save resources.
* [cite_start]**Dynamic Reporting:** Calculates correlations and seasonal anomalies in real-time.
* **Absolute Path Management:** Results are strictly saved within the `outputs/` project folder.

## 🛠️ Prerequisites
Install required Python libraries:
```bash
pip install pandas matplotlib seaborn scipy numpy pytest
▶️ Execution
Open a terminal in the project directory.

Run: python seasonal_analysis.py.

Check the outputs/ folder for Final_Report.html.

🧪 Testing
To verify code integrity and path accuracy, run:

Bash

pytest test_seasonal.py

---

### 3. The Testing Suite: `test_seasonal.py`
This file ensures the script remains stable and accurate.

```python
"""
🧪 UNIT TESTS FOR ECO-PULSE
Validates paths, logic, and output integrity.
"""
import os
import pytest
from seasonal_analysis import OUTPUT_DIR, get_general_recommendation

def test_path_configuration():
    """Ensures the output directory is correctly linked to the project root."""
    assert os.path.isabs(OUTPUT_DIR)
    assert "outputs" in OUTPUT_DIR

def test_recommendation_logic():
    """Checks if the random tip generator returns valid HTML-ready strings."""
    tip = get_general_recommendation()
    assert isinstance(tip, str)
    assert "<strong>" in tip

def test_directory_creation():
    """Verifies that the script can create the outputs folder if missing."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    assert os.path.exists(OUTPUT_DIR)
💡 Understanding the Code
Path Management (os.path): The script uses os.path.abspath(__file__) to find exactly where it is stored on your computer. This prevents files from being saved in the wrong location if you run the code from a different folder.


Data Integration: It merges two different datasets (NASA for heat and OWID for emissions) using a common Year key to calculate scientific correlations.


Resource Efficiency: It writes a small text file (last_run_info.txt) to remember the last data update, preventing unnecessary downloads and chart generation.

Safety (Testing): The pytest script acts as a safety net. It allows you to change the code in the future and instantly verify that you haven't broken the core paths or logic.
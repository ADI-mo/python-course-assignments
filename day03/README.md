


# 🧪 Modular Growth Rate Calculator (Python, SciPy, Matplotlib)

This is a **modular Python project** designed to calculate and analyze the **specific growth rate ($k$)** of biological populations (e.g., bacteria, cells) using **time-concentration (Time-Series) data**.

---

## ✨ Key Features

* **Single-Point Calculation ($k$)**: Basic method based on $N_0$ and $N_t$.
* **Multi-Point Fit**: Uses **linear regression** (SciPy) for accurate growth curve analysis across multiple data points.
* **Graphical Interface (GUI)**: Load data, plot graphs (Matplotlib), and display results in a user-friendly window.
* **File Loading**: Ability to load data directly from CSV or TXT files.

---

## 📈 Linear Regression Principle

**Linear Regression** is a statistical tool used to find the line of best fit for a set of data points. In this project, we use it to calculate the growth rate ($k$) reliably, even when noise is present in lab data.

### Logarithmic Transformation

Cell growth is an exponential process. To transform it into a linear process, we apply a logarithmic transformation (base 2):

[
$\log_2(N) = \log_2(N_0) + k \cdot t$
]

* $\log_2(N)$ is the vertical axis
* $t$ is the horizontal axis

### Finding the Slope

After transformation, the data points form a straight line. **SciPy's linear regression** finds the slope:

[
\text{Slope} = k
]

The slope ($k$) is the specific growth rate per unit of time, representing the number of doublings (Generations) per unit time.

### $R^2$ Metric

The **Coefficient of Determination ($R^2$)** shows how well the straight line fits the $\log_2$ data.

* $R^2$ ranges between 0 and 1
* Values closer to 1.0 indicate a better fit for the exponential growth phase

> ⚠️ **Important Usage Note:**
> Only input data corresponding to the **exponential growth phase** to get an accurate $k$. Use $R^2$ as a guide for selecting correct points.

---

## 🏗️ Project Structure

The business logic is completely separated from the interface, ensuring stability and ease of testing.

| File                       | Role                                                                                   | Key Libraries           |
| -------------------------- | -------------------------------------------------------------------------------------- | ----------------------- |
| `calculator_logic.py`      | Business Logic. Contains the calculation functions `growth_rate` and `growth_rate_fit` | `numpy`, `scipy.stats`  |
| `growth_rateGUI.py`        | Main Application (GUI)                                                                 | `tkinter`, `matplotlib` |
| `test_calculator_logic.py` | Unit Tests. Comprehensive testing of all calculation functions                         | `pytest`, `numpy`       |

---

## 🛠️ Installation & Running

### 📥 Requirements

* Python 3

### Installing Dependencies

```bash
pip install scipy matplotlib pytest numpy
```

### 🚀 Running the Application (GUI)

```bash
python growth_rateGUI.py
```

**Usage:**

* Enter multiple time and concentration points **or** use the **"Load Data from File"** button.
* Click **"Calculate & Plot Growth Rate (k)"** to get fitted results and a graph.

---

## 📁 File Format for Data Loading

When loading data from a file, the file must meet the following conditions:

* **Format:** `.txt` or `.csv`
* **Two-Column Structure:**

  1. Time ($t$) ≥ 0
  2. Concentration ($N$) > 0
* **Delimiter:** Columns can be separated by commas `,`, tabs, or spaces
* **Comments:** Lines starting with `#` or empty lines are ignored

**Example File Content:**

```
# Time (Hours), Concentration (OD)
0, 0.1
1.5, 0.25
3.0, 0.5
4.5, 1.05
6.0, 2.0
```

---

## ✅ Running Tests

To verify the integrity of the calculation logic:

```bash
pytest test_calculator_logic.py
```

---

## 🤖 AI Usage and Debugging Documentation

| Step | Prompt Provided to AI             | Purpose                                                                                                           |
| ---- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1    | Enhance `calculator_logic.py`     | Add `growth_rate_fit` using multiple time and concentration points. Integrates SciPy for multi-point calculation. |
| 2    | Create `test_calculator_logic.py` | Write comprehensive unit tests for both `growth_rate` and `growth_rate_fit`. Ensure edge cases are handled.       |
| 3    | Update `growth_rateGUI.py`        | Allow multi-point input, call `growth_rate_fit`, and embed Matplotlib plot in the GUI.                            |
| 4    | Update `README.md`                | Document file structure, SciPy/Matplotlib usage, installation steps, running GUI/tests, and AI prompts used.      |
| 5    | Add file loading to GUI           | Users can now load CSV/TXT data directly.                                                                         |
| 6    | Document linear regression usage  | Explain why only exponential growth phase data should be used.                                                    |

### Post-Development Debugging (Critical Fix)

**Issue:**

* `test_growth_rate_fit_stagnant_data_k0` failed because stagnant data (no change in concentration) caused SciPy to calculate $R^2 = \text{NaN}$ due to division by zero.

**Fix:**

* Added logical check inside `growth_rate_fit` for zero variance.
* Returns `k=0.0` and `R^2=1.0` for stagnant data, resolving the statistical error and making the test pass.

--


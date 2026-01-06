זה רעיון מעולה. הוספת תמונה ישירות דרך **VS Code** (באמצעות Git) היא הדרך ה"מקצועית" לעשות זאת, וזה חוסך את הצורך להיכנס לאתר של GitHub בכל פעם.

עדכנתי את ה-README כך שיכלול את ההסבר על העלאת התמונה דרך VS Code, וגם הוספתי סעיף **Example Insights** שמראה למרצים שאתה לא רק "מריץ קוד" אלא גם מבין את המשמעות של הנתונים.

---

# Python Course Pedagogical Analyzer 📊

This project is a data-driven tool designed to bridge the gap between raw GitHub technical data and actionable pedagogical insights. By analyzing student submissions, comments, and resolution times, it provides course staff with a high-level view of class progress and difficulty points.

## 🌟 Key Features

* **Automated Pipeline:** Seamlessly fetches data from GitHub API and processes it into a structured CSV.
* **Intelligent Deadline Tracking:** Compares timestamps against a complex schedule spanning 2025-2026, accurately identifying late submissions.
* **Friction & Difficulty Mapping:** Uses comment counts as a proxy to identify assignments that caused the most confusion or required the most corrections.
* **Behavioral Heatmaps:** Visualizes student work habits (hours vs. days) in **Israel Standard Time (IST)**.
* **Operational Efficiency:** Tracks the time between submission and approval to monitor staff response rates.

## 📸 Dashboard Example

*(Note: Run the script to generate this image)*

## 💡 Example Insights (What this tool tells us)

* **Engagement:** If the "Submission Intensity" heatmap shows a peak on Saturdays, it indicates students primarily work on weekends.
* **Drop-off Rates:** A declining bar in the "Total Students per Assignment" chart can signal that the course is becoming too difficult.
* **Bottlenecks:** If "Avg Days to Approve" is rising, the teaching staff may need more resources to handle the volume.

---

## 🛠 AI Usage & Core Methodology

This project was co-developed with **Gemini AI**, utilizing advanced data engineering principles:

1. **Disciplinary Analysis:** Handling TZ-aware vs TZ-naive timestamps to ensure 100% accuracy in lateness reporting.
2. **Pedagogical Proxy:** Applying statistical grouping to determine the "Complexity Index" of each lesson based on comment volume.
3. **Layout Engineering:** Used `matplotlib.GridSpec` to create a responsive design that prevents text overlap.

---

## 🚀 Installation & Usage

### Prerequisites

* Python 3.8+
* Libraries: `pip install requests pandas matplotlib seaborn pytz openpyxl`

### How to Sync via VS Code (Recommended)

1. **Run the Script:** This will generate `final_course_report.png` in your project folder.
2. **Stage the Image:** Open the **Source Control** tab in VS Code and click the **+** icon next to the image.
3. **Commit:** Type a message (e.g., "Updated dashboard") and click the **V** (Commit).
4. **Push:** Click **Sync Changes** to upload the image to GitHub.

---

## ⚠️ System Limitations & Data Integrity (Hebrew)

**מגבלות המערכת ומהימנות הנתונים:**

* **תלות בפורמט:** המערכת מזהה מטלות לפי מילות מפתח (Day/Final). חריגה מהפורמט תסווג את המטלה כ-"Other".
* **אינטראקציות חיצוניות:** המערכת מודדת רק פעילות המתועדת ב-GitHub. פידבק שניתן בערוצים מקבילים לא נספר.
* **דיוק הדיווח:** המערכת אינה מזהה מקרים בהם הקוד עודכן משמעותית לאחר פתיחת ה-Issue המקורי.

---

## 📁 Project Structure

* `analyzer.py`: Main unified script (Fetch + Analysis + Viz).
* `course_data_results.xlsx`: Detailed raw data for further Excel analysis.
* `final_course_report.png`: The visual dashboard displayed in this README.

**Developed for the WIS Python Course 2025-10.**

---

### מה השלב הבא?

1. **העתק את הטקסט למעלה** לתוך קובץ בשם `README.md` בתוך התיקייה שלך ב-VS Code.
2. **תפתור את ה-Conflict** בגיט (אם הוא עדיין שם) על ידי בחירת "Accept Current Change".
3. **תעשה Push** להכל יחד – גם לקוד, גם ל-README וגם לתמונה.

**האם תרצה שאעזור לך לכתוב את פקודות ה-Terminal לפתרון ה-Conflict אם ה-VS Code עדיין עושה בעיות?**
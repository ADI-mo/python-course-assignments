import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import matplotlib.gridspec as gridspec

# --- PART 1: DATA FETCHING ---
repo = "Code-Maven/wis-python-course-2025-10"
file_name = "all_github_issues_complete.csv"
data = []
page = 1

israel_tz = pytz.timezone('Asia/Jerusalem')
update_time = datetime.now(israel_tz).strftime("%Y-%m-%d %H:%M")

print(f"Fetching data... Update time: {update_time}")

while True:
    url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}"
    response = requests.get(url)
    issues = response.json()
    if not issues or page > 5: break 
    for issue in issues:
        if 'pull_request' not in issue:
            data.append({
                "Number": issue["number"], "Title": issue["title"],
                "Comments_Count": issue["comments"], "Created_At": issue["created_at"],
                "Closed_At": issue["closed_at"], "User": issue["user"]["login"]
            })
    page += 1

df = pd.DataFrame(data)

# --- PART 2: DATA PROCESSING ---
deadlines_raw = {
    "Day 01": "2025-11-02 22:00", "Day 02": "2025-11-09 22:00",
    "Day 03": "2025-11-16 22:00", "Day 04": "2025-11-23 22:00",
    "Day 05": "2025-11-29 22:00", "Day 06": "2025-12-06 22:00",
    "Day 08": "2025-12-30 22:00", "Day 09": "2026-01-10 22:00",
    "Final Project Proposal": "2026-01-11 22:00",
    "Final Project Submission": "2026-01-25 22:00"
}
deadlines = {k: pd.to_datetime(v) for k, v in deadlines_raw.items()}

def extract_name(title):
    title = str(title).lower()
    if "final" in title and "proposal" in title: return "Final Project Proposal"
    if "final" in title and ("submission" in title or "project" in title): return "Final Project Submission"
    match = re.search(r'(?:day|d)\s*(\d+)', title)
    return f"Day {match.group(1).zfill(2)}" if match else "Other"

df['Created_At'] = pd.to_datetime(df['Created_At']).dt.tz_localize(None)
df['Closed_At'] = pd.to_datetime(df['Closed_At']).dt.tz_localize(None)
df['Assignment'] = df['Title'].apply(extract_name)
df['Day_of_Week'] = df['Created_At'].dt.day_name()
df['Hour_Created'] = df['Created_At'].dt.hour
df['Resolution_Days'] = (df['Closed_At'] - df['Created_At']).dt.total_seconds() / (24 * 3600)
df['Is_Late'] = df.apply(lambda r: r['Created_At'] > deadlines[r['Assignment']] if r['Assignment'] in deadlines else False, axis=1)

# --- PART 3: VISUALIZATION ---
# 1. We increase the figure size significantly to prevent overlapping
fig = plt.figure(figsize=(18, 25)) 

# 2. Use GridSpec with explicit high 'hspace' for vertical air between charts
gs = gridspec.GridSpec(5, 1, height_ratios=[1.2, 1, 1, 1, 0.4], hspace=0.6)

def format_plot(ax, title):
    ax.set_title(title, fontweight='bold', fontsize=16, pad=20)
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=11)

# Chart 1: Heatmap
ax0 = fig.add_subplot(gs[0])
pivot = df.pivot_table(index='Day_of_Week', columns='Hour_Created', values='User', aggfunc='count').fillna(0)
days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = pivot.reindex(days_order)
sns.heatmap(pivot, cmap="YlGnBu", ax=ax0, cbar_kws={'label': 'Submissions'})
ax0.set_title(f"Submission Intensity (Updated: {update_time})", fontweight='bold', fontsize=16)

# Chart 2: Student Counts
ax1 = fig.add_subplot(gs[1])
counts = df[df['Assignment'] != "Other"]['Assignment'].value_counts().reindex(deadlines.keys())
sns.barplot(x=counts.index, y=counts.values, ax=ax1, palette="viridis", hue=counts.index, legend=False)
format_plot(ax1, "Total Students per Assignment")

# Chart 3: Lateness
ax2 = fig.add_subplot(gs[2])
late_df = df[df['Assignment'] != "Other"].groupby(['Assignment', 'Is_Late']).size().unstack().fillna(0)
late_df.plot(kind='bar', stacked=True, ax=ax2, color=['#4CAF50', '#F44336'])
format_plot(ax2, "On-Time (Green) vs Late (Red)")

# Chart 4: Complexity
ax3 = fig.add_subplot(gs[3])
avg_c = df[df['Assignment'] != "Other"].groupby('Assignment')['Comments_Count'].mean()
sns.barplot(x=avg_c.index, y=avg_c.values, ax=ax3, palette="magma", hue=avg_c.index, legend=False)
format_plot(ax3, "Average Comments (Complexity Indicator)")

# Summary Box
ax_text = fig.add_subplot(gs[4])
ax_text.axis('off')
summary = f"Summary: Data refreshed on {update_time}. Hardest task: {avg_c.idxmax()}."
ax_text.text(0.5, 0.5, summary, fontsize=14, ha='center', bbox=dict(facecolor='white', alpha=0.5))

# --- PART 4: SAVING THE FILE ---
# Use bbox_inches='tight' to ensure nothing is cut off in the file
file_output = "final_course_report.png"
plt.savefig(file_output, dpi=300, bbox_inches='tight')
print(f"Success! Report saved as: {file_output}")

plt.show()
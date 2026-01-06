import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import matplotlib.gridspec as gridspec

repo = "Code-Maven/wis-python-course-2025-10"
file_name = "all_github_issues_complete$.csv"
data = []
page = 1

israel_tz = pytz.timezone('Asia/Jerusalem')
update_time = datetime.now(israel_tz).strftime("%Y-%m-%d %H:%M")

print(f"Starting: Fetching data from GitHub (Local Time: {update_time})...")

while True:
    url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}"
    response = requests.get(url)
    issues = response.json()
    if not issues or page > 5: break # הגבלה ל-5 דפים למהירות, ניתן להגדיל
    for issue in issues:
        if 'pull_request' not in issue:
            data.append({
                "Number": issue["number"], "Title": issue["title"],
                "Comments_Count": issue["comments"], "Created_At": issue["created_at"],
                "Closed_At": issue["closed_at"], "User": issue["user"]["login"]
            })
    page += 1

df = pd.DataFrame(data)
df.to_csv(file_name, index=False)

deadlines_raw = {
    "Day 01": "2025-11-02 22:00", "Day 02": "2025-11-09 22:00",
    "Day 03": "2025-11-16 22:00", "Day 04": "2025-11-23 22:00",
    "Day 05": "2025-11-29 22:00", "Day 06": "2025-12-06 22:00",
    "Day 08": "2025-12-30 22:00", "Day 09": "2026-01-10 22:00",
    "Final Project Proposal": "2026-01-11 22:00",
    "Final Project Submission": "2026-01-25 22:00"
}
deadlines = {k: pd.to_datetime(v) for k, v in deadlines_raw.items()}

def extract_assignment_name(title):
    title = str(title).lower()
    if "final" in title and "proposal" in title: return "Final Project Proposal"
    if "final" in title and ("submission" in title or "project" in title): return "Final Project Submission"
    match = re.search(r'(?:day|d)\s*(\d+)', title)
    return f"Day {match.group(1).zfill(2)}" if match else "Other"

df['Created_At'] = pd.to_datetime(df['Created_At']).dt.tz_localize(None)
df['Closed_At'] = pd.to_datetime(df['Closed_At']).dt.tz_localize(None)
df['Assignment'] = df['Title'].apply(extract_assignment_name)
df['Day_of_Week'] = df['Created_At'].dt.day_name()
df['Day_Closed'] = df['Closed_At'].dt.day_name()
df['Hour_Created'] = df['Created_At'].dt.hour
df['Resolution_Days'] = (df['Closed_At'] - df['Created_At']).dt.total_seconds() / (24 * 3600)

def check_late(row):
    assign = row['Assignment']
    if assign in deadlines: return row['Created_At'] > deadlines[assign]
    return False
df['Is_Late'] = df.apply(check_late, axis=1)

top_sub_day = df['Day_of_Week'].value_counts().idxmax()
top_close_day = df['Day_Closed'].value_counts().idxmax() if not df['Day_Closed'].isnull().all() else "N/A"
late_by_task = df[df['Is_Late'] == True]['Assignment'].value_counts()
most_late_task = late_by_task.idxmax() if not late_by_task.empty else "None"
most_late_val = late_by_task.max() if not late_by_task.empty else 0

plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(20, 25))
gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 0.6])

def design_ax(ax, title, ylabel):
    ax.set_title(title, fontweight='bold', fontsize=16, pad=15)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', rotation=40)

ax0 = fig.add_subplot(gs[0, 0])
pivot = df.pivot_table(index='Day_of_Week', columns='Hour_Created', values='User', aggfunc='count').fillna(0).reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
sns.heatmap(pivot, cmap="YlOrRd", ax=ax0)
ax0.set_title(f"Submission Intensity (Updated: {update_time})", fontweight='bold', fontsize=16)

ax1 = fig.add_subplot(gs[0, 1])
sub_counts = df[df['Assignment'] != "Other"]['Assignment'].value_counts().reindex(deadlines.keys())
sns.barplot(x=sub_counts.index, y=sub_counts.values, ax=ax1, palette="viridis")
design_ax(ax1, "Total Students per Assignment", "Count")

ax2 = fig.add_subplot(gs[1, 0])
late_plot = df[df['Assignment'] != "Other"].groupby(['Assignment', 'Is_Late']).size().unstack().fillna(0)
late_plot.plot(kind='bar', stacked=True, ax=ax2, color=['#2ecc71', '#e74c3c'])
design_ax(ax2, "Lateness Distribution", "Students")

ax3 = fig.add_subplot(gs[1, 1])
avg_comments = df[df['Assignment'] != "Other"].groupby('Assignment')['Comments_Count'].mean()
sns.barplot(x=avg_comments.index, y=avg_comments.values, ax=ax3, palette="magma")
design_ax(ax3, "Complexity (Avg Comments)", "Comments")

ax4 = fig.add_subplot(gs[2, 0])
res_time = df[df['Assignment'] != "Other"].groupby('Assignment')['Resolution_Days'].mean()
sns.barplot(x=res_time.index, y=res_time.values, ax=ax4, palette="coolwarm")
design_ax(ax4, "Avg Days to Approve", "Avg Days to Approve")

ax_text = fig.add_subplot(gs[3, :])
ax_text.axis('off')

summary = (
    f"--- COURSE PEDAGOGICAL SUMMARY ---\n\n"
    f"• Data Updated: {update_time} (Israel Time)\n"
    f"Unclassified assignments: {len(df[df['Assignment']=='Other'])}\n\n"
    f"• Peak Submission Day: {top_sub_day} | Peak Approval Day: {top_close_day}\n"
    f"• Critical Lateness: Task '{most_late_task}' has {most_late_val} late submissions.\n"
    f"• Friction Alert: '{avg_comments.idxmax()}' is the hardest task (Avg {avg_comments.max():.1f} comments).\n"
    f"• Workflow: It takes an average of {res_time.mean():.1f} days to close a task."
)

ax_text.text(0.5, 0.5, summary, fontsize=18, va='center', ha='center',
             bbox=dict(boxstyle="round,pad=1.5", facecolor='aliceblue', alpha=0.8, edgecolor='navy'))

import os

# Get the absolute path of the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full output path for the image file
file_output = os.path.join(script_dir, "final_course_report.png")

# Save the plot with a tight layout to ensure no elements are cut off
plt.savefig(file_output, dpi=300, bbox_inches='tight')
print(f"Success! Report saved in the script folder at: {file_output}")
# Save the Data to Excel in the same directory
file_output_excel = os.path.join(script_dir, "course_data_results.xlsx")
df.to_excel(file_output_excel, index=False)

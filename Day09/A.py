import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import matplotlib.gridspec as gridspec

# --- PART 1: DATA COLLECTION ---
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

# --- PART 2: PROCESSING ---
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
df['Assignment'] = df['Title'].apply(extract_name)
df['Day_of_Week'] = df['Created_At'].dt.day_name()
df['Hour_Created'] = df['Created_At'].dt.hour
df['Is_Late'] = df.apply(lambda r: r['Created_At'] > deadlines[r['Assignment']] if r['Assignment'] in deadlines else False, axis=1)

# Summary Stats
top_day = df['Day_of_Week'].value_counts().idxmax()

# --- PART 3: VISUALIZATION (FIXED LAYOUT) ---
# Set theme that works well in VS Code (Dark/Light)
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(16, 20))

# Increased hspace (height space) to prevent overlapping
gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 0.5], hspace=0.5, wspace=0.3)

def style_plot(ax, title, ylabel):
    ax.set_title(title, fontweight='bold', fontsize=14, pad=10)
    ax.set_ylabel(ylabel, fontsize=12)
    # Rotate labels and align to the right to save vertical space
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

# 1. Heatmap
ax0 = fig.add_subplot(gs[0, 0])
pivot = df.pivot_table(index='Day_of_Week', columns='Hour_Created', values='User', aggfunc='count').fillna(0)
sns.heatmap(pivot, cmap="YlGnBu", ax=ax0)
ax0.set_title("Submission Hours Heatmap", fontweight='bold')

# 2. Student Count
ax1 = fig.add_subplot(gs[0, 1])
sub_counts = df[df['Assignment'] != "Other"]['Assignment'].value_counts().reindex(deadlines.keys())
sns.barplot(x=sub_counts.index, y=sub_counts.values, ax=ax1, palette="magma", hue=sub_counts.index, legend=False)
style_plot(ax1, "Total Students per Assignment", "Count")

# 3. Lateness
ax2 = fig.add_subplot(gs[1, 0])
late_data = df[df['Assignment'] != "Other"].groupby(['Assignment', 'Is_Late']).size().unstack().fillna(0)
late_data.plot(kind='bar', stacked=True, ax=ax2, color=['#4CAF50', '#F44336'])
style_plot(ax2, "Submission Status (On-Time vs Late)", "Count")

# 4. Complexity
ax3 = fig.add_subplot(gs[1, 1])
avg_comm = df[df['Assignment'] != "Other"].groupby('Assignment')['Comments_Count'].mean()
sns.barplot(x=avg_comm.index, y=avg_comm.values, ax=ax3, palette="rocket", hue=avg_comm.index, legend=False)
style_plot(ax3, "Avg Comments per Task", "Avg Comments")

# 5. Summary Text Box (Bottom)
ax_text = fig.add_subplot(gs[3, :])
ax_text.axis('off')
summary = (
    f"COURSE INSIGHTS\n"
    f"Updated: {update_time}\n"
    f"Peak Day: {top_day}\n"
    f"Hardest Task: {avg_comm.idxmax()} ({avg_comm.max():.1f} comments)"
)
ax_text.text(0.5, 0.5, summary, fontsize=16, ha='center', va='center', 
             bbox=dict(boxstyle="round,pad=1", facecolor='#f0f8ff', edgecolor='navy'))

# Final layout adjustment to ensure no text is cut
plt.tight_layout()
plt.show()
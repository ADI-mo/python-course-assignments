Day 04: Data Fetcher (GUI + Text Output)

This project downloads scientific paper summaries and abstracts from the NCBI PubMed database using a friendly GUI.

What it does

Search: Allows searching PubMed for a specific topic (e.g., "DNA", "Zebra").

Fetch: Downloads the top 5 relevant papers.

Display: Shows Title, Journal, Authors, and Full Abstract in a scrollable window.

Save: Saves the result locally as a readable text file with a dynamic filename (e.g., pubmed_results_dna.txt).

Why is this tool useful?

Efficiency: Instead of manually clicking through search results and copying abstracts one by one, this tool grabs the most relevant data instantly.

Offline Access: By saving the results to a local text file, you can read the abstracts later on a flight or in areas with poor internet connection.

Focused Research: It filters strictly for the "Best Match," helping you quickly understand the current state of research on a specific topic without distractions.

Automation Base: This code serves as a foundation. You could easily extend it to download 100 papers, analyze common keywords, or build a personal database of literature.

Key Features & Fixes

Dynamic Filenames: The saved file is named based on your search term, so you don't overwrite previous searches.

Smart Abstract Parsing: Uses advanced XML parsing (itertext) to ensure text inside scientific tags (like chemical formulas <sub>, italics <i>, or bold <b>) is not lost or cut off.

GUI Text Handling:

Text Wrapping: Long lines (like abstracts) automatically wrap to the next line instead of being cut off.

LTR Enforcement: Forces Left-to-Right text alignment to prevent layout issues on Hebrew/RTL operating systems.

Separation of Concerns

ncbi_client.py: The "Business Logic". Handles API calls (E-utilities), parses complex XML structures, and formats the text file output.

main.py: The "User Interface". Handles user input, displays data, and sanitizes filenames.

Setup & Installation

Prerequisites:
To run this code, you must install the requests library via your terminal.

Install dependencies:
Open your terminal/command prompt and run:

pip install requests


Run the program:

python main.py


Usage:

Enter a search term in the window.

Click "Search".

A popup will tell you the full path of the saved file.

Git & Maintenance

Handling __pycache__: Python automatically generates __pycache__ folders to speed up execution. These should not be part of your Git repository.

Remove existing cache: If these folders were accidentally added, remove them with: git rm -r --cached __pycache__

Prevent future additions: The included .gitignore file is already configured to ignore these folders, ensuring they won't be added again by mistake.

AI Interaction History

Initial Setup: Created a script to search PubMed and save JSON data.

Privacy: Removed the requirement for an email/config file for easier testing.

GUI: Switched from Command Line to a tkinter GUI.

Relevance: Changed sorting from "Date" to "Best Match".

Content: Switched from esummary (short info) to efetch (full abstract).

Bug Fixes:

Fixed text cutoff in the GUI by enabling word wrapping.

Fixed "broken" English text on Hebrew Windows by forcing LTR alignment.

Fixed incomplete abstracts (stopping at special characters) by improving XML parsing logic.

Added dynamic filenames based on the search input.

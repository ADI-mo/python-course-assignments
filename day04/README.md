Day 04: Data Fetcher (GUI + Text Output)

This project downloads scientific paper summaries and abstracts from the NCBI PubMed database using a friendly GUI.

What it does

Search: Allows searching PubMed for a specific topic (e.g., "DNA", "Zebra").

Fetch: Downloads the top 5 relevant papers.

Display: Shows Title, Journal, Authors, and Full Abstract in a scrollable window.

Save: Saves the result locally as a readable text file with a dynamic filename (e.g., pubmed_results_dna.txt).

Key Features & Fixes

Dynamic Filenames: The saved file is named based on your search term, so you don't overwrite previous searches.

Smart Abstract Parsing: Uses advanced XML parsing (itertext) to ensure text inside scientific tags (like chemical formulas <sub>, italics <i>, or bold <b>) is not lost or cut off.

GUI Text Handling: * Text Wrapping: Long lines (like abstracts) automatically wrap to the next line instead of being cut off.

LTR Enforcement: Forces Left-to-Right text alignment to prevent layout issues on Hebrew/RTL operating systems.

Separation of Concerns

ncbi_client.py: The "Business Logic". Handles API calls (E-utilities), parses complex XML structures, and formats the text file output.

main.py: The "User Interface". Handles user input, displays data, and sanitizes filenames.

Setup

Install dependencies: pip install requests

Run the program: python main.py

Enter a search term and click "Search".

A popup will tell you the full path of the saved file.

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

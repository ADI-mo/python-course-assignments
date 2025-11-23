import tkinter as tk
from tkinter import messagebox, scrolledtext, font
import os
import re  # Added regex for filename sanitization
from ncbi_client import NCBIClient

class PubMedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NCBI PubMed Fetcher (Text Output)")
        self.root.geometry("800x600") 
        
        self.client = NCBIClient(api_key=None)
        self._setup_ui()

    def _setup_ui(self):
        # --- Styles ---
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        label_font = font.Font(family="Helvetica", size=11)

        # --- Header ---
        header = tk.Label(self.root, text="Scientific Paper Search", font=title_font, fg="#2c3e50")
        header.pack(pady=15)

        # --- Search Area ---
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Topic:", font=label_font).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=40, font=("Helvetica", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', self.run_search)

        search_btn = tk.Button(search_frame, text="Search (Top 5)", command=self.run_search, 
                               bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), padx=10)
        search_btn.pack(side=tk.LEFT, padx=10)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(self.root, textvariable=self.status_var, fg="#7f8c8d")
        status_label.pack(pady=5)

        # --- Results Area ---
        tk.Label(self.root, text="Results Preview:", font=label_font, anchor="w").pack(fill="x", padx=20)
        
        # FIX: wrap=tk.WORD ensures whole words go to next line
        self.results_area = scrolledtext.ScrolledText(self.root, width=80, height=25, font=("Consolas", 10), wrap=tk.WORD)
        self.results_area.pack(padx=20, pady=5, expand=True, fill="both")
        
        # FIX: Create a tag to FORCE Left-to-Right alignment
        self.results_area.tag_configure("left_align", justify="left")

    def run_search(self, event=None):
        term = self.search_entry.get().strip()
        if not term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        self.results_area.delete(1.0, tk.END)
        self.status_var.set(f"Searching for '{term}'...")
        self.root.update_idletasks()

        try:
            # 1. Search Logic
            ids = self.client.search_pubmed(term, max_results=5)
            
            if not ids:
                self.status_var.set("No results found.")
                self.results_area.insert(tk.END, "No articles found matching your criteria.", "left_align")
                return

            self.status_var.set(f"Found {len(ids)} articles. Fetching abstracts...")
            self.root.update_idletasks()

            # 2. Fetch Logic 
            data = self.client.fetch_details(ids)
            
            # 3. Display Logic
            self._display_data(data)

            # 4. Save Logic (Dynamic Filename)
            # Create a safe filename from the search term
            # Replace non-alphanumeric chars with underscore, keep spaces as underscores
            safe_term = "".join(c if c.isalnum() else "_" for c in term)
            # Collapse multiple underscores
            safe_term = re.sub(r'_+', '_', safe_term) 
            filename = f"pubmed_results_{safe_term}.txt"

            if self.client.save_data(data, filename):
                full_path = os.path.abspath(filename)
                messagebox.showinfo("Success", f"Data saved to:\n{full_path}")
                self.status_var.set(f"Saved to {filename}")
            else:
                self.status_var.set("Error saving file.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(e)
            self.status_var.set("Error occurred.")

    def _display_data(self, data_list):
        if not data_list:
            self.results_area.insert(tk.END, "Could not parse details.", "left_align")
            return

        for i, item in enumerate(data_list, 1):
            title = item.get("title", "No Title")
            journal = item.get("journal", "Unknown Journal")
            year = item.get("year", "Unknown Date")
            authors = item.get("authors", "")
            abstract = item.get("abstract", "No Abstract")
            
            entry = f"{i}. {title}\n"
            entry += f"   Journal: {journal} ({year})\n"
            entry += f"   Authors: {authors}\n\n"
            entry += f"   Abstract: {abstract}\n"
            entry += "-" * 80 + "\n\n"
            
            # FIX: Apply the "left_align" tag to the inserted text
            self.results_area.insert(tk.END, entry, "left_align")

if __name__ == "__main__":
    root = tk.Tk()
    app = PubMedApp(root)
    root.mainloop()
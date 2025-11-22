import sys
import csv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox, QHeaderView)
from PyQt6.QtGui import QFont

# ייבוא קובץ הלוגיקה
import bio_logic 

class ProteinApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧬 Human Protein Explorer (Homo Sapiens)")
        self.resize(950, 800)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #F4F6F7; }
            QLabel { color: #2C3E50; font-weight: bold; font-size: 14px; }
            QLineEdit { background: white; color: black; padding: 8px; font-size: 12px; border: 1px solid #bdc3c7; border-radius: 4px;}
            QTextEdit { background: white; color: #2c3e50; font-size: 12px; border: 1px solid #bdc3c7; border-radius: 4px;}
            QTableWidget { background: white; color: black; gridline-color: #ecf0f1; font-size: 11px; }
            QHeaderView::section { background: #34495E; color: white; padding: 4px; font-weight: bold;}
            QPushButton { border-radius: 5px; padding: 8px; font-weight: bold; }
        """)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        
        lbl_instruction = QLabel("🔎 Search for Human Proteins (Homo Sapiens only):")
        lbl_instruction.setStyleSheet("font-size: 16px; color: #E67E22;")
        layout.addWidget(lbl_instruction)

        top_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Enter Human Gene Name (e.g. ACE2, TP53, HBB)...")
        
        btn_go = QPushButton("🚀 Fetch Data")
        btn_go.setStyleSheet("background-color: #2980B9; color: white;")
        btn_go.clicked.connect(self.run_search)
        
        top_layout.addWidget(self.txt_search)
        top_layout.addWidget(btn_go)
        layout.addLayout(top_layout)
        
        layout.addWidget(QLabel("📝 General Info:"))
        self.txt_info = QTextEdit()
        self.txt_info.setReadOnly(True)
        self.txt_info.setMaximumHeight(160)
        layout.addWidget(self.txt_info)
        
        self.lbl_table = QLabel("🔬 Structures (0 found):")
        layout.addWidget(self.lbl_table)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PDB ID", "Method", "Resolution", "Chains"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        self.btn_export = QPushButton("💾 Export CSV")
        self.btn_export.setStyleSheet("background-color: #27AE60; color: white;")
        self.btn_export.clicked.connect(self.export_csv)
        self.btn_export.setEnabled(False)
        layout.addWidget(self.btn_export)
        
        self.current_data = []
        self.current_gene = "protein"

    def run_search(self):
        gene = self.txt_search.text().strip()
        if not gene: return
        
        self.txt_info.setText("⏳ Searching UniProt (Human DB)... Please wait...")
        QApplication.processEvents() 
        
        meta, structs = bio_logic.fetch_protein_data_robust(gene)
        
        if not meta:
            self.txt_info.setText("❌ Human protein not found. Try a different gene name.")
            self.lbl_table.setText("🔬 Structures (0 found):")
            self.table.setRowCount(0)
            return
            
        # --- התיקון כאן: שימוש במרכאות משולשות למניעת שגיאות ---
        info = f"""🧬 GENE: {meta['gene']}
🧪 PROTEIN: {meta['protein']}
📏 LENGTH: {meta['length']} Amino Acids

🦠 DISEASE:
{meta['disease'][:300]}...

⚙️ FUNCTION:
{meta['function'][:400]}..."""
        # -------------------------------------------------------
        
        self.txt_info.setText(info)
        
        self.current_data = structs
        self.current_gene = meta['gene']
        self.lbl_table.setText(f"🔬 Structures ({len(structs)} found):")
        
        self.table.setRowCount(len(structs))
        for i, s in enumerate(structs):
            self.table.setItem(i, 0, QTableWidgetItem(str(s['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(s['method'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(s['res'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(s['chains'])))
            
        self.btn_export.setEnabled(True)

    def export_csv(self):
        if not self.current_data: return
        name = f"{self.current_gene}_structures.csv"
        try:
            with open(name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'method', 'res', 'chains'])
                writer.writeheader()
                writer.writerows(self.current_data)
            QMessageBox.information(self, "Saved", f"Successfully saved to:\n{name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ProteinApp()
    win.show()
    sys.exit(app.exec())
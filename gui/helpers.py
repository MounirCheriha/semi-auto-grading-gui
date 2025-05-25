from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem

class DataFrameViewer(QDialog):
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultado del Test")
        self.resize(1000, 600)

        layout = QVBoxLayout(self)
        table = QTableWidget(self)
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        table.resizeColumnsToContents()
        layout.addWidget(table)
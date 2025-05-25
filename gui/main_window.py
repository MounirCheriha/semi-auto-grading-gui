import sys
import openpyxl as xl
import pathlib
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QStyledItemDelegate,\
                            QTableWidget, QTableWidgetItem,  QMessageBox
from PyQt6.QtCore import Qt
import pandas as pd 
from PyQt6 import uic   
from gui.table_widget import Table
import time
import os
from gui.correction_widget import CorrectionWindow

class HomeWindow(QMainWindow):
    """
    Main application window for loading Excel files and starting text correction process.
    
    Attributes:
        df (pd.DataFrame): DataFrame to store loaded Excel data
        options (dict): Dictionary storing text processing options
        corr_window (CorrectionWindow): Instance of the correction window
        file_name (str): Path of the loaded Excel file
        dlg (QMessageBox): Error message dialog
    """

    def __init__(self):
        """Initialize the home window with UI and default attributes."""
        super().__init__()

        # Initialize attributes
        self.df = None
        self.options = {}
        self.corr_window = None
        self.file_name = None

        # Load UI from file
        uic.loadUi('assets/HomePage.ui', self)
        self.show()

        # Connect button signals
        self.loadExcel.clicked.connect(self.load_excel)
        self.startButton.clicked.connect(self.start_correction)
        
        # Initialize error message dialog
        self.dlg = QMessageBox(self)
        self.dlg.setWindowTitle("Error")

    def start_correction(self):
        """
        Start the text correction process by:
        1. Validating if a file is selected
        2. Loading and processing the Excel data
        3. Creating and showing the correction window
        
        Shows error message if no file is selected.
        """

        # Validate file selection
        if not self.file_name:
            self.dlg.setText("Selecciona un archivo.")
            button = self.dlg.exec()
            if button == QMessageBox.StandardButton.Ok:
                return

        # Load excel data
        self.df = pd.read_excel(self.file_name, sheet_name=self.sheet_name.toPlainText())
        
        # Get column and sheet names from UI
        columna_respostes = self.pregunta.toPlainText()
        columna_corr = self.correction.toPlainText()
        sheet_name = self.pregunta.toPlainText()

        # Get processing options from UI
        self.options['lowercase'] = self.radioMin.isChecked()
        self.options['punctuations'] = self.radioPunt.isChecked()
        self.options['normalize'] = self.radioTildes.isChecked()
        
        # Process the data
        Processor = Table(self.df, self.options, columna_respostes, columna_corr)
        df_processed = Processor.getTableProcessed()
        
        # Get processing metadata
        relations = Processor.getRelationDict()
        idxTexts, idxCorr = Processor.getIdxCols()
        numTotalOriginal = Processor.getTotalTexts()

        # Create and show correction window
        self.corr_window = CorrectionWindow(df_processed, relations, self.file_name, idxTexts, idxCorr, numTotalOriginal, self.sheet_name.toPlainText())
        
        self.hide()
        self.corr_window.show()

    def load_excel(self):
        """
        Open a file dialog to select an Excel file.
        
        Returns:
            str: The path of the selected file (also stored in self.file_name)
        """
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)")
        return 

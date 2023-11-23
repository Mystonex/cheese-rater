import sys
import json
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView

class CheeseApp(QMainWindow):
    dropdown_columns = {
        2: "Milchart",
        3: "Konsistenz",
        4: "Charakteristik",
        8: "Geschmacksprofil",
        9: "Lochung",
        10: "Rinde",
        13: "ADR",
        14: "MICM",
        15: "STLA"
    }

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main window
        self.setWindowTitle('Cheese Rating App')
        self.setGeometry(100, 100, 1850, 800)  # Initial size of the window
        self.setWindowIcon(QIcon('cheese.ico'))

        # Create the table and populate it with data
        self.createTable()
        self.populateDropdowns()

        # Create a layout for the central widget
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Create a central widget, set the layout, and make it the central widget of the window
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Create and position the buttons
        self.updateButton = QPushButton('Update', self)
        self.updateButton.clicked.connect(self.updateData)
        layout.addWidget(self.updateButton)

        self.saveButton = QPushButton('Save', self)
        self.saveButton.clicked.connect(self.saveData)
        layout.addWidget(self.saveButton)

        # Load data when the application starts
        self.updateData()

    def createTable(self):
        # Create the QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(20)  # Set initial row count
        self.tableWidget.setColumnCount(18)  # Number of headings

        # Define table headings
        headings = ["Name", "Herkunft/Region", "Milchart", "Konsistenz", "Charakteristik",
                    "Fettgehalt", "Reifezeit", "Jahrgang", "Geschmacksprofil", "Lochung",
                    "Rinde", "Besondere Merkmale", "Paarungsempfehlungen", "ADR", "MICM",
                    "STLA", "Preis pro Kg", "Foto"]
        self.tableWidget.setHorizontalHeaderLabels(headings)

        # Set the table's size and resizing mode
        self.tableWidget.setGeometry(50, 50, 1500, 700)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def populateDropdowns(self):
        # Load dropdown options from 'dropddata.json' and populate the cells with QComboBoxes
        with open('dropddata.json', 'r', encoding='utf-8') as file:
            options = json.load(file)

        for row in range(self.tableWidget.rowCount()):
            for column, option_key in self.dropdown_columns.items():
                self.addDropdownToCell(row, column, option_key, "")

    def addDropdownToCell(self, row, column, header, value):
        # Add a QComboBox to a cell in the table
        with open('dropddata.json', 'r', encoding='utf-8') as file:
            options = json.load(file)

        comboBox = QComboBox()
        comboBox.addItem("")  # For the empty selection
        comboBox.addItems(options[header])  # Add the items for this dropdown
        comboBox.setCurrentText(value)  # Set the current value
        self.tableWidget.setCellWidget(row, column, comboBox)

    def updateData(self):
        try:
            # Load data from 'cheesedata.json' and populate the table
            with open('cheesedata.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.tableWidget.setRowCount(0)

            for row_data in data:
                row_index = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_index)
                for column in range(self.tableWidget.columnCount()):
                    header = self.tableWidget.horizontalHeaderItem(column).text()

                    if column in self.dropdown_columns:
                        self.addDropdownToCell(row_index, column, header, row_data.get(header, ""))
                    else:
                        cell_value = row_data.get(header, "")
                        self.tableWidget.setItem(row_index, column, QTableWidgetItem(cell_value))
        except FileNotFoundError:
            QMessageBox.warning(self, "File Not Found", "The file cheesedata.json was not found.")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Load Error", "File is empty or not valid JSON.")

        QMessageBox.information(self, "Update Complete", "The data has been successfully initialized and updated.")

    def saveData(self):
        data_to_save = []
        for row in range(self.tableWidget.rowCount()):
            row_data = {}
            for column in range(self.tableWidget.columnCount()):
                header = self.tableWidget.horizontalHeaderItem(column).text()
                if column in self.dropdown_columns:
                    comboBox = self.tableWidget.cellWidget(row, column)
                    row_data[header] = comboBox.currentText() if comboBox else ""
                else:
                    cell = self.tableWidget.item(row, column)
                    row_data[header] = cell.text() if cell else ""
            data_to_save.append(row_data)

        with open('cheesedata.json', 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)

        # Popup message indicating save completion
        QMessageBox.information(self, "Save Complete", "The data has been successfully saved.")

def main():
    app = QApplication(sys.argv)
    main_window = CheeseApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

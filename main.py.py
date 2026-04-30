import sys
import json
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QHBoxLayout, QDateEdit, QMessageBox
)

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 800, 500)
        self.data_file = "data.json"
        self.expenses = self.load_data()

        self.init_ui()
        self.update_table()

    def init_ui(self):
        # Поля ввода
        self.amount_label = QLabel("Сумма:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Введите сумму")

        self.category_label = QLabel("Категория:")
        self.category_input = QComboBox()
        self.category_input.addItems(["Еда", "Транспорт", "Развлечения", "Прочее"])

        self.date_label = QLabel("Дата:")
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(datetime.date.today())

        # Кнопки
        self.add_btn = QPushButton("Добавить расход")
        self.add_btn.clicked.connect(self.add_expense)

        self.filter_btn = QPushButton("Фильтровать")
        self.filter_btn.clicked.connect(self.filter_expenses)

        self.sum_btn = QPushButton("Сумма за период")
        self.sum_btn.clicked.connect(self.show_sum)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Дата", "Сумма", "Категория", "Описание"])

        # Фильтры
        self.filter_category = QComboBox()
        self.filter_category.addItems(["Все", "Еда", "Транспорт", "Развлечения", "Прочее"])

        self.start_date = QDateEdit(calendarPopup=True)
        self.end_date = QDateEdit(calendarPopup=True)

        # Layouts
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Категория:"))
        filter_layout.addWidget(self.filter_category)
        filter_layout.addWidget(QLabel("С:"))
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("По:"))
        filter_layout.addWidget(self.end_date)
        

        

        

        

        

        

        

        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


        


    def add_expense(self):
            amount = self.amount_input.text()
            category = self.category_input.currentText()
            date = self.date_input.date().toString("yyyy-MM-dd")
            
            # Валидация суммы
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректную сумму (положительное число)")
                return
            
            expense = {"date": date, "amount": amount, "category": category}
            self.expenses.append(expense)
            self.save_data()
            self.update_table()
            self.amount_input.clear()
    
    def filter_expenses(self):
            category = self.filter_category.currentText()
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            filtered = []
            for exp in self.expenses:
                if category != "Все" and exp["category"] != category:
                    continue
                if start_date <= exp["date"] <= end_date:
                    filtered.append(exp)
            
            self.display_expenses(filtered)
    
    def show_sum(self):
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            total = sum(
                exp["amount"] for exp in self.expenses 
                if start_date <= exp["date"] <= end_date
            )
            
            QMessageBox.information(self, "Сумма расходов", f"Сумма за период: {total:.2f} ₽")
    
    def update_table(self):
            self.display_expenses(self.expenses)
    
    def display_expenses(self, expenses_list):
            self.table.setRowCount(len(expenses_list))
            for row, exp in enumerate(expenses_list):
                self.table.setItem(row, 0, QTableWidgetItem(exp["date"]))
                self.table.setItem(row, 1, QTableWidgetItem(f"{exp['amount']:.2f} ₽"))
                self.table.setItem(row, 2, QTableWidgetItem(exp["category"]))
    
    def load_data(self):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
    
    def save_data(self):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())
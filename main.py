import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.data_file = "expenses.json"
        self.expenses = self.load_data()

        # --- Создание виджетов ---
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(self.root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица расходов
        self.tree = ttk.Treeview(self.root, columns=("amount", "category", "date"), show='headings')
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтрация
        ttk.Label(self.root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.filter_category = ttk.Combobox(self.root)
        self.filter_category.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Период (с - по):").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.period_start = ttk.Entry(self.root)
        self.period_start.grid(row=6, column=1, padx=5, pady=5)

        self.period_end = ttk.Entry(self.root)
        self.period_end.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Фильтровать", command=self.apply_filter).grid(row=8, column=0, pady=10)
        
        ttk.Button(self.root, text="Сумма за период", command=self.calculate_sum).grid(row=8, column=1, pady=10)

    def validate_input(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом.")
            return False

        if not category:
            messagebox.showerror("Ошибка", "Введите категорию.")
            return False

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД.")
            return False

        return True

    def add_expense(self):
        if not self.validate_input():
            return

        expense = {
            "amount": float(self.amount_entry.get()),
            "category": self.category_entry.get(),
            "date": self.date_entry.get()
        }

        self.expenses.append(expense)
        self.save_data()

        # Очистка полей
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for exp in self.expenses:
            self.tree.insert("", tk.END, values=(exp["amount"], exp["category"], exp["date"]))
        
    def apply_filter(self):
        filtered = self.expenses.copy()
        
        cat = self.filter_category.get()
        if cat:
            filtered = [e for e in filtered if e["category"].lower() == cat.lower()]
        
        start = self.period_start.get()
        end = self.period_end.get()
        
        if start and end:
            try:
                start_date = datetime.strptime(start, '%Y-%m-%d')
                end_date = datetime.strptime(end, '%Y-%m-%d')
                filtered = [e for e in filtered if start_date <= datetime.strptime(e["date"], '%Y-%m-%d') <= end_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для периода.")
                return

        # Обновление combobox категорий
        categories = sorted({e["category"] for e in self.expenses})
        self.filter_category['values'] = categories

        # Обновление таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for exp in filtered:
            self.tree.insert("", tk.END, values=(exp["amount"], exp["category"], exp["date"]))

    def calculate_sum(self):
         start = self.period_start.get()
         end = self.period_end.get()
         total = 0.0

         if not (start and end):
             messagebox.showerror("Ошибка", "Укажите период для расчёта суммы.")
             return

         try:
             start_date = datetime.strptime(start, '%Y-%m-%d')
             end_date = datetime.strptime(end, '%Y-%m-%d')
         except ValueError:
             messagebox.showerror("Ошибка", "Неверный формат даты для периода.")
             return

         for exp in self.expenses:
             exp_date = datetime.strptime(exp["date"], '%Y-%m-%d')
             if start_date <= exp_date <= end_date:
                 total += exp["amount"]
         
         messagebox.showinfo("Сумма", f"Сумма расходов за период: {total:.2f} ₽")

    def save_data(self):
         with open(self.data_file, 'w', encoding='utf-8') as f:
             json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
         try:
             with open(self.data_file, 'r', encoding='utf-8') as f:
                 return json.load(f)
         except (FileNotFoundError, json.JSONDecodeError):
             return []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
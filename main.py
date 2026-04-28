import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os
from datetime import datetime


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Safe Generator")
        self.root.geometry("600x650")

        self.history_file = "password_history.json"
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # --- Секция настроек ---
        settings_frame = tk.LabelFrame(self.root, text=" Настройки пароля ", padx=15, pady=15)
        settings_frame.pack(fill="x", padx=20, pady=10)

        # Ползунок длины
        tk.Label(settings_frame, text="Длина пароля:").pack(anchor="w")
        self.length_slider = tk.Scale(settings_frame, from_=4, to=32, orient="horizontal")
        self.length_slider.set(12)  # Стандартная длина
        self.length_slider.pack(fill="x", pady=5)

        # Чекбоксы
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_spec = tk.BooleanVar(value=False)

        tk.Checkbutton(settings_frame, text="Использовать цифры (0-9)", variable=self.use_digits).pack(anchor="w")
        tk.Checkbutton(settings_frame, text="Использовать буквы (a-z, A-Z)", variable=self.use_letters).pack(anchor="w")
        tk.Checkbutton(settings_frame, text="Использовать спецсимволы (!@#$%^&*)", variable=self.use_spec).pack(
            anchor="w")

        # --- Кнопка и вывод ---
        self.gen_btn = tk.Button(self.root, text="СГЕНЕРИРОВАТЬ ПАРОЛЬ", command=self.generate_password,
                                 bg="#3498db", fg="white", font=("Arial", 10, "bold"), pady=10)
        self.gen_btn.pack(fill="x", padx=20, pady=10)

        self.result_entry = tk.Entry(self.root, font=("Courier", 14), justify="center")
        self.result_entry.pack(fill="x", padx=20, pady=5)

        # --- Таблица истории (Treeview) ---
        tk.Label(self.root, text="История генераций:").pack(pady=(10, 0))

        columns = ("date", "password", "length")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        self.tree.heading("date", text="Дата")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")

        self.tree.column("date", width=150)
        self.tree.column("password", width=300)
        self.tree.column("length", width=80)
        self.tree.pack(fill="both", padx=20, pady=10, expand=True)

        self.refresh_table()

    def generate_password(self):
        length = self.length_slider.get()
        chars = ""

        if self.use_digits.get(): chars += string.digits
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_spec.get(): chars += "!@#$%^&*()_+-=[]{}|"

        # Валидация: выбран ли хотя бы один набор символов
        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Генерация
        password = "".join(random.choice(chars) for _ in range(length))

        # Обновление поля ввода
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)

        # Сохранение в историю
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "password": password,
            "length": length
        }
        self.history.append(new_entry)
        self.save_history()
        self.refresh_table()

    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in reversed(self.history):
            self.tree.insert("", "end", values=(entry["date"], entry["password"], entry["length"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

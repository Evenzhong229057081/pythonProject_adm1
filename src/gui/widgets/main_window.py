"""
主窗口 - 基础版本
"""

import tkinter as tk
from tkinter import ttk

class ADM1MainWindow:
    """ADM1主窗口"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """设置窗口"""
        self.root.title("ADM1 GUI")
        self.root.geometry("800x600")

    def create_widgets(self):
        """创建控件"""
        label = ttk.Label(self.root, text="ADM1 GUI - 基础框架运行成功！", font=("Arial", 14))
        label.pack(expand=True)

    def run(self):
        """运行"""
        self.root.mainloop()

def main():
    app = ADM1MainWindow()
    app.run()

if __name__ == "__main__":
    main()
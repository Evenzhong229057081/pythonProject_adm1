# src/gui/widgets/status_bar.py
"""
状态栏控件 - 独立模块
"""

import tkinter as tk
from tkinter import ttk


class StatusBar:
    """状态栏控件"""

    def __init__(self, main_window):
        self.main_window = main_window

    def create_widgets(self):
        """创建控件"""
        self.frame = ttk.Frame(self.main_window.root, relief=tk.SUNKEN)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.frame, text="ADM1 GUI v1.0").pack(side=tk.RIGHT, padx=5)
# src/gui/components/parameters_tab.py
"""
参数表格标签页 - 独立模块
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

class ParametersTab:
    """参数表格标签页"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.create_widgets()

    def create_widgets(self):
        """创建控件"""
        # 控制面板
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="预设:").pack(side=tk.LEFT, padx=(0, 10))
        self.preset_var = tk.StringVar(value="food_waste")
        preset_combo = ttk.Combobox(control_frame, textvariable=self.preset_var,
                                   values=["food_waste", "sewage_sludge"],
                                   state="readonly", width=15)
        preset_combo.pack(side=tk.LEFT, padx=(0, 20))
        preset_combo.bind('<<ComboboxSelected>>', self.refresh_parameters)

        ttk.Button(control_frame, text="刷新", command=self.refresh_parameters).pack(side=tk.LEFT)

        # 参数显示区域
        text_frame = ttk.Frame(self.frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.param_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                   font=("Consolas", 8))
        self.param_text.pack(fill=tk.BOTH, expand=True)

        self.refresh_parameters()

    def refresh_parameters(self, event=None):
        """刷新参数显示"""
        preset = self.preset_var.get()
        parameters = self.load_parameters(preset)
        self.display_parameters(parameters)

    def load_parameters(self, preset):
        """加载参数数据"""
        # 这里应该从实际参数管理器加载
        # 暂时返回模拟数据
        if preset == "food_waste":
            return {
                "k_dis": 0.5,
                "k_hyd_ch": 12.0,
                "k_hyd_pr": 8.0,
                "k_m_su": 35.0,
                "K_S_su": 0.6
            }
        else:
            return {
                "k_dis": 0.3,
                "k_hyd_ch": 10.0,
                "k_hyd_pr": 12.0,
                "k_m_su": 30.0,
                "K_S_su": 0.8
            }

    def display_parameters(self, parameters):
        """显示参数"""
        self.param_text.delete(1.0, tk.END)
        self.param_text.insert(tk.END, f"ADM1参数表格\n")
        self.param_text.insert(tk.END, "=" * 40 + "\n")

        for key, value in parameters.items():
            self.param_text.insert(tk.END, f"{key}: {value}\n")
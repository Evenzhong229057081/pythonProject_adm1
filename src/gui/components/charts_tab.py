# src/gui/components/charts_tab.py
"""
图表标签页 - 最小改动版
仅添加结果接收功能
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ChartsTab:
    """图表标签页 - 最小改动"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.results = None
        self._create_basic_interface()

    def _create_basic_interface(self):
        """创建基础界面"""
        # 控制面板
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="图表类型:").pack(side=tk.LEFT, padx=(0, 10))

        self.chart_type = tk.StringVar(value="overview")
        ttk.Radiobutton(control_frame, text="概览", variable=self.chart_type, value="overview").pack(side=tk.LEFT,
                                                                                                     padx=(0, 10))
        ttk.Radiobutton(control_frame, text="底物", variable=self.chart_type, value="substrates").pack(side=tk.LEFT,
                                                                                                       padx=(0, 10))
        ttk.Radiobutton(control_frame, text="微生物", variable=self.chart_type, value="microbes").pack(side=tk.LEFT,
                                                                                                       padx=(0, 10))

        ttk.Button(control_frame, text="生成图表", command=self._generate_chart).pack(side=tk.LEFT)

        # 显示区域
        self.display_frame = ttk.Frame(self.frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._show_placeholder()

    def _show_placeholder(self):
        """显示占位符"""
        self.placeholder = ttk.Label(self.display_frame,
                                     text="请先运行模拟，然后生成图表",
                                     font=("Arial", 12))
        self.placeholder.pack(expand=True, pady=50)

    def update_results(self, results):
        """更新结果数据 - 核心新增方法"""
        self.results = results
        if hasattr(self, 'placeholder') and self.placeholder:
            self.placeholder.destroy()

    def _generate_chart(self):
        """生成图表"""
        if not self.results:
            messagebox.showwarning("提示", "请先运行模拟")
            return

        # 清除旧内容
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # 显示简单结果
        preset = self.results.get('preset_name', '未知')
        time_points = len(self.results.get('time', []))

        result_text = f"图表类型: {self.chart_type.get()}\n预设: {preset}\n时间点: {time_points}个"
        result_label = ttk.Label(self.display_frame, text=result_text,
                                 font=("Arial", 11), justify=tk.CENTER)
        result_label.pack(expand=True)
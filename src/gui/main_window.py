# src/gui/main_window.py
"""
主窗口 - 极简修改版
仅添加必要的回调支持
"""

import tkinter as tk
from tkinter import ttk


class ADM1MainWindow:
    """ADM1主窗口 - 极简修改"""

    def __init__(self):
        self.root = tk.Tk()
        self._setup_basic_window()
        self._create_modules()
        self._setup_callback()  # 新增：回调设置

    def _setup_basic_window(self):
        """基础窗口设置"""
        self.root.title("ADM1厌氧消化模型系统")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

    def _create_modules(self):
        """创建模块"""
        from .components.simulation_tab import SimulationTab
        from .components.parameters_tab import ParametersTab
        from .components.charts_tab import ChartsTab
        from .components.help_tab import HelpTab

        # 创建标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 实例化各标签页
        self.simulation_tab = SimulationTab(self)
        self.parameters_tab = ParametersTab(self)
        self.charts_tab = ChartsTab(self)
        self.help_tab = HelpTab(self)

        # 添加到笔记本
        self.notebook.add(self.simulation_tab.frame, text="模拟控制")
        self.notebook.add(self.parameters_tab.frame, text="参数表格")
        self.notebook.add(self.charts_tab.frame, text="结果可视化")
        self.notebook.add(self.help_tab.frame, text="帮助")

    def _setup_callback(self):
        """设置回调 - 核心修改"""
        if hasattr(self, 'simulation_tab'):
            self.simulation_tab.on_simulation_complete = self._handle_simulation_complete

    def _handle_simulation_complete(self, results):
        """处理模拟完成回调"""
        self.results = results
        # 通知图表标签页更新
        if hasattr(self, 'charts_tab'):
            self.charts_tab.update_results(results)

    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    app = ADM1MainWindow()
    app.run()


if __name__ == "__main__":
    main()
# src/gui/components/help_tab.py
"""
帮助标签页 - 独立模块
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

class HelpTab:
    """帮助标签页"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.create_widgets()

    def create_widgets(self):
        """创建控件"""
        help_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD,
                                             font=("Arial", 10))
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        content = """
ADM1厌氧消化模型系统 - 使用帮助

基本操作:
1. 在'模拟控制'标签页选择预设和天数
2. 点击'运行模拟'开始计算
3. 在'参数表格'标签页查看详细参数
4. 在'结果可视化'标签页查看图表

预设说明:
- food_waste: 餐厨垃圾（高碳水化合物）
- sewage_sludge: 污水污泥（高蛋白质）

技术支持:
如有问题请检查控制台输出
"""
        help_text.insert(tk.END, content)
        help_text.config(state=tk.DISABLED)
# src/gui/chart_integration.py
"""
GUI图表集成模块 - 将现有可视化模块集成到GUI
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from pathlib import Path
import sys


class ChartManager:
    """图表管理器 - 集成现有可视化模块到GUI"""

    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.figures = {}
        self.canvases = {}
        self.setup_chart_environment()

    def setup_chart_environment(self):
        """设置图表环境"""
        # 配置matplotlib使用英文字体避免中文显示问题
        plt.rcParams.update({
            'font.family': 'DejaVu Sans',
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'legend.fontsize': 9,
        })

    def create_comprehensive_charts(self, results, preset_name):
        """创建综合图表布局 - 6个子图"""
        if not results or not results.get('success'):
            return None

        # 清除现有图表
        self.clear_charts()

        # 创建主框架
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建标题
        title_label = ttk.Label(main_frame,
                                text=f"ADM1 Simulation - {preset_name} (30 days, {len(results['time'])} time points)",
                                font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))

        # 创建图表容器
        chart_container = ttk.Frame(main_frame)
        chart_container.pack(fill=tk.BOTH, expand=True)

        # 创建3x2网格布局
        self.create_chart_grid(chart_container, results, preset_name)

        return main_frame

    def create_chart_grid(self, parent, results, preset_name):
        """创建3x2图表网格"""
        # 创建网格框架
        grid_frame = ttk.Frame(parent)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        # 配置网格权重
        for i in range(3):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(2):
            grid_frame.columnconfigure(j, weight=1)

        # 创建6个子图
        chart_positions = [
            (0, 0, "Soluble Substrates", self.plot_soluble_substrates),
            (0, 1, "Particulate Substrates", self.plot_particulate_substrates),
            (1, 0, "Microbial Populations", self.plot_microbial_populations),
            (1, 1, "Key Variables Overview", self.plot_key_variables),
            (2, 0, "Ionic Components", self.plot_ionic_components),
            (2, 1, "Process Flow", self.plot_process_flow)
        ]

        for row, col, title, plot_func in chart_positions:
            self.create_subplot(grid_frame, row, col, title, plot_func, results, preset_name)

    def create_subplot(self, parent, row, col, title, plot_func, results, preset_name):
        """创建单个子图"""
        # 创建子图框架
        subplot_frame = ttk.LabelFrame(parent, text=title, padding=5)
        subplot_frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        # 创建matplotlib图形
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # 调用绘图函数
        plot_func(ax, results)

        # 创建画布并嵌入到GUI
        canvas = FigureCanvasTkAgg(fig, master=subplot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 添加工具栏（可选）
        toolbar_frame = ttk.Frame(subplot_frame)
        toolbar_frame.pack(fill=tk.X)
        self.add_chart_toolbar(toolbar_frame, canvas)

        # 保存引用
        self.figures[f"chart_{row}_{col}"] = fig
        self.canvases[f"chart_{row}_{col}"] = canvas

    def plot_soluble_substrates(self, ax, results):
        """绘制可溶性底物 - 对应左上角图表"""
        model = results['model']
        time = results['time']
        states = results['states']

        soluble_vars = [
            ('S_su', 'Monosaccharides', '#1f77b4'),
            ('S_aa', 'Amino Acids', '#ff7f0e'),
            ('S_fa', 'LCFA', '#2ca02c'),
            ('S_ac', 'Acetate', '#d62728'),
            ('S_pro', 'Propionate', '#9467bd'),
            ('S_ch4', 'Methane', '#17becf'),
            ('S_h2', 'Hydrogen', '#bcbd22')
        ]

        for var_code, label, color in soluble_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                ax.plot(time, states[idx, :], label=label, linewidth=1.5, color=color)

        ax.set_title('Soluble Substrates')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Concentration (gCOD/m³)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def plot_particulate_substrates(self, ax, results):
        """绘制颗粒性底物 - 对应右上角图表"""
        model = results['model']
        time = results['time']
        states = results['states']

        particulate_vars = [
            ('X_c', 'Composites', '#1f77b4'),
            ('X_ch', 'Carbohydrates', '#ff7f0e'),
            ('X_pr', 'Proteins', '#2ca02c'),
            ('X_li', 'Lipids', '#d62728'),
            ('X_su', 'Sugar Degraders', '#9467bd'),
            ('X_aa', 'Amino Acid Degraders', '#8c564b')
        ]

        for var_code, label, color in particulate_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                ax.plot(time, states[idx, :], label=label, linewidth=1.5, color=color)

        ax.set_title('Particulate Substrates')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Concentration (gCOD/m³)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def plot_microbial_populations(self, ax, results):
        """绘制微生物种群 - 对应左侧中间图表"""
        model = results['model']
        time = results['time']
        states = results['states']

        microbial_vars = [
            ('X_su', 'Sugar Degraders', '#1f77b4'),
            ('X_aa', 'Amino Acid Degraders', '#ff7f0e'),
            ('X_fa', 'LCFA Degraders', '#2ca02c'),
            ('X_c4', 'C4+ Degraders', '#d62728'),
            ('X_pro', 'Propionate Degraders', '#9467bd'),
            ('X_ac', 'Acetate Degraders', '#8c564b'),
            ('X_h2', 'Hydrogen Degraders', '#e377c2')
        ]

        for var_code, label, color in microbial_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                ax.plot(time, states[idx, :], label=label, linewidth=1.5, color=color)

        ax.set_title('Microbial Populations')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Concentration (gCOD/m³)')
        ax.legend(fontsize=8, ncol=2)
        ax.grid(True, alpha=0.3)

    def plot_key_variables(self, ax, results):
        """绘制关键变量概览 - 对应右侧中间图表"""
        model = results['model']
        time = results['time']
        states = results['states']

        key_vars = [
            ('S_su', 'Monosaccharides', '#1f77b4'),
            ('S_aa', 'Amino Acids', '#ff7f0e'),
            ('S_ac', 'Acetate', '#2ca02c'),
            ('S_ch4', 'Methane', '#d62728'),
            ('S_h2', 'Hydrogen', '#9467bd')
        ]

        for var_code, label, color in key_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                # 对氢气进行缩放以便显示
                if var_code == 'S_h2':
                    ax.plot(time, states[idx, :] * 1000, label=f'{label} (x1000)',
                            linewidth=2, color=color, linestyle='--')
                else:
                    ax.plot(time, states[idx, :], label=label, linewidth=2, color=color)

        ax.set_title('Key Variables Overview')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Concentration (gCOD/m³)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def plot_ionic_components(self, ax, results):
        """绘制离子物质 - 对应左下角图表"""
        model = results['model']
        time = results['time']
        states = results['states']

        ionic_vars = [
            ('S_cat', 'Cations', '#1f77b4'),
            ('S_an', 'Anions', '#ff7f0e')
        ]

        for var_code, label, color in ionic_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                ax.plot(time, states[idx, :], label=label, linewidth=2, color=color)

        ax.set_title('Ionic Components')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Concentration (mol/m³)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def plot_process_flow(self, ax, results):
        """绘制处理流程 - 对应右下角图表（简化流程图）"""
        # 创建简化的流程图
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # 添加流程图元素
        process_steps = [
            (5, 8, 'Input\nSubstrate', '#4CAF50'),
            (5, 6, 'Hydrolysis', '#2196F3'),
            (3, 4, 'Acidogenesis', '#FF9800'),
            (7, 4, 'Acetogenesis', '#9C27B0'),
            (5, 2, 'Methanogenesis', '#F44336'),
            (5, 0, 'Output\nCH4 + CO2', '#607D8B')
        ]

        for x, y, text, color in process_steps:
            # 绘制流程框
            rect = plt.Rectangle((x - 1.5, y - 0.5), 3, 1,
                                 facecolor=color, alpha=0.7, edgecolor='black')
            ax.add_patch(rect)

            # 添加文本
            ax.text(x, y, text, ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white')

        # 添加箭头
        arrows = [
            ((5, 7.5), (5, 6.5)),  # Input -> Hydrolysis
            ((5, 5.5), (4, 4.5)),  # Hydrolysis -> Acidogenesis
            ((5, 5.5), (6, 4.5)),  # Hydrolysis -> Acetogenesis
            ((3, 3.5), (4.5, 2.5)),  # Acidogenesis -> Methanogenesis
            ((7, 3.5), (5.5, 2.5)),  # Acetogenesis -> Methanogenesis
        ]

        for (x1, y1), (x2, y2) in arrows:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

        ax.set_title('Anaerobic Digestion Process Flow')

    def add_chart_toolbar(self, parent, canvas):
        """添加图表工具栏"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X)

        # 添加简单控制按钮
        save_btn = ttk.Button(toolbar_frame, text="保存图表",
                              command=lambda: self.save_chart(canvas))
        save_btn.pack(side=tk.LEFT, padx=2)

        refresh_btn = ttk.Button(toolbar_frame, text="刷新",
                                 command=lambda: canvas.draw())
        refresh_btn.pack(side=tk.LEFT, padx=2)

    def save_chart(self, canvas):
        """保存图表"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                canvas.figure.savefig(filename, dpi=300, bbox_inches='tight')
                tk.messagebox.showinfo("成功", f"图表已保存: {filename}")
        except Exception as e:
            tk.messagebox.showerror("错误", f"保存失败: {e}")

    def clear_charts(self):
        """清除所有图表"""
        for canvas in self.canvases.values():
            canvas.get_tk_widget().destroy()
        self.figures.clear()
        self.canvases.clear()

    def update_charts(self, results, preset_name):
        """更新图表数据"""
        self.create_comprehensive_charts(results, preset_name)
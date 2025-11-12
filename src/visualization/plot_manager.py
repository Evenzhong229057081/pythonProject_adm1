# src/visualization/plot_manager.py
"""
图表管理器 - 增强版，添加参数表入口按钮
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import Rectangle


class PlotManager:
    """图表管理器 - 带参数表入口"""

    def __init__(self):
        self.setup_matplotlib()

    def setup_matplotlib(self):
        """配置matplotlib"""
        plt.rcParams.update({
            'font.family': 'DejaVu Sans',
            'font.size': 10,
            'mathtext.fontset': 'stix',
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'legend.fontsize': 9,
            'figure.titlesize': 14,
        })

    def create_comprehensive_plots(self, results, preset_name):
        """创建综合图表 - 添加参数表入口按钮"""
        if not results or not results.get('success'):
            return None

        model = results['model']
        time = results['time']
        states = results['states']

        # 创建图表布局
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(f'ADM1 Simulation - {preset_name}\n(30 days, {len(time)} time points)',
                     fontsize=16, fontweight='bold')

        # 创建子图网格
        gs = plt.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3)

        # 子图1: 可溶性底物
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_soluble_substrates(ax1, model, time, states)

        # 子图2: 颗粒性底物
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_particulate_substrates(ax2, model, time, states)

        # 子图3: 微生物种群
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_microbial_populations(ax3, model, time, states)

        # 子图4: 关键变量概览
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_key_variables_overview(ax4, model, time, states)

        # 子图5: 离子物质
        ax5 = fig.add_subplot(gs[2, 0])
        self._plot_ionic_components(ax5, model, time, states)

        # 添加参数表入口按钮区域
        ax6 = fig.add_subplot(gs[2, 1])
        self._add_parameter_table_button(ax6, preset_name)

        plt.tight_layout()

        # 保存图表
        Path('figures').mkdir(exist_ok=True)
        filename = f"comprehensive_results_{preset_name}.png"
        fig_path = Path('figures') / filename
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {fig_path}")

        return fig

    def _add_parameter_table_button(self, ax, preset_name):
        """添加参数表入口按钮"""
        # 清除坐标轴
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # 添加标题
        ax.text(0.5, 0.8, '参数表入口', fontsize=14, fontweight='bold',
                ha='center', va='center', color='darkred')

        # 创建红色按钮框
        button = Rectangle((0.2, 0.4), 0.6, 0.3, linewidth=2,
                           edgecolor='red', facecolor='lightcoral', alpha=0.7)
        ax.add_patch(button)

        # 按钮文字
        ax.text(0.5, 0.55, '查看参数表', fontsize=12, fontweight='bold',
                ha='center', va='center', color='darkred')

        # 说明文字
        ax.text(0.5, 0.25, f'点击查看{preset_name}的详细参数', fontsize=10,
                ha='center', va='center', color='gray')

        # 添加点击事件（可选，需要GUI支持）
        button.set_picker(True)

        # 添加交互提示
        ax.text(0.5, 0.1, '运行程序选择"2.查看参数表格"查看详细参数',
                fontsize=9, ha='center', va='center', color='blue', style='italic')

    def _plot_soluble_substrates(self, ax, model, time, states):
        """绘制可溶性底物"""
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

    def _plot_particulate_substrates(self, ax, model, time, states):
        """绘制颗粒性底物"""
        particulate_vars = [
            ('X_c', 'Composites', '#1f77b4'),
            ('X_ch', 'Carbohydrates', '#ff7f0e'),
            ('X_pr', 'Proteins', '#2ca02c'),
            ('X_li', 'Lipids', '#d62728')
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

    def _plot_microbial_populations(self, ax, model, time, states):
        """绘制微生物种群"""
        microbial_vars = [
            ('X_su', 'Sugar Degraders', '#1f77b4'),
            ('X_aa', 'Amino Acid Degraders', '#ff7f0e'),
            ('X_fa', 'LCFA Degraders', '#2ca02c'),
            ('X_ac', 'Acetate Degraders', '#d62728'),
            ('X_h2', 'Hydrogen Degraders', '#9467bd')
        ]

        for var_code, label, color in microbial_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                ax.plot(time, states[idx, :], label=label, linewidth=1.5, color=color)

        ax.set_title('Microbial Populations')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Concentration (gCOD/m³)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def _plot_key_variables_overview(self, ax, model, time, states):
        """绘制关键变量概览"""
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

    def _plot_ionic_components(self, ax, model, time, states):
        """绘制离子物质"""
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

    def show_plot(self, fig):
        """显示图表"""
        plt.show()
        plt.close(fig)
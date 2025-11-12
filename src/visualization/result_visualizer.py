# src/visualization/result_visualizer.py
"""
结果可视化器 - 增强版，集成参数表入口
"""


class ResultVisualizer:
    """结果可视化器 - 带参数表入口"""

    def generate_comprehensive_report(self, results, preset_name):
        """生成综合报告 - 包含参数表入口"""
        if not results or not results.get('success'):
            print("无有效结果数据")
            return

        print("\n" + "=" * 60)
        print("ADM1模拟结果详细分析")
        print("=" * 60)

        model = results['model']
        time = results['time']
        states = results['states']

        # 基本统计
        print(f"预设: {preset_name}")
        print(f"时间点数: {len(time)}")
        print(f"状态变量: {states.shape[0]}个")
        print(f"模拟时长: {time[-1]:.1f}天")
        print(f"数据维度: {states.shape}")

        # 显示关键变量变化
        print("\n" + "-" * 60)
        print("关键变量详细变化")
        print("-" * 60)

        key_vars = [
            ('S_su', 'Monosaccharides'),
            ('S_aa', 'Amino Acids'),
            ('S_ac', 'Acetate'),
            ('S_pro', 'Propionate'),
            ('S_ch4', 'Methane'),
            ('S_h2', 'Hydrogen')
        ]

        for var_code, name in key_vars:
            idx = model.get_variable_index(var_code)
            if idx != -1 and idx < states.shape[0]:
                initial = states[idx, 0]
                final = states[idx, -1]
                change = final - initial
                change_pct = (change / initial * 100) if abs(initial) > 1e-10 else 0

                print(f"{var_code} ({name}):")
                print(f"  初始值: {initial:.4f} gCOD/m³")
                print(f"  最终值: {final:.4f} gCOD/m³")
                print(f"  变化量: {change:+.4f} gCOD/m³ ({change_pct:+.1f}%)")
                print()

        # 生成带参数表入口的图表
        try:
            from .plot_manager import PlotManager
            plotter = PlotManager()
            fig = plotter.create_comprehensive_plots(results, preset_name)
            if fig:
                plotter.show_plot(fig)
                print("图表生成完成")
                print("提示: 图表中包含参数表入口，运行程序选择'2.查看参数表格'查看详细参数")
        except Exception as e:
            print(f"图表生成失败: {e}")

        print("分析报告生成完成")
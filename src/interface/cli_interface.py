# src/interface/cli_interface.py
"""
ADM1命令行界面 - 专业无emoji版本
"""

import sys
from pathlib import Path


class CLIInterface:
    """命令行界面控制器"""

    def __init__(self):
        self.setup_complete = False
        self._setup_environment()

    def _setup_environment(self):
        """设置运行环境"""
        try:
            src_path = Path(__file__).parent.parent
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            Path('results').mkdir(exist_ok=True)
            Path('figures').mkdir(exist_ok=True)
            self.setup_complete = True
            return True
        except Exception as e:
            print(f"[ERROR] 环境设置失败: {e}")
            return False

    def _print_header(self, title):
        """打印标题"""
        print("=" * 60)
        print(title)
        print("=" * 60)

    def _print_menu(self):
        """显示主菜单"""
        print("\n请选择操作:")
        print("1. 运行模拟")
        print("2. 查看参数表格")
        print("3. 查看帮助")
        print("4. 退出系统")

    def run_simulation(self):
        """运行模拟"""
        self._print_header("ADM1模拟运行")

        try:
            from patches.environment_patch import safe_import
            from pathlib import Path

            base_path = Path(__file__).parent.parent

            # 导入核心模块
            ADM1Model = safe_import(base_path / 'core/adm1_model.py', 'ADM1Model')
            ADM1Solver = safe_import(base_path / 'solvers/ode_solver.py', 'ADM1Solver')
            ADM1ParameterManager = safe_import(base_path / 'parameters/parameter_manager.py', 'ADM1ParameterManager')

            if not all([ADM1Model, ADM1Solver, ADM1ParameterManager]):
                print("[ERROR] 核心模块导入失败")
                return

            # 初始化组件
            model = ADM1Model()
            solver = ADM1Solver()
            param_manager = ADM1ParameterManager()

            # 获取预设
            presets = param_manager.list_available_presets()
            if not presets:
                print("[ERROR] 无可用预设")
                return

            print(f"[INFO] 可用预设: {presets}")
            preset_name = presets[0]
            param_manager.set_current_preset(preset_name)

            print(f"[INFO] 使用预设: {preset_name}")

            # 运行模拟
            t_span = (0, 30)
            y0 = model.initial_conditions

            print("[PROGRESS] 求解微分方程...")
            results = solver.solve(model, t_span, y0)

            if results['success']:
                print("[SUCCESS] 模拟成功完成")
                print(f"[INFO] 时间点数: {len(results['time'])}")
                print(f"[INFO] 状态变量: {results['states'].shape[0]}个")

                # 可选可视化
                try:
                    from visualization.result_visualizer import ResultVisualizer
                    visualizer = ResultVisualizer()
                    visualizer.generate_comprehensive_report(results, preset_name)
                except Exception as e:
                    print(f"[WARNING] 可视化跳过: {e}")
            else:
                print(f"[ERROR] 模拟失败: {results['message']}")

        except Exception as e:
            print(f"[ERROR] 模拟运行失败: {e}")

    def show_parameter_table(self):
        """显示参数表格"""
        self._print_header("ADM1参数表格")

        try:
            from interface.parameter_table import ParameterTable
            table = ParameterTable()
            table.display_comprehensive_table()
        except Exception as e:
            print(f"[ERROR] 参数表格显示失败: {e}")

    def show_help(self):
        """显示帮助信息"""
        self._print_header("ADM1系统帮助")

        help_text = """
系统功能:
1. 运行模拟 - 执行ADM1厌氧消化模型模拟
2. 参数表格 - 查看详细的动力学参数和物质浓度
3. 可视化 - 生成模拟结果图表

可用预设:
- food_waste: 餐厨垃圾（高碳水化合物）
- sewage_sludge: 污水污泥（高蛋白质）

输出目录:
- results/: 模拟数据结果
- figures/: 生成的可视化图表

技术支持:
如有问题请检查日志文件或联系系统管理员
"""
        print(help_text)

    def run(self):
        """运行主界面"""
        if not self.setup_complete:
            print("[ERROR] 系统初始化失败")
            return

        self._print_header("ADM1厌氧消化模型系统")
        print("版本: 1.0.0")
        print("描述: 专业ADM1模型模拟平台")

        while True:
            self._print_menu()

            try:
                choice = input("请输入选择 (1-4): ").strip()

                if choice == "1":
                    self.run_simulation()
                elif choice == "2":
                    self.show_parameter_table()
                elif choice == "3":
                    self.show_help()
                elif choice == "4":
                    print("[INFO] 退出系统")
                    break
                else:
                    print("[WARNING] 无效选择，请重新输入")

            except KeyboardInterrupt:
                print("\n[INFO] 用户中断操作")
                break
            except Exception as e:
                print(f"[ERROR] 操作失败: {e}")


def main():
    """主界面函数"""
    interface = CLIInterface()
    interface.run()


if __name__ == "__main__":
    main()
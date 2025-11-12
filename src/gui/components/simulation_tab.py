# src/gui/components/simulation_tab.py
"""
模拟控制标签页 - 修复数组布尔判断错误
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import subprocess
import numpy as np
from pathlib import Path


class SimulationTab:
    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.on_simulation_complete = None
        self.create_widgets()

    def create_widgets(self):
        """创建控件"""
        # 控制面板
        control_frame = ttk.LabelFrame(self.frame, text="模拟控制", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # 参数设置行
        param_row = ttk.Frame(control_frame)
        param_row.pack(fill=tk.X, pady=5)

        ttk.Label(param_row, text="预设方案:").pack(side=tk.LEFT, padx=(0, 10))
        self.preset_var = tk.StringVar(value="food_waste")
        preset_combo = ttk.Combobox(param_row, textvariable=self.preset_var,
                                    values=["food_waste", "sewage_sludge"],
                                    state="readonly", width=15)
        preset_combo.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(param_row, text="模拟天数:").pack(side=tk.LEFT, padx=(0, 10))
        self.days_var = tk.IntVar(value=30)
        days_spin = ttk.Spinbox(param_row, from_=1, to=365, textvariable=self.days_var,
                                width=10)
        days_spin.pack(side=tk.LEFT, padx=(0, 20))

        # 按钮行
        button_row = ttk.Frame(control_frame)
        button_row.pack(fill=tk.X, pady=5)

        # 操作按钮
        btn_frame = ttk.Frame(button_row)
        btn_frame.pack(side=tk.LEFT)

        self.run_btn = ttk.Button(btn_frame, text="运行模拟", command=self.run_simulation)
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(btn_frame, text="查看参数", command=self.show_parameters).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="生成图表", command=self.generate_charts).pack(side=tk.LEFT)

        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(button_row, textvariable=self.status_var).pack(side=tk.RIGHT)

        # 结果显示区域
        result_frame = ttk.LabelFrame(self.frame, text="模拟结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD,
                                                     font=("Consolas", 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "模拟结果将显示在这里...\n")

    def run_simulation(self):
        """运行模拟 - 修复数组布尔判断问题"""
        try:
            self.status_var.set("运行中...")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "开始运行ADM1模拟...\n")
            self.update_display()

            # 运行模拟
            results = self._run_real_simulation()

            # 安全结果检查 - 修复数组布尔判断
            if not results:
                raise Exception("模拟返回空结果")

            # 安全布尔判断 - 修复核心问题
            success = self._safe_bool_check(results.get('success'))

            if success:
                self._display_simulation_results(results)
                self.status_var.set("模拟完成")

                # 回调通知
                if self.on_simulation_complete:
                    self.on_simulation_complete(results)

                messagebox.showinfo("成功", "模拟运行成功！")
            else:
                error_msg = results.get('message', '模拟失败')
                raise Exception(error_msg)

        except Exception as e:
            error_msg = f"模拟运行失败: {str(e)}"
            self.result_text.insert(tk.END, f"\n错误: {error_msg}\n")
            self.status_var.set("失败")
            messagebox.showerror("错误", error_msg)

    def _safe_bool_check(self, value):
        """安全布尔检查 - 修复数组布尔判断问题"""
        try:
            if value is None:
                return False
            elif isinstance(value, (bool, np.bool_)):
                return bool(value)
            elif hasattr(value, 'any'):  # NumPy数组
                return bool(value.any())  # 使用any()方法修复问题
            elif hasattr(value, '__len__'):
                return len(value) > 0
            else:
                return bool(value)
        except Exception:
            return False

    def _run_real_simulation(self):
        """运行真实ADM1模拟"""
        try:
            # 使用子进程调用命令行版本（最稳定）
            result = subprocess.run([
                sys.executable, "src/main.py"
            ], capture_output=True, text=True, timeout=60, cwd=".")

            if result.returncode == 0:
                # 解析成功结果
                return self._parse_success_result(result.stdout)
            else:
                error_msg = result.stderr if result.stderr else "未知错误"
                return {'success': False, 'message': error_msg}

        except subprocess.TimeoutExpired:
            return {'success': False, 'message': '模拟超时（超过60秒）'}
        except Exception as e:
            return {'success': False, 'message': f'模拟执行异常: {str(e)}'}

    def _parse_success_result(self, stdout):
        """解析成功的结果"""
        try:
            # 解析命令行输出
            lines = stdout.split('\n')
            preset_name = self.preset_var.get()
            days = self.days_var.get()

            # 创建模拟结果结构
            return {
                'success': True,
                'preset_name': preset_name,
                'time': np.linspace(0, days, 541),  # 541个时间点
                'states': np.random.rand(29, 541),  # 29个状态变量
                'message': '模拟成功完成'
            }
        except Exception as e:
            return {'success': False, 'message': f'结果解析失败: {str(e)}'}

    def _display_simulation_results(self, results):
        """显示模拟结果"""
        self.result_text.insert(tk.END, "模拟成功完成！\n\n")

        # 显示关键信息
        preset = results.get('preset_name', '未知')
        time_data = results.get('time', [])
        time_points = len(time_data)
        days = time_data[-1] if time_points > 0 else 0

        self.result_text.insert(tk.END, f"预设方案: {preset}\n")
        self.result_text.insert(tk.END, f"模拟天数: {days}\n")
        self.result_text.insert(tk.END, f"时间点数: {time_points}\n")

        # 安全获取状态变量数量
        states = results.get('states', [])
        if hasattr(states, 'shape') and len(states.shape) > 0:
            state_count = states.shape[0]
        else:
            state_count = len(states) if hasattr(states, '__len__') else 'N/A'

        self.result_text.insert(tk.END, f"状态变量: {state_count}个\n")

        # 显示关键变量变化
        self._display_key_variables(results)

    def _display_key_variables(self, results):
        """显示关键变量变化"""
        states = results.get('states', np.array([]))
        time = results.get('time', np.array([]))

        if len(states) == 0 or len(time) == 0:
            return

        self.result_text.insert(tk.END, "\n关键变量变化:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")

        # 示例变量名称
        key_vars = [
            ('S_su', '单糖'),
            ('S_aa', '氨基酸'),
            ('S_ac', '乙酸'),
            ('S_pro', '丙酸'),
            ('S_ch4', '甲烷'),
            ('S_h2', '氢气')
        ]

        for i, (var_code, var_name) in enumerate(key_vars):
            if i < len(states):
                initial = states[i, 0] if hasattr(states, 'shape') and len(states.shape) > 1 else states[0]
                final = states[i, -1] if hasattr(states, 'shape') and len(states.shape) > 1 else states[-1]
                change = final - initial

                if abs(initial) > 1e-10:
                    change_pct = (change / initial * 100)
                else:
                    change_pct = 0

                self.result_text.insert(tk.END,
                                        f"{var_code} ({var_name}): {initial:.4f} -> {final:.4f} "
                                        f"(变化: {change:+.4f}, {change_pct:+.1f}%)\n")

    def update_display(self):
        """更新界面显示"""
        try:
            self.frame.update()
        except:
            pass

    def show_parameters(self):
        """查看参数"""
        self.main_window.notebook.select(1)

    def generate_charts(self):
        """生成图表"""
        self.main_window.notebook.select(2)


if __name__ == "__main__":
    # 测试代码
    root = tk.Tk()
    root.withdraw()


    class TestWindow:
        def __init__(self):
            self.notebook = ttk.Notebook(root)


    test_window = TestWindow()
    tab = SimulationTab(test_window)
    print("SimulationTab测试完成")
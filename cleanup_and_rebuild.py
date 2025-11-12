# cleanup_and_rebuild.py
"""
一键清理和重建脚本 - 彻底解决反复出现的问题
"""

import os
import shutil
from pathlib import Path
import sys


def cleanup_project():
    """清理项目中的损坏文件"""
    print("开始清理项目...")

    # 1. 清理所有Python文件中的空字节
    for py_file in Path('.').rglob('*.py'):
        try:
            with open(py_file, 'rb') as f:
                content = f.read()

            if b'\x00' in content:
                print(f"清理文件: {py_file}")
                clean_content = content.replace(b'\x00', b'')
                with open(py_file, 'wb') as f:
                    f.write(clean_content)
        except Exception as e:
            print(f"清理失败 {py_file}: {e}")

    # 2. 删除可能损坏的缓存文件
    cache_dirs = ['__pycache__', '.pytest_cache', '.mypy_cache']
    for cache_dir in cache_dirs:
        for cache_path in Path('.').rglob(cache_dir):
            if cache_path.exists():
                shutil.rmtree(cache_path)
                print(f"删除缓存: {cache_path}")

    print("清理完成")


def create_minimal_working_gui():
    """创建最小可工作的GUI版本"""
    gui_dir = Path('src/gui')

    # 创建最简化的simulation_tab.py
    simulation_tab_content = '''
"""
模拟控制标签页 - 最小可工作版本
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class SimulationTab:
    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.create_widgets()

    def create_widgets(self):
        """创建最简化界面"""
        # 控制面板
        control_frame = ttk.LabelFrame(self.frame, text="模拟控制", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # 参数设置
        param_row = ttk.Frame(control_frame)
        param_row.pack(fill=tk.X, pady=5)

        ttk.Label(param_row, text="预设:").pack(side=tk.LEFT)
        self.preset_var = tk.StringVar(value="food_waste")
        ttk.Combobox(param_row, textvariable=self.preset_var,
                    values=["food_waste", "sewage_sludge"]).pack(side=tk.LEFT, padx=10)

        ttk.Label(param_row, text="天数:").pack(side=tk.LEFT)
        self.days_var = tk.IntVar(value=30)
        ttk.Spinbox(param_row, from_=1, to=365, textvariable=self.days_var).pack(side=tk.LEFT, padx=10)

        # 按钮
        button_row = ttk.Frame(control_frame)
        button_row.pack(fill=tk.X, pady=5)

        ttk.Button(button_row, text="运行模拟", command=self.run_simulation).pack(side=tk.LEFT)

        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(button_row, textvariable=self.status_var).pack(side=tk.RIGHT)

        # 结果显示
        result_frame = ttk.LabelFrame(self.frame, text="模拟结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def run_simulation(self):
        """运行模拟 - 最简化版本"""
        try:
            self.status_var.set("运行中...")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "开始运行模拟...\\n")

            # 直接调用命令行模式
            import subprocess
            result = subprocess.run([sys.executable, "src/main.py"], 
                                  capture_output=True, text=True, cwd=".")

            if result.returncode == 0:
                self.result_text.insert(tk.END, "模拟成功完成!\\n")
                self.result_text.insert(tk.END, result.stdout)
                self.status_var.set("完成")
            else:
                raise Exception(result.stderr)

        except Exception as e:
            self.result_text.insert(tk.END, f"错误: {str(e)}\\n")
            self.status_var.set("失败")
            messagebox.showerror("错误", str(e))
'''

    # 写入文件
    (gui_dir / 'components' / 'simulation_tab.py').write_text(simulation_tab_content)
    print("创建最小化GUI完成")


if __name__ == "__main__":
    cleanup_project()
    create_minimal_working_gui()
    print("重建完成！现在运行: python adm1_gui.py")
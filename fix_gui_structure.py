# fix_gui_structure.py
"""
GUI结构修复脚本
"""

from pathlib import Path


def create_init_files():
    """创建正确的__init__.py文件"""
    print("创建__init__.py文件...")

    init_files = {
        'src/gui/__init__.py': '''
"""
GUI模块初始化文件
"""

from .widgets.main_window import ADM1MainWindow

__all__ = ['ADM1MainWindow']
''',

        'src/gui/components/__init__.py': '''
"""
组件模块初始化文件
"""

from .charts_tab import ChartsTab
from .help_tab import HelpTab
from .parameters_tab import ParametersTab
from .simulation_tab import SimulationTab

__all__ = ['ChartsTab', 'HelpTab', 'ParametersTab', 'SimulationTab']
''',

        'src/gui/utils/__init__.py': '''
"""
工具模块初始化文件
"""

from .chart_manager import ChartManager

__all__ = ['ChartManager']
''',

        'src/gui/widgets/__init__.py': '''
"""
小部件模块初始化文件
"""

from .main_window import ADM1MainWindow
from .chart_integration import ChartIntegration

__all__ = ['ADM1MainWindow', 'ChartIntegration']
'''
    }

    for file_path, content in init_files.items():
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip(), encoding='utf-8')
        print(f"✅ 创建文件: {file_path}")


def create_missing_files():
    """创建缺失的基础文件"""
    print("\n创建基础文件...")

    base_files = {
        'src/gui/components/charts_tab.py': '''
"""
图表标签页 - 基础版本
"""

import tkinter as tk
from tkinter import ttk

class ChartsTab:
    """图表标签页"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.create_widgets()

    def create_widgets(self):
        """创建控件"""
        label = ttk.Label(self.frame, text="图表功能 - 开发中", font=("Arial", 12))
        label.pack(expand=True, pady=50)
''',

        'src/gui/components/help_tab.py': '''
"""
帮助标签页 - 基础版本
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
        help_text = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        help_text.insert(tk.END, "帮助内容 - 开发中")
        help_text.config(state=tk.DISABLED)
''',

        'src/gui/components/parameters_tab.py': '''
"""
参数表格标签页 - 基础版本
"""

import tkinter as tk
from tkinter import ttk

class ParametersTab:
    """参数表格标签页"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.create_widgets()

    def create_widgets(self):
        """创建控件"""
        label = ttk.Label(self.frame, text="参数表格 - 开发中", font=("Arial", 12))
        label.pack(expand=True, pady=50)
''',

        'src/gui/components/simulation_tab.py': '''
"""
模拟控制标签页 - 基础版本
"""

import tkinter as tk
from tkinter import ttk

class SimulationTab:
    """模拟控制标签页"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(main_window.notebook)
        self.create_widgets()

    def create_widgets(self):
        """创建控件"""
        label = ttk.Label(self.frame, text="模拟控制 - 开发中", font=("Arial", 12))
        label.pack(expand=True, pady=50)
''',

        'src/gui/utils/chart_manager.py': '''
"""
图表管理器 - 基础版本
"""

class ChartManager:
    """图表管理器"""

    def __init__(self):
        pass
''',

        'src/gui/widgets/chart_integration.py': '''
"""
图表集成 - 基础版本
"""

class ChartIntegration:
    """图表集成"""

    def __init__(self):
        pass
''',

        'src/gui/widgets/main_window.py': '''
"""
主窗口 - 基础版本
"""

import tkinter as tk
from tkinter import ttk

class ADM1MainWindow:
    """ADM1主窗口"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """设置窗口"""
        self.root.title("ADM1 GUI")
        self.root.geometry("800x600")

    def create_widgets(self):
        """创建控件"""
        label = ttk.Label(self.root, text="ADM1 GUI - 基础框架运行成功！", font=("Arial", 14))
        label.pack(expand=True)

    def run(self):
        """运行"""
        self.root.mainloop()

def main():
    app = ADM1MainWindow()
    app.run()

if __name__ == "__main__":
    main()
'''
    }

    for file_path, content in base_files.items():
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip(), encoding='utf-8')
        print(f"✅ 创建文件: {file_path}")


def main():
    """主修复函数"""
    print("=" * 60)
    print("GUI结构修复工具")
    print("=" * 60)

    create_init_files()
    create_missing_files()

    print("\n" + "=" * 60)
    print("修复完成！")
    print("=" * 60)
    print("现在运行诊断脚本检查修复结果:")
    print("python diagnose_gui.py")
    print("\n如果诊断通过，运行GUI:")
    print("python adm1_gui.py")


if __name__ == "__main__":
    main()
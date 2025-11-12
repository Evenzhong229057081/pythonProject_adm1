# src/visualization/__init__.py
"""
可视化模块 - 修复导入问题
"""

import sys
from pathlib import Path

# 确保可以正确导入
def setup_visualization_paths():
    """设置可视化模块路径"""
    src_path = Path(__file__).parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

# 导出主要类
try:
    from .plot_manager import PlotManager
    from .result_visualizer import ResultVisualizer
    __all__ = ['PlotManager', 'ResultVisualizer']
except ImportError as e:
    print(f"可视化模块导入警告: {e}")
    __all__ = []
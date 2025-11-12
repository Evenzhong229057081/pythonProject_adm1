# check_visualization.py
"""
可视化模块检查工具
"""

import sys
from pathlib import Path


def check_visualization():
    """检查可视化模块"""
    print("=" * 60)
    print("🔍 可视化模块诊断")
    print("=" * 60)

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # 检查可视化模块文件
    vis_path = src_path / 'visualization'
    files = ['__init__.py', 'plot_manager.py', 'result_visualizer.py']

    print("📁 文件检查:")
    for file in files:
        file_path = vis_path / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 文件缺失")

    # 检查导入
    print("\n🔧 导入检查:")
    try:
        from visualization import PlotManager, ResultVisualizer
        print("✅ 可视化模块导入成功")

        # 测试类实例化
        try:
            plotter = PlotManager()
            visualizer = ResultVisualizer()
            print("✅ 类实例化成功")
            return True
        except Exception as e:
            print(f"❌ 类实例化失败: {e}")
            return False

    except ImportError as e:
        print(f"❌ 可视化模块导入失败: {e}")
        return False


def check_plot_dependencies():
    """检查绘图依赖"""
    print("\n📊 依赖检查:")
    try:
        import matplotlib
        print(f"✅ matplotlib: {matplotlib.__version__}")

        import numpy as np
        print(f"✅ numpy: {np.__version__}")

        import pandas as pd
        print(f"✅ pandas: {pd.__version__}")

        return True
    except ImportError as e:
        print(f"❌ 依赖缺失: {e}")
        return False


if __name__ == "__main__":
    success = check_visualization() and check_plot_dependencies()
    print("\n" + "=" * 60)
    if success:
        print("🎉 可视化模块检查通过")
    else:
        print("❌ 可视化模块存在问题")
    print("=" * 60)
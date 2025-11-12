"""
独立可视化脚本 - 单独控制图表显示
"""

import sys
from pathlib import Path

# 添加src到路径
src_path = Path(__file__).parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def main():
    """独立可视化工具"""
    print("=" * 50)
    print("ADM1独立可视化工具")
    print("=" * 50)

    print("功能说明:")
    print("  1. 从保存的结果文件重新生成图表")
    print("  2. 自定义图表样式和布局")
    print("  3. 批量生成多种图表格式")
    print("  4. 导出高质量图片")

    print("\n状态: 功能开发中")
    print("提示: 当前请使用主程序生成图表")

    # 示例：测试可视化模块导入
    try:
        from src.visualization.plot_manager import PlotManager
        print("SUCCESS: 可视化模块导入成功")
    except ImportError as e:
        print(f"ERROR: 可视化模块导入失败: {e}")


if __name__ == "__main__":
    main()
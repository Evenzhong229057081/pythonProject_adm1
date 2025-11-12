# adm1_gui.py
"""
ADM1 GUI启动器 - 主入口文件
修复Python路径问题，保持简洁风格
"""

import sys
import os
from pathlib import Path


def setup_environment():
    """设置运行环境"""
    # 获取项目根目录
    project_root = Path(__file__).parent

    # 添加src到路径（关键修复）
    src_path = project_root / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
        print(f"路径配置完成: {src_path}")

    # 设置工作目录
    os.chdir(project_root)

    # 创建输出目录
    Path('results').mkdir(exist_ok=True)
    Path('figures').mkdir(exist_ok=True)

    print("ADM1厌氧消化模型系统 - GUI版本")
    print(f"工作目录: {project_root}")
    print(f"Python版本: {sys.version.split()[0]}")
    print("环境设置完成")


def main():
    """主函数"""
    try:
        setup_environment()

        # 导入并启动GUI
        from gui.main_window import ADM1MainWindow
        print("GUI模块导入成功")

        app = ADM1MainWindow()
        app.run()

    except ImportError as e:
        print(f"GUI导入失败: {e}")
        print("可能的原因:")
        print("1. 文件结构不正确")
        print("2. __init__.py文件有问题")
        print("3. 模块依赖缺失")
        input("按回车键退出...")
    except Exception as e:
        print(f"GUI启动失败: {e}")
        input("按回车键退出...")


if __name__ == "__main__":
    main()
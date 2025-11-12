# check_modules.py
"""
模块检测工具 - 修复版
"""

import sys
from pathlib import Path


def check_module(module_path, class_name=None):
    """检查单个模块"""
    try:
        if class_name:
            # 检查类导入
            exec(f"from {module_path} import {class_name}")
            print(f"PASS {module_path}.{class_name}")
        else:
            # 检查模块导入
            exec(f"import {module_path}")
            print(f"PASS {module_path}")
        return True
    except Exception as e:
        print(f"FAIL {module_path}{'.' + class_name if class_name else ''}: {str(e)[:100]}")
        return False


def main():
    """主检测函数"""
    print("=" * 50)
    print("模块检测工具")
    print("=" * 50)

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # 检查核心模块
    modules_to_check = [
        # 核心模型
        ('core.adm1_model', 'ADM1Model'),
        ('solvers.ode_solver', 'ADM1Solver'),
        ('parameters.parameter_manager', 'ADM1ParameterManager'),

        # 界面模块
        ('interface.cli_interface', 'main'),  # 检查main函数

        # 补丁模块
        ('patches.environment_patch', 'apply_patch_and_run'),

        # 可视化模块
        ('visualization.result_visualizer', 'ResultVisualizer'),
        ('visualization.plot_manager', 'PlotManager'),
    ]

    success_count = 0
    total_count = len(modules_to_check)

    for module_path, class_name in modules_to_check:
        if check_module(module_path, class_name):
            success_count += 1

    print("\n" + "=" * 50)
    print(f"检测结果: {success_count}/{total_count} 通过")
    print("=" * 50)

    if success_count == total_count:
        print("所有模块正常")
    else:
        print("部分模块存在问题")


if __name__ == "__main__":
    main()
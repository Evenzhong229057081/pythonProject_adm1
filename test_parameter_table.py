# test_parameter_table.py
"""
独立测试参数表格功能
"""

import sys
from pathlib import Path


def test_parameter_table():
    """测试参数表格"""
    print("测试参数表格功能...")

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        from interface.parameter_table import ParameterTable
        print("✅ 参数表格模块导入成功")

        table = ParameterTable()
        print("✅ 参数表格实例化成功")

        table.display_parameter_table()
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


if __name__ == "__main__":
    test_parameter_table()
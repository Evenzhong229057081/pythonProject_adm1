# test_simulation_tab.py
"""
SimulationTab单元测试 - 隔离测试
"""

import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock


class TestSimulationTab(unittest.TestCase):
    """SimulationTab单元测试"""

    def setUp(self):
        """测试设置"""
        src_path = Path('src')
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

    def test_safe_bool_check(self):
        """测试安全布尔检查"""
        from gui.components.simulation_tab import SimulationTab

        # 创建模拟窗口
        mock_window = MagicMock()
        tab = SimulationTab(mock_window)

        # 测试各种类型的布尔值
        test_cases = [
            (True, True),
            (False, False),
            ([1, 2, 3], True),  # 非空列表
            ([], False),  # 空列表
            (np.array([True, False]), True),  # NumPy数组
            (np.array([]), False),  # 空数组
            ("hello", True),  # 非空字符串
            ("", False),  # 空字符串
            (None, False),  # None
            (0, False),  # 零
            (1, True),  # 非零
        ]

        for value, expected in test_cases:
            with self.subTest(value=value, expected=expected):
                result = tab._safe_bool_check(value)
                self.assertEqual(result, expected)

    def test_is_valid_results(self):
        """测试结果有效性检查"""
        from gui.components.simulation_tab import SimulationTab

        mock_window = MagicMock()
        tab = SimulationTab(mock_window)

        # 测试用例
        test_cases = [
            # (输入, 期望结果)
            (None, False),
            ({}, False),
            ({'time': [], 'states': [], 'success': True}, True),
            ({'time': [], 'states': []}, False),  # 缺少success
            ({'time': [], 'success': True}, False),  # 缺少states
            ({'states': [], 'success': True}, False),  # 缺少time
        ]

        for results, expected in test_cases:
            with self.subTest(results=results, expected=expected):
                result = tab._is_valid_results(results)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
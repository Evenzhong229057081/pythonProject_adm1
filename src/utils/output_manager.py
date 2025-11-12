# src/utils/output_manager.py
"""
统一输出管理器 - 专业无emoji版本
使用文本标识符替代表情符号，确保跨环境兼容性
"""

import sys
from pathlib import Path


class OutputManager:
    """专业输出管理器"""

    def __init__(self, mode="standard"):
        self.mode = mode
        # 使用文本标识符替代emoji
        self.indicators = {
            'success': '[SUCCESS]',
            'warning': '[WARNING]',
            'error': '[ERROR]',
            'info': '[INFO]',
            'progress': '[PROGRESS]',
            'module': '[MODULE]'
        }

        # 颜色配置（可选）
        self.colors = {
            'success': '\033[92m',
            'warning': '\033[93m',
            'error': '\033[91m',
            'info': '\033[94m',
            'end': '\033[0m'
        }

    def _colorize(self, text, color_type):
        """可选的颜色输出"""
        if sys.stdout.isatty() and color_type in self.colors:
            return f"{self.colors[color_type]}{text}{self.colors['end']}"
        return text

    def print_header(self, title, width=50):
        """打印章节标题"""
        print()
        print("=" * width)
        print(title)
        print("=" * width)

    def print_success(self, message):
        """成功消息"""
        print(f"{self.indicators['success']} {message}")

    def print_warning(self, message):
        """警告消息"""
        print(f"{self.indicators['warning']} {message}")

    def print_error(self, message):
        """错误消息"""
        print(f"{self.indicators['error']} {message}")

    def print_info(self, message):
        """信息消息"""
        print(f"{self.indicators['info']} {message}")

    def print_progress(self, message, current=None, total=None):
        """进度消息"""
        if current is not None and total is not None:
            progress = f"({current}/{total})"
            print(f"{self.indicators['progress']} {progress} {message}")
        else:
            print(f"{self.indicators['progress']} {message}")

    def print_module_status(self, module_name, success=True, details=None):
        """模块状态"""
        status = self.indicators['success'] if success else self.indicators['error']
        message = f"{status} {module_name}"
        if details:
            message += f" - {details}"
        print(message)

    def print_simulation_results(self, results, preset_name):
        """模拟结果报告"""
        if not results or not results.get('success'):
            self.print_error("模拟失败")
            return

        self.print_header("模拟结果摘要")
        print(f"预设名称: {preset_name}")
        print(f"时间点数: {len(results['time'])}")
        print(f"模拟时长: {results['time'][-1]:.1f} 天")
        print(f"状态变量: {results['states'].shape[0]} 个")
        print(f"数据维度: {results['states'].shape}")

        # 关键性能指标
        if hasattr(results.get('model'), 'state_variables'):
            print("\n关键变量变化:")
            key_vars = ['S_su', 'S_aa', 'S_ac', 'S_ch4', 'S_h2']
            for var in key_vars:
                idx = results['model'].get_variable_index(var)
                if idx != -1 and idx < results['states'].shape[0]:
                    initial = results['states'][idx, 0]
                    final = results['states'][idx, -1]
                    change = final - initial
                    print(f"  {var}: {initial:.4f} → {final:.4f} (Δ{change:+.4f})")


# 全局单例实例
_output_manager = None


def get_output_manager():
    """获取输出管理器实例"""
    global _output_manager
    if _output_manager is None:
        _output_manager = OutputManager()
    return _output_manager
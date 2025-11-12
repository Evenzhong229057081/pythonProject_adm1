# src/interface/__init__.py
"""
界面模块初始化 - 修复版
"""

from .cli_interface import main

# 移除不存在的 CLIInterface 导入
__all__ = ['main']
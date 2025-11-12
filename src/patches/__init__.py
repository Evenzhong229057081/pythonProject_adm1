# src/patches/__init__.py
"""
ADM1环境补丁模块
处理特定环境问题
"""

from .environment_patch import apply_patch, apply_patch_and_run

__all__ = ['apply_patch', 'apply_patch_and_run']
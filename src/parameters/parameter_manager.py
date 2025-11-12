"""
ADM1参数管理器 - 全新创建版本
完全避免编码问题
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class KineticParameters:
    """动力学参数"""
    k_dis: float = 0.5
    k_hyd_ch: float = 10.0
    k_hyd_pr: float = 10.0
    k_hyd_li: float = 10.0
    k_m_su: float = 30.0
    k_m_aa: float = 50.0
    k_m_fa: float = 6.0
    k_m_c4: float = 20.0
    k_m_pro: float = 13.0
    k_m_ac: float = 8.0
    k_m_h2: float = 35.0
    K_S_su: float = 0.5
    K_S_aa: float = 0.3
    K_S_fa: float = 0.4
    K_S_c4: float = 0.2
    K_S_pro: float = 0.1
    K_S_ac: float = 0.15
    K_S_h2: float = 7e-6
    Y_su: float = 0.1
    Y_aa: float = 0.08
    Y_fa: float = 0.06
    Y_c4: float = 0.06
    Y_pro: float = 0.04
    Y_ac: float = 0.05
    Y_h2: float = 0.06
    k_dec: float = 0.02

@dataclass
class MetalParameters:
    """金属参数"""
    k_edta_fe: float = 1.0e5
    k_precip_fes: float = 0.015
    KI_Fe: float = 0.001
    KI_Ni: float = 0.0005
    KI_Co: float = 0.0003

class ADM1ParameterManager:
    """ADM1参数管理器"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent
            self.config_path = project_root / 'config' / 'substrate_presets.json'
        else:
            self.config_path = Path(config_path)

        self.presets = {}
        self.current_preset = None
        self.load_presets()

    def load_presets(self) -> bool:
        """加载预设"""
        try:
            if not self.config_path.exists():
                logger.warning(f"配置文件不存在: {self.config_path}")
                return False

            with open(self.config_path, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)

            loaded_count = 0
            for preset_name, data in preset_data.items():
                self.presets[preset_name] = data
                loaded_count += 1
                logger.info(f"已加载预设: {preset_name}")

            return loaded_count > 0

        except Exception as e:
            logger.error(f"加载预设失败: {e}")
            return False

    def get_preset(self, preset_name: str) -> Optional[Dict]:
        """获取预设"""
        return self.presets.get(preset_name)

    def set_current_preset(self, preset_name: str) -> bool:
        """设置当前预设"""
        if preset_name in self.presets:
            self.current_preset = preset_name
            return True
        return False

    def get_current_parameters(self) -> Dict[str, Any]:
        """获取当前参数"""
        if not self.current_preset:
            return {}
        return self.presets.get(self.current_preset, {})

    def list_available_presets(self) -> List[str]:
        """列出可用预设"""
        return list(self.presets.keys())

    def get_preset_info(self, preset_name: str) -> Dict[str, Any]:
        """获取预设信息"""
        preset = self.get_preset(preset_name)
        if not preset:
            return {}
        return {
            'name': preset_name,
            'description': preset.get('description', ''),
            'parameters': preset.get('kinetic_parameters', {})
        }

def test_function():
    """测试函数"""
    manager = ADM1ParameterManager()
    presets = manager.list_available_presets()
    print(f"测试成功 - 可用预设: {presets}")
    return True

if __name__ == "__main__":
    test_function()

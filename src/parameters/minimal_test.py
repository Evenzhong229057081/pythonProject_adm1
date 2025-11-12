"""
最小化参数管理器 - 排除所有可能的编码问题
"""

class ADM1ParameterManager:
    def __init__(self):
        self.presets = ["food_waste", "sewage_sludge"]

    def list_available_presets(self):
        return self.presets

    def set_current_preset(self, preset_name):
        return preset_name in self.presets

# 测试代码
if __name__ == "__main__":
    manager = ADM1ParameterManager()
    print("测试成功:", manager.list_available_presets())

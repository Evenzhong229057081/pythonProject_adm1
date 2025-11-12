# debug_parameters.py
"""
参数调试脚本 - 找出数据获取失败的原因
"""

import sys
from pathlib import Path


def debug_parameter_access():
    """调试参数访问"""
    print("=" * 60)
    print("参数访问调试")
    print("=" * 60)

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        from patches.environment_patch import safe_import

        base_path = Path('src')

        # 导入模块
        ADM1Model = safe_import(base_path / 'core/adm1_model.py', 'ADM1Model')
        ADM1ParameterManager = safe_import(base_path / 'parameters/parameter_manager.py', 'ADM1ParameterManager')

        if not ADM1Model or not ADM1ParameterManager:
            print("❌ 模块导入失败")
            return False

        print("✅ 模块导入成功")

        # 创建实例
        model = ADM1Model()
        param_manager = ADM1ParameterManager()

        print("✅ 实例创建成功")

        # 测试参数管理器
        presets = param_manager.list_available_presets()
        print(f"可用预设: {presets}")

        if presets:
            preset_name = presets[0]
            print(f"使用预设: {preset_name}")

            # 设置预设
            success = param_manager.set_current_preset(preset_name)
            print(f"设置预设结果: {success}")

            # 获取参数
            params = param_manager.get_current_parameters()
            print(f"参数类型: {type(params)}")
            print(f"参数数量: {len(params) if params else 0}")

            if params:
                print("\n前5个参数:")
                for i, (key, value) in enumerate(params.items()):
                    if i < 5:
                        print(f"  {key}: {value}")

            # 测试模型
            print(f"\n模型状态变量数量: {len(model.state_variables)}")
            print(f"初始条件数量: {len(model.initial_conditions)}")

            print("\n前5个状态变量和初始值:")
            for i in range(min(5, len(model.state_variables))):
                var = model.state_variables[i]
                val = model.initial_conditions[i] if i < len(model.initial_conditions) else "N/A"
                print(f"  {var}: {val}")

            return True
        else:
            print("❌ 无可用预设")
            return False

    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    debug_parameter_access()
# quick_test.py
"""
快速功能测试 - 无emoji版
"""

import sys
from pathlib import Path


def test_core_functionality():
    """测试核心功能"""
    print("=" * 50)
    print("核心功能测试")
    print("=" * 50)

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        # 测试补丁导入
        from patches.environment_patch import safe_import
        base_path = Path('src')

        # 测试导入核心模块
        modules = {}
        test_modules = [
            ('core/adm1_model.py', 'ADM1Model'),
            ('solvers/ode_solver.py', 'ADM1Solver'),
            ('parameters.parameter_manager.py', 'ADM1ParameterManager')
        ]

        for module_path, class_name in test_modules:
            module = safe_import(base_path / module_path, class_name)
            if module:
                modules[class_name] = module
                print(f"PASS {class_name} 导入成功")
            else:
                print(f"FAIL {class_name} 导入失败")
                return False

        # 测试模拟运行
        print("\n测试模拟运行...")
        ADM1Model, ADM1Solver, ADM1ParameterManager = modules.values()

        model = ADM1Model()
        solver = ADM1Solver()
        param_manager = ADM1ParameterManager()

        presets = param_manager.list_available_presets()
        if presets:
            print(f"PASS 预设加载成功: {presets}")

            # 快速测试
            t_span = (0, 5)  # 缩短测试时间
            y0 = model.initial_conditions

            results = solver.solve(model, t_span, y0)
            if results['success']:
                print(f"PASS 模拟测试成功: {len(results['time'])} 时间点")
                return True
            else:
                print(f"FAIL 模拟测试失败: {results['message']}")
                return False
        else:
            print("FAIL 无可用预设")
            return False

    except Exception as e:
        print(f"FAIL 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    if test_core_functionality():
        print("\n核心功能测试通过")
    else:
        print("\n核心功能测试失败")


if __name__ == "__main__":
    main()
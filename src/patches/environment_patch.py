# patches/environment_patch.py
"""
环境补丁模块 - 修复函数缺失问题
"""

import sys
from pathlib import Path


def apply_patch(return_results=False):
    """
    apply_patch函数 - 添加缺失的函数
    这是GUI代码期望导入的函数
    """
    return apply_patch_and_run(return_results)


def apply_patch_and_run(return_results=False):
    """应用补丁并运行模拟"""
    try:
        # 添加当前目录到路径
        base_path = Path(__file__).parent.parent
        if str(base_path) not in sys.path:
            sys.path.insert(0, str(base_path))

        # 导入核心模块
        from core.adm1_model import ADM1Model
        from solvers.ode_solver import ADM1Solver
        from parameters.parameter_manager import ADM1ParameterManager

        # 初始化组件
        model = ADM1Model()
        solver = ADM1Solver()
        param_manager = ADM1ParameterManager()

        # 获取预设
        presets = param_manager.list_available_presets()
        if not presets:
            if return_results:
                return {'success': False, 'message': '无可用预设'}
            else:
                print("错误: 无可用预设")
                return

        preset_name = presets[0]
        param_manager.set_current_preset(preset_name)

        # 运行模拟
        t_span = (0, 30)
        y0 = model.initial_conditions

        results = solver.solve(model, t_span, y0)

        if return_results:
            # 返回模式：返回完整结果供GUI使用
            results['preset_name'] = preset_name
            results['model'] = model
            return results
        else:
            # 原有逻辑
            if results.get('success'):
                print("模拟成功完成")
                print(f"时间点数: {len(results['time'])}")
                print(f"状态变量: {results['states'].shape[0]}个")
            else:
                print(f"模拟失败: {results.get('message')}")
            return results

    except Exception as e:
        if return_results:
            return {'success': False, 'message': f'运行失败: {str(e)}'}
        else:
            print(f"运行失败: {e}")
            return None


# 保持向后兼容
def main(return_results=False):
    """主函数 - 用于直接运行"""
    return apply_patch_and_run(return_results)


if __name__ == "__main__":
    apply_patch_and_run()
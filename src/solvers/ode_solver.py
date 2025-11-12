"""
ADM1微分方程求解器 - 修复导入问题版本
处理刚性系统的数值求解
"""

import sys
import os
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, Tuple, Optional

# 修复导入路径问题：添加项目根目录到Python路径
project_root = Path(__file__).parent.parent  # 获取项目根目录
sys.path.insert(0, str(project_root))  # 添加到Python路径

class ADM1Solver:
    """ADM1微分方程求解器"""

    def __init__(self, solver_params: Dict = None):
        # 默认求解参数（针对刚性系统优化）
        self.solver_params = solver_params or {
            'method': 'BDF',       # 刚性系统首选方法
            'rtol': 1e-6,          # 相对容差
            'atol': 1e-8,          # 绝对容差
            'max_step': 0.1,       # 最大步长
            'first_step': 0.01     # 初始步长
        }

    def solve(self, model, t_span: Tuple[float, float], y0: np.ndarray = None) -> Dict:
        """
        求解ADM1微分方程系统

        Args:
            model: ADM1模型实例
            t_span: 时间范围 (开始, 结束)
            y0: 初始条件向量

        Returns:
            包含求解结果的字典
        """
        if y0 is None:
            y0 = model.initial_conditions

        def ode_system(t: float, y: np.ndarray) -> np.ndarray:
            """定义ODE系统右手边函数"""
            # 计算总变化率 = 生化反应 + 物理化学过程
            return model.biochemical_reactions(t, y)

        # 使用SciPy求解器
        try:
            solution = solve_ivp(
                fun=ode_system,
                t_span=t_span,
                y0=y0,
                method=self.solver_params['method'],
                rtol=self.solver_params['rtol'],
                atol=self.solver_params['atol'],
                max_step=self.solver_params['max_step'],
                first_step=self.solver_params.get('first_step', None),
                dense_output=True
            )

            return {
                'time': solution.t,
                'states': solution.y,
                'success': solution.success,
                'message': solution.message,
                'nfev': solution.nfev,  # 函数调用次数
                'njev': solution.njev,   # 雅可比调用次数
                'model': model
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"求解失败: {str(e)}",
                'time': np.array([]),
                'states': np.array([]),
                'model': model
            }

def simple_test():
    """简化测试函数 - 避免复杂的导入依赖"""
    print("=== ADM1求解器简化测试 ===")

    # 创建一个简单的测试模型类
    class SimpleTestModel:
        def __init__(self):
            self.initial_conditions = np.array([1.0, 0.5, 0.1])  # 简化初始条件
            self.state_variables = ['S_su', 'S_ac', 'S_ch4']  # 简化状态变量

        def biochemical_reactions(self, t, y):
            """简化的生化反应函数 - 用于测试"""
            # 简单的线性衰减模型用于测试
            return -0.1 * y  # 所有变量以0.1/d的速率衰减

        def get_variable_index(self, var_name):
            """获取变量索引"""
            if var_name in self.state_variables:
                return self.state_variables.index(var_name)
            return -1

    # 测试求解器基本功能
    model = SimpleTestModel()
    solver = ADM1Solver()

    print("✅ 模型和求解器初始化成功")
    print(f"初始条件: {model.initial_conditions}")
    print(f"状态变量: {model.state_variables}")

    # 运行短期模拟（0.1天）
    results = solver.solve(model, (0, 0.1), model.initial_conditions)

    print(f"求解状态: {'成功' if results['success'] else '失败'}")
    if results['success']:
        print(f"时间点数: {len(results['time'])}")
        print(f"状态矩阵形状: {results['states'].shape}")
        print(f"函数调用次数: {results['nfev']}")

        # 显示变量变化
        for i, var in enumerate(model.state_variables):
            initial = results['states'][i, 0]
            final = results['states'][i, -1]
            change = final - initial
            print(f"{var}: {initial:.4f} → {final:.4f} (变化: {change:+.4f})")
    else:
        print(f"错误信息: {results['message']}")

    return results

def test_import_path():
    """测试导入路径是否正确"""
    print("=== 导入路径测试 ===")

    # 测试能否导入核心模块
    try:
        from src.core.adm1_model import ADM1Model
        print("✅ 成功导入 ADM1Model (src.core.adm1_model)")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")

    # 测试备用导入路径
    try:
        from core.adm1_model import ADM1Model
        print("✅ 成功导入 ADM1Model (core.adm1_model)")
        return True
    except ImportError as e:
        print(f"❌ 备用导入失败: {e}")

    # 显示当前Python路径
    print("\n当前Python路径:")
    for i, path in enumerate(sys.path[:5]):  # 只显示前5个路径
        print(f"  {i+1}. {path}")

    return False

if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 简化测试（推荐先运行）")
    print("2. 导入路径测试")
    print("3. 完整模型测试")

    choice = input("请输入选择 (1-3): ").strip()

    if choice == "1":
        # 运行简化测试
        simple_test()

    elif choice == "2":
        # 测试导入路径
        test_import_path()

    elif choice == "3":
        # 尝试完整模型测试
        try:
            from src.core.adm1_model import ADM1Model

            print("=== ADM1完整模型测试 ===")
            model = ADM1Model()
            solver = ADM1Solver()

            # 运行短期模拟
            results = solver.solve(model, (0, 1), model.initial_conditions)

            print(f"求解状态: {'成功' if results['success'] else '失败'}")
            if results['success']:
                print(f"时间点数: {len(results['time'])}")
                print(f"状态矩阵: {results['states'].shape}")
        except ImportError as e:
            print(f"❌ 无法导入完整模型: {e}")
            print("请先运行简化测试或导入路径测试")
    else:
        print("无效选择，运行简化测试")
        simple_test()
#!/usr/bin/env python3
"""
ADM1项目结构自动化生成脚本
运行后会自动创建标准项目结构
"""

import os
from pathlib import Path


def create_project_structure(base_path="."):
    """创建ADM1标准项目结构"""

    # 定义需要创建的目录结构
    dir_structure = [
        "src/__init__.py",
        "src/core/__init__.py",
        "src/solvers/__init__.py",
        "src/utils/__init__.py",
        "src/visualization/__init__.py",
        "src/interface/__init__.py",
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "examples/basic/__init__.py",
        "examples/advanced/__init__.py",
        "data/input/.gitkeep",
        "data/output/.gitkeep",
        "config/__init__.py",
        "docs/references/.gitkeep"
    ]

    # 创建目录和文件
    for path in dir_structure:
        full_path = Path(base_path) / path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if path.endswith(".py"):
            full_path.touch()
            print(f"创建文件: {full_path}")
        else:
            full_path.touch()
            print(f"创建占位文件: {full_path}")

    # 创建核心模板文件
    core_files = {
        "src/core/adm1_model.py": """\"\"\"
ADM1核心模型定义
包含26个状态变量和19个生化过程
\"\"\"

class ADM1Model:
    \"\"\"ADM1模型主类\"\"\"

    def __init__(self):
        self.state_variables = [
            'S_su', 'S_aa', 'S_fa', 'S_va', 'S_bu', 'S_pro', 
            'S_ac', 'S_h2', 'S_ch4', 'S_IC', 'S_IN', 'S_I'
            # ...其他变量
        ]

    def biochemical_reactions(self, t, y):
        \"\"\"计算生化反应速率\"\"\"
        pass
""",
        "src/solvers/ode_solver.py": """\"\"\"
ADM1微分方程求解器
\"\"\"

from scipy.integrate import solve_ivp

class ADM1Solver:
    \"\"\"ADM1求解器类\"\"\"

    def solve(self, model, t_span, y0):
        \"\"\"求解ADM1系统\"\"\"
        pass
""",
        "src/main.py": """\"\"\"
ADM1程序主入口
\"\"\"

from core.adm1_model import ADM1Model
from solvers.ode_solver import ADM1Solver

def main():
    \"\"\"主函数\"\"\"
    model = ADM1Model()
    solver = ADM1Solver()

    # 模拟参数
    t_span = (0, 30)  # 30天模拟
    y0 = model.initial_conditions

    # 求解
    solution = solver.solve(model, t_span, y0)

if __name__ == "__main__":
    main()
"""
    }

    # 写入核心模板文件
    for file_path, content in core_files.items():
        full_path = Path(base_path) / file_path
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"创建模板文件: {full_path}")


if __name__ == "__main__":
    print("=== ADM1项目结构生成器 ===")
    create_project_structure()
    print("项目结构创建完成！")
    print("完成后可删除本脚本")

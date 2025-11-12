# fix_u2023.py
"""
修复U+2023非法字符问题
"""

import os
from pathlib import Path


def find_and_fix_u2023():
    """查找并修复U+2023字符"""
    print("开始查找并修复U+2023字符...")

    # 查找所有__init__.py文件
    problem_files = []

    for init_file in Path('.').rglob('__init__.py'):
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否包含U+2023字符
            if '\u2023' in content:
                print(f"发现U+2023字符: {init_file}")
                problem_files.append(init_file)

                # 备份文件
                backup_path = str(init_file) + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已创建备份: {backup_path}")

                # 修复字符
                fixed_content = content.replace('\u2023', '#')
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

                print(f"修复完成: 将U+2023替换为#")

        except Exception as e:
            print(f"检查文件失败 {init_file}: {e}")

    return problem_files


def check_specific_files():
    """检查特定的问题文件"""
    suspect_files = [
        "src/inputs/__init__.py",
        "src/parameters/__init__.py",
        "tests/parameters/__init__.py"
    ]

    print("检查特定文件...")
    for file_path in suspect_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline()
                    print(f"检查文件: {file_path}")
                    print(f"第一行: {repr(first_line)}")
                    if '\u2023' in first_line:
                        print("*** 发现U+2023字符 ***")
                    print("-" * 50)
            except Exception as e:
                print(f"检查失败 {file_path}: {e}")


def main():
    """主函数"""
    print("=== 修复U+2023字符问题 ===")

    # 检查特定文件
    check_specific_files()

    # 查找并修复所有文件
    problem_files = find_and_fix_u2023()

    if problem_files:
        print(f"修复完成: 处理了 {len(problem_files)} 个文件")
        for f in problem_files:
            print(f"  - {f}")
    else:
        print("未发现U+2023字符")

    # 验证修复
    print("\n验证修复...")
    verify_fix()


def verify_fix():
    """验证修复结果"""
    try:
        # 尝试导入可能出问题的模块
        import src.inputs
        import src.parameters
        print("✅ 模块导入成功")
        return True
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False


if __name__ == "__main__":
    main()
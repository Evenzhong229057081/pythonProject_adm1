# check_encoding_fixed.py
"""
检查文件编码问题 - 修复版本
"""

import os
from pathlib import Path


def check_file_encoding(file_path):
    """检查单个文件的编码问题"""
    try:
        with open(file_path, 'rb') as f:
            first_bytes = f.read(10)

        print("分析文件: " + str(file_path))
        print("前10字节: " + first_bytes.hex())

        # 检查常见问题字节
        if first_bytes.startswith(b'\xef\xbb\xbf'):
            print("问题: 发现UTF-8 BOM标记")
            return 'bom'
        elif first_bytes.startswith(b'\xff'):
            print("问题: 发现0xFF字节开头")
            return '0xff'
        elif b'\x00' in first_bytes:
            print("问题: 发现空字节")
            return 'null_byte'
        else:
            print("状态: 文件开头正常")
            return 'normal'

    except Exception as e:
        print("错误: 读取失败 - " + str(e))
        return 'error'


def main():
    """主函数"""
    print("开始检查项目中的__init__.py文件...")

    problem_files = []
    checked_count = 0

    # 检查所有__init__.py文件
    for init_file in Path('.').rglob('__init__.py'):
        result = check_file_encoding(init_file)
        checked_count += 1

        if result != 'normal':
            problem_files.append((str(init_file), result))

        print("-" * 50)

    # 输出结果
    print("\n检查完成:")
    print("已检查文件数: " + str(checked_count))
    print("发现问题文件: " + str(len(problem_files)))

    if problem_files:
        print("有问题的文件:")
        for file_path, issue in problem_files:
            print("  - " + file_path + " : " + issue)
    else:
        print("所有文件正常")


if __name__ == "__main__":
    main()
# fix_ff_bytes.py
"""
修复0xFF字节开头问题
"""

import os
from pathlib import Path


def fix_ff_byte(file_path):
    """修复单个文件的0xFF字节问题"""
    try:
        print("修复文件: " + str(file_path))

        # 备份原文件
        backup_path = file_path + ".backup"
        with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        print("已创建备份: " + backup_path)

        # 读取原始字节
        with open(file_path, 'rb') as f:
            content = f.read()

        # 检查并移除0xFF FE（UTF-16 LE BOM）
        if content.startswith(b'\xff\xfe'):
            print("发现UTF-16 LE BOM，正在移除...")
            content = content[2:]
        # 检查并移除0xFE FF（UTF-16 BE BOM）
        elif content.startswith(b'\xfe\xff'):
            print("发现UTF-16 BE BOM，正在移除...")
            content = content[2:]
        # 检查单独的0xFF字节
        elif content.startswith(b'\xff'):
            print("发现0xFF字节开头，正在修复...")
            content = content[1:]

        # 尝试解码为UTF-16，然后转换为UTF-8
        try:
            # 尝试UTF-16解码
            text_content = content.decode('utf-16')
            print("成功以UTF-16解码")
        except UnicodeDecodeError:
            try:
                # 尝试UTF-8解码
                text_content = content.decode('utf-8')
                print("成功以UTF-8解码")
            except UnicodeDecodeError:
                # 最后尝试latin-1
                text_content = content.decode('latin-1')
                print("使用latin-1解码")

        # 保存为UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text_content)

        print("修复成功")
        return True

    except Exception as e:
        print("修复失败: " + str(e))
        return False


def main():
    """主函数"""
    problem_files = [
        "src/inputs/__init__.py",
        "src/parameters/__init__.py",
        "tests/parameters/__init__.py"
    ]

    fixed_count = 0
    for file_path in problem_files:
        if Path(file_path).exists():
            if fix_ff_byte(file_path):
                fixed_count += 1
        else:
            print("文件不存在: " + file_path)

    print("修复完成: " + str(fixed_count) + "/" + str(len(problem_files)) + " 个文件")


if __name__ == "__main__":
    main()
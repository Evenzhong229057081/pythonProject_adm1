# fix_gb2312_encoding.py
"""
专门修复GB2312编码问题
"""


def fix_gb2312_encoding():
    """修复GB2312编码问题"""
    file_path = "src/gui/components/simulation_tab.py"

    print("开始修复GB2312编码问题...")

    # 备份原文件
    backup_path = file_path + ".gb2312.backup"
    with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
        dst.write(src.read())
    print(f"已创建备份: {backup_path}")

    try:
        # 以GB2312编码读取
        with open(file_path, 'r', encoding='gb2312') as f:
            content = f.read()
        print("✅ 成功以GB2312编码读取文件")

        # 检查中文字符
        chinese_chars = []
        for char in content:
            if '\u4e00' <= char <= '\u9fff':  # 中文字符范围
                chinese_chars.append(char)

        if chinese_chars:
            print(f"发现中文字符: {set(chinese_chars)}")
        else:
            print("未发现中文字符")

        # 保存为UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 文件已转换为UTF-8编码")

        return True

    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False


def verify_fix():
    """验证修复结果"""
    file_path = "src/gui/components/simulation_tab.py"

    try:
        # 尝试以UTF-8读取
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ UTF-8编码验证成功")

        # 检查文件内容
        lines = content.split('\n')
        print(f"文件行数: {len(lines)}")
        print("前5行内容:")
        for i, line in enumerate(lines[:5], 1):
            print(f"{i}: {line[:100]}")  # 显示前100个字符

        return True

    except UnicodeDecodeError as e:
        print(f"❌ UTF-8验证失败: {e}")
        return False


if __name__ == "__main__":
    if fix_gb2312_encoding():
        print("\n修复完成，开始验证...")
        if verify_fix():
            print("\n🎉 修复验证成功！")
        else:
            print("\n❌ 修复验证失败")
    else:
        print("\n❌ 修复失败")
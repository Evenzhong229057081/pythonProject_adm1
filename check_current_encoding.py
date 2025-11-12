# check_current_encoding.py
"""
检查当前文件编码状态
"""

import chardet


def analyze_file(file_path):
    """详细分析文件编码"""
    with open(file_path, 'rb') as f:
        content = f.read()

    print(f"\n=== 分析文件: {file_path} ===")
    print(f"文件大小: {len(content)} 字节")
    print(f"开头16字节: {content[:16].hex()}")

    # 检测编码
    result = chardet.detect(content)
    print(f"检测编码: {result['encoding']}")
    print(f"置信度: {result['confidence']:.2f}")

    # 检查特定问题字节
    if b'\xc4' in content:
        positions = [i for i, b in enumerate(content) if b == 0xc4]
        print(f"发现0xC4字节在位置: {positions[:5]}...")  # 显示前5个位置

    # 尝试读取第2行
    try:
        lines = content.split(b'\n')
        if len(lines) > 1:
            line2 = lines[1]
            print(f"第2行内容: {line2}")
            print(f"第2行解码尝试: {line2.decode('utf-8', errors='replace')}")
    except:
        pass


# 分析问题文件
analyze_file("src/gui/components/simulation_tab.py")
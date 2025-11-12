# test_gui.py
"""
GUI测试脚本
"""

import sys
from pathlib import Path


def test_gui():
    """测试GUI启动"""
    print("测试GUI启动...")

    # 添加src到路径
    src_path = Path('src')
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        from gui.main_window import ADM1MainWindow
        print("✅ GUI模块导入成功")

        # 创建简单测试窗口
        import tkinter as tk
        root = tk.Tk()
        root.title("GUI测试")
        root.geometry("400x300")

        label = tk.Label(root, text="GUI测试成功！", font=("Arial", 14))
        label.pack(expand=True)

        button = tk.Button(root, text="关闭", command=root.destroy)
        button.pack(pady=10)

        print("✅ GUI测试窗口创建成功")
        print("如果看到窗口显示，说明GUI环境正常")

        root.mainloop()
        return True

    except Exception as e:
        print(f"❌ GUI测试失败: {e}")
        return False


if __name__ == "__main__":
    test_gui()
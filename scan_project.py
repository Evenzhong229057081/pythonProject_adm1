import os
from pathlib import Path
import json


class ProjectScanner:
    def __init__(self, root_path='.'):
        self.root_path = Path(root_path)
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'file_types': {},
            'dir_structure': {}
        }
        self.exclude_dirs = {'.git', '__pycache__', '.idea', 'venv', 'env', '.vscode', 'node_modules'}
        self.exclude_files = {'.DS_Store', 'thumbs.db'}

    def scan(self):
        """执行扫描"""
        print(f"🔍 扫描项目: {self.root_path.absolute()}")
        print("=" * 60)

        structure = self._scan_directory(self.root_path)
        self._print_summary()

        return structure

    def _scan_directory(self, path, depth=0):
        """递归扫描目录"""
        if depth == 0:
            current_structure = {
                'name': path.name,
                'type': 'directory',
                'path': str(path),
                'children': []
            }
        else:
            current_structure = {
                'name': path.name,
                'type': 'directory',
                'children': []
            }

        try:
            items = list(path.iterdir())

            # 先处理目录
            dirs = [item for item in items if item.is_dir() and item.name not in self.exclude_dirs]
            dirs.sort(key=lambda x: x.name.lower())

            # 再处理文件
            files = [item for item in items if item.is_file() and item.name not in self.exclude_files]
            files.sort(key=lambda x: x.name.lower())

            # 统计目录
            self.stats['total_dirs'] += len(dirs)

            # 处理子目录
            for dir_path in dirs:
                child_structure = self._scan_directory(dir_path, depth + 1)
                current_structure['children'].append(child_structure)

            # 处理文件
            for file_path in files:
                file_info = {
                    'name': file_path.name,
                    'type': 'file',
                    'extension': file_path.suffix.lower(),
                    'size': file_path.stat().st_size
                }
                current_structure['children'].append(file_info)

                # 统计文件类型
                ext = file_path.suffix.lower() or '无扩展名'
                self.stats['file_types'][ext] = self.stats['file_types'].get(ext, 0) + 1
                self.stats['total_files'] += 1

        except PermissionError:
            current_structure['error'] = '权限不足'

        return current_structure

    def _print_summary(self):
        """打印统计摘要"""
        print("\n" + "=" * 60)
        print("📊 项目统计摘要")
        print("=" * 60)
        print(f"📁 总目录数: {self.stats['total_dirs']}")
        print(f"📄 总文件数: {self.stats['total_files']}")
        print("\n📋 文件类型分布:")
        for ext, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {ext if ext else '无扩展名'}: {count} 个")

    def export_json(self, filename='project_structure.json'):
        """导出为JSON文件"""
        structure = self._scan_directory(self.root_path)
        data = {
            'project_root': str(self.root_path.absolute()),
            'scan_stats': self.stats,
            'structure': structure
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 项目结构已导出到: {filename}")
        return filename


def print_simple_tree():
    """简单的树状结构打印"""

    def print_tree(path, prefix="", is_last=True):
        """递归打印树状结构"""
        name = path.name if path != Path('.') else Path('.').absolute().name

        if path.is_dir():
            # 打印目录
            connector = "└── " if is_last else "├── "
            print(prefix + connector + "📁 " + name + "/")

            # 新的前缀
            new_prefix = prefix + ("    " if is_last else "│   ")

            try:
                # 获取子项
                items = list(path.iterdir())
                items = [item for item in items
                         if item.name not in ['.git', '__pycache__', '.idea', 'venv', 'env']
                         and not item.name.startswith('.')]

                # 排序：目录在前，文件在后
                dirs = [item for item in items if item.is_dir()]
                files = [item for item in items if item.is_file()]
                dirs.sort(key=lambda x: x.name.lower())
                files.sort(key=lambda x: x.name.lower())
                items_sorted = dirs + files

                # 递归打印
                for i, item in enumerate(items_sorted):
                    print_tree(item, new_prefix, i == len(items_sorted) - 1)

            except PermissionError:
                print(new_prefix + "└── ⚠️ 无权限访问")

        else:
            # 打印文件
            connector = "└── " if is_last else "├── "
            # 文件图标
            if path.suffix.lower() == '.py':
                icon = "🐍"
            elif path.suffix.lower() in ['.md', '.txt']:
                icon = "📄"
            elif path.suffix.lower() in ['.json', '.yaml']:
                icon = "⚙️"
            else:
                icon = "📄"
            print(prefix + connector + icon + " " + name)

    print("🌳 项目目录树:")
    print_tree(Path('.'))


if __name__ == "__main__":
    # 使用示例
    print("选择扫描模式:")
    print("1. 简单树状结构")
    print("2. 详细统计扫描")

    choice = input("请输入选择 (1/2): ").strip()

    if choice == "1":
        print_simple_tree()
    elif choice == "2":
        scanner = ProjectScanner('.')
        scanner.scan()

        # 可选导出
        export = input("\n是否导出为JSON文件？(y/n): ").lower().strip()
        if export == 'y':
            scanner.export_json()
    else:
        print_simple_tree()  # 默认使用简单模式
import os.path
import json
import h5py

"""Input opend file and initial path of tree node that start to write file tree."""


class ExportTree:
    """
    Export the hierarchical structure of an h5 file to a JSON format.
    You can specify the starting path like '/folder1/folder2/item' to begin from a particular node.
    If no path is provided, the export starts from the root directory by default.
    """
    def __init__(self, file, save_path, initial_path=None):
        self.file = file
        self.save_path = save_path
        self.initial_path = initial_path
        self.data = None

    def export_tree_to_json(self):
        if self.initial_path is None:
            parent_text = os.path.basename(self.file.filename)
            parent_path = ''
        else:
            parent_text = self.initial_path
            parent_path = self.initial_path

        self.data = self.get_children_item(parent_text, parent_path, level=0)

        with open(self.save_path, 'w') as f:  # if not exist, create one
            json.dump(self.data, f, indent=4)

    def get_children_item(self, text, path, level):
        # save parent data
        data = {
            'text': text,
            'path': path,
            'level': level,
            'children': []
        }

        try:
            if path == '':
                keys = self.file.keys()
            else:
                keys = self.file[path].keys()

            for key in keys:
                child_path = f'{path}/{key}'
                child_data = self.get_children_item(key, child_path, level=level + 1)
                data['children'].append(child_data)
        except Exception as e:
            pass

        return data


def import_tree(filepath):
    """
    import data from a json file
    :param filepath: path of an h5 file
    :return: data in JSON format
    """
    with open(filepath, 'r') as f:  # if not exist, create one
        data = json.load(f)
    return data


def print_tree_from_traget_node(data, node_path, level=0):
    # 检查当前节点的路径是否匹配
    if data['path'] == node_path or node_path is None:
        print('|' + '--' * level + '| ' + data['text'])

        # 如果有 children，则递归打印每个子项
        for child in data.get('children', []):
            print_tree(child, level + 1)
        return  # 找到目标后返回，不再继续遍历

    # 继续查找子项
    for child in data.get('children', []):
        print_tree_from_traget_node(child, node_path, level)


def print_tree(node, level, end='\n'):
    # 打印当前节点
    print('|' + '--' * level + '| ' + node['text'], end=end)

    # 递归打印每个子项
    for child in node.get('children', []):
        if 'children' not in child or not child['children']:
            # 打印没有子项的节点及其路径
            print_tree(child, level + 1, '')
            print('  ' * 5 + '<path>' + child['path'])
        else:
            print_tree(child, level + 1, '\n')


def find_items_by_level_and_text(tree_data, level, text_condition):
    """根据指定的层级和文本条件查找项"""
    results = []
    _find_items_recursive(tree_data, level, text_condition, results)
    return results


def _find_items_recursive(node, target_level, text_condition, results):
    """递归遍历树，查找满足条件的节点"""
    # 如果当前节点的 level 等于目标 level，且 text 满足条件，则加入结果
    if node['level'] == target_level and text_condition(node['text']):
        results.append(node['path'])

    # 递归遍历子节点
    for child in node.get('children', []):
        _find_items_recursive(child, target_level, text_condition, results)


if __name__ == '__main__':
    # h5文件路径
    file_path = r'C:\Users\a1033\Desktop\Contemporary\20240620\2024-05-31.h5'

    # 读取h5文件
    f = h5py.File(file_path, "r")

    # json保存路径
    save_path = r'/test\pass\output2.json'

    # 保存json
    # exportTree = ExportTree(f, save_path, initial_path=None)
    # exportTree.export_tree_to_json()

    # 从路径中读取json
    json_path = save_path
    with open(json_path, "r") as f:
        # 调用函数，返回文件树中，满足条件text_condition的项
        results = find_items_by_level_and_text(
            tree_data=json.load(f),
            level=1,
            text_condition=lambda text: 'Particle' in text and 'Scanner' not in text
                                        and text not in [f'Particle_{i}' for i in range(5)]
        )

    # 打印这些项的text字段
    for item in results:
        print(item['text'])

    # save_fullpath = r'D:\GitProject\SpectraPro\test\data_processing\20240925\tree'
    # for key in f.keys():
    #     if key != 'nplab_log':
    #         parent_path = f'/{key}'
    #         save_name = fr'{save_fullpath}\{key}.txt'
    #         with open(save_name, 'w') as f:
    #             # 重定向标准输出
    #             sys.stdout = f
    #             print_tree_from_traget_node(tree_data, parent_path)

import os.path
import json
import h5py
import pprint
import sys


class DealWithH5:
    def __init__(self, file, initial_path=None):
        self.file = file
        self.initial_path = initial_path
        self.data = None

    def save_keys_of_h5(self):
        if self.initial_path is None:
            parent_text = os.path.basename(self.file.filename)
            parent_path = ''
        else:
            parent_text = self.initial_path
            parent_path = self.initial_path

        self.data = self.get_children_key(parent_text, parent_path)

        with open('../../tests/pass/output.json', 'w') as f:  # if not exist, create one
            json.dump(self.data, f, indent=4)

    def get_children_key(self, text, path):
        # save parent data
        data = {
            'text': text,
            'path': path,
            'children': []
        }

        try:
            if path == '':
                keys = self.file.keys()
            else:
                keys = self.file[path].keys()

            for key in keys:
                child_path = f'{path}/{key}'
                child_data = self.get_children_key(key, child_path)
                data['children'].append(child_data)
        except Exception as e:
            pass

        return data

    def read_keys_of_h5(self):
        with open('../../tests/pass/output.json', 'r') as f:  # if not exist, create one
            data = json.load(f)
        return data


def find_and_print_tree(data, target_path, level=0):
    # 检查当前节点的路径是否匹配
    if data['path'] == target_path:
        print('|' + '--' * level + '| ' + data['text'])

        # 如果有 children，则递归打印每个子项
        for child in data.get('children', []):
            print_tree(child, level + 1)
        return  # 找到目标后返回，不再继续遍历

    # 继续查找子项
    for child in data.get('children', []):
        find_and_print_tree(child, target_path, level)


def print_tree(node, level, end='\n'):
    # 打印当前节点
    print('|' + '--' * level + '| ' + node['text'], end=end)

    # 递归打印每个子项
    for child in node.get('children', []):
        if 'children' not in child or not child['children']:
            # 打印没有子项的节点及其路径
            print_tree(child, level + 1, '')
            print('  '*5 + '<path>' + child['path'])
        else:
            print_tree(child, level + 1, '\n')


if __name__ == '__main__':
    file_path = r'C:\Users\a1033\Desktop\Contemporary\20240620\2024-05-31.h5'
    f = h5py.File(file_path, "r")
    dealWithH5 = DealWithH5(f, initial_path=None)
    tree_data = dealWithH5.read_keys_of_h5()

    save_fullpath = r'D:\GitProject\SpectraPro\tests\data_processing\20240925\tree'
    for key in f.keys():
        if key != 'nplab_log':
            parent_path = f'/{key}'
            save_name = fr'{save_fullpath}\{key}.txt'
            with open(save_name, 'w') as f:
                # 重定向标准输出
                sys.stdout = f
                find_and_print_tree(tree_data, parent_path)

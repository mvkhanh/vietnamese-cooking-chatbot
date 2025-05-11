from typing import Literal
import json

class Loader:
    key_maps = {'name': 'Tên món', 'description': 'Mô tả món ăn', 'cook_time': 'Thời gian nấu', 'instructions': 'Hướng dẫn nấu', 'categories': 'Danh mục món ăn', 'ingredients': 'Nguyên liệu', 'level': 'Mức độ', 'servings': 'Khẩu phần'}
    
    def __init__(self, file_type: str = Literal['json']):
        assert file_type in ['json'], 'file_type must be json'
    
    def load(self, recipes_file):
        with open(recipes_file, 'r', encoding='utf-8') as file:
            # Load the JSON data from the file
            data = json.load(file)
            
        # remove 'Món Ngon Mỗi Ngày' and convert to string
        texts = []
        for recipe in data:
            if 'món ngon mỗi ngày' in recipe['description'].lower():
                recipe['description'] = '\n'.join([s for s in recipe['description'].split('\n') if 'món ngon mỗi ngày' not in s.lower()])
            txt = ''
            for k, v in Loader.key_maps.items():
                value = recipe[k]
                if value == '' or value == 0 or value == []:
                    continue
                txt += f'{v}: '
                if k == 'categories':
                    txt += ', '.join([c['detail_category'] for c in value]) + '.'
                elif k == 'ingredients':
                    txt += '\n'
                    for i in value:
                        txt += f"- {i['name']}"
                        if i['quantity'] != '':
                            txt += f": {i['quantity']}"
                        txt += '.\n'
                elif k == 'instructions':
                    txt += '\n'
                    txt += '\n'.join([f'- {s}' for s in value.split('\n')])
                elif k == 'cook_time':
                    txt += f'{value} phút.'
                elif k == 'servings':
                    txt += f'{value} người.'
                else:
                    txt += f'{value}.'
                txt += '\n'
            texts.append(txt)
        return texts
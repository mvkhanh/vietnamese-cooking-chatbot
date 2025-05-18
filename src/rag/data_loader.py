from typing import Literal
import json

class Loader:
    
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
                
            instructions = ingredients = categories = f'{recipe["name"]}\n'
            
            if recipe['cook_time'] != 0:
                instructions += f'Thời gian nấu: {recipe["cook_time"]} phút.\n'
            if recipe['instructions'] != "":
                instructions += 'Hướng dẫn nấu:\n'
                instructions += '\n'.join([f'- {s}' for s in recipe['instructions'].split('\n')])
            
            if recipe['servings'] != 0:
                ingredients += f'Khẩu phần: {recipe["servings"]}\n'
            if recipe['ingredients'] != []:
                ingredients += 'Nguyên liệu:\n'
                for i in recipe['ingredients']:
                    ingredients += f"- {i['name']}"
                    if i['quantity'] != '':
                        ingredients += f": {i['quantity']}"
                    ingredients += '.\n'
                    
            if categories != []:
                categories += 'Danh mục món ăn: '
                categories += ', '.join([c['detail_category'] for c in recipe['categories']]) + '.'
            
            if instructions != f'{recipe["name"]}\n':
                texts.append(instructions)
            if ingredients != f'{recipe["name"]}\n':
                texts.append(ingredients)
            if categories != f'{recipe["name"]}\n':
                texts.append(categories)
        return texts
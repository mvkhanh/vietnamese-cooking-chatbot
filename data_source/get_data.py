# Run in webdjango: python manage.py shell

from recipes.models import Recipe, RecipeIngredient
import json

# Lấy toàn bộ recipe, kèm category và nguyên liệu
recipes = Recipe.objects.prefetch_related(
    'category__category',           # category là DetailCategory, lấy thêm Category
    'ingredients',                  # ingredients từ M2M
    'recipeingredient_set__ingredient'  # quantity từ through model
)

data = []
for recipe in recipes:
    data.append({
        'name': recipe.name,
        'description': recipe.description,
        'cook_time': recipe.cook_time,
        'instructions': recipe.instructions,
        'level': recipe.level,
        'servings': recipe.servings,
        'categories': [
            {
                'detail_category': dc.name,
                'category': dc.category.name
            }
            for dc in recipe.category.all()
        ],
        'ingredients': [
            {
                'name': ri.ingredient.name,
                'quantity': ri.quantity
            }
            for ri in recipe.recipeingredient_set.all()
        ]
    })

# Xuất JSON
with open('recipes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
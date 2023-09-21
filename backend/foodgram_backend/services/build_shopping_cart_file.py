class BuildShoppingCartFileService:

    def __init__(self, ingredients):
        self.ingredients = ingredients
        self.final_list = self._build()

    def _build(self):
        final_list = 'Ваш список покупок:\n'

        for item in self.ingredients:
            ingredient_name = item['ingredient__name']
            measurement_unit = item['ingredient__measurement_unit']
            amount = item['amount']
            final_list += f'{ingredient_name} ({measurement_unit}) {amount}\n'
        
        return final_list[:-1]

    @property
    def filename(self):
        return 'shopping-list.txt'

import graphene
from graphene_django import DjangoObjectType

from ingredients.models import Category, Ingredient


"""
NOTE You can think of this as being something like your top-level `urls.py` file.
"""


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    """
    query implementation using class

    expect below query:
    ```graphql
    query {
        allIngredients {
            ingredients: [Ingredient!]!
        }
    }
    ```
    but can not find no explicit query definition (like above) inside of method.
    """

    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        """
        resolver get all ingredients

        NOTE We can easily optimize query count in the resolve method
        """
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist as err:
            print(err)
            return None


cookbook_schema = graphene.Schema(query=Query)

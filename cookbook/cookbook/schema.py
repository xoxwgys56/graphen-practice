from nis import cat
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


class CategoryInput(graphene.InputObjectType):
    name = graphene.String()


class IngredientInput(graphene.InputObjectType):
    name = graphene.String()
    notes = graphene.String()
    category = CategoryInput()


class CreateIngredient(graphene.Mutation):
    class Arguments:
        ingredient = IngredientInput(required=True)

    ok = graphene.Boolean()
    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(root, info, ingredient):
        # NOTE do not check category is defined or not.
        try:
            category = Category.objects.get(name=ingredient.category.name)
        except Exception as err:
            category = Category(name=ingredient.category.name)
            category.save()
        new_ingredient = Ingredient(
            name=ingredient.name, notes=ingredient.notes, category=category
        )
        ok = True
        new_ingredient.save()

        return CreateIngredient(ingredient=new_ingredient, ok=ok)


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


class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()


cookbook_schema = graphene.Schema(query=Query, mutation=Mutation)

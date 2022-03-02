# graphene-django practice

follow [quickstart](https://docs.graphene-python.org/en/latest/quickstart/)

## usage

```shell
# use pipenv
pipenv shell
pipenv install && pipenv install --dev

# use python venv
#
# skip generate venv and activate
pip3 install -r ./requirements.txt

# after initialize
cd ./cookbook
python3 manage.py migrate && python3 manage.py loaddata ingredients
python3 manage.py runserver
```

### superuser

- id : admin
- pw : 1234

## Issues

```shell
ImportError: cannot import name 'force_text' from 'django.utils.encoding'
```

can resolve using below [answer](https://stackoverflow.com/questions/70382084/import-error-force-text-from-django-utils-encoding)

```python
# <your-venv>/lib/python3.9/site-packages/django/utils/encoding.py
from django.utils.encoding import force_text
# to
from django.utils.encoding import force_str
```

see related [issue](https://github.com/graphql-python/graphene-django/issues/1284)

## NOTE

### auto camelCase field

copied from [#testing-our-graphql-schema](https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/#testing-our-graphql-schema)

> Graphene [automatically camelcases](https://docs.graphene-python.org/en/latest/types/schema/#auto-camelcase-field-names) all field names for better compatibility with JavaScript clients.

for example, if you named method which `resolve_all_ingredients`. graphene-django parsing it as `allIngredients`

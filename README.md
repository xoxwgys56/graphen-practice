# graphene-django practice

follow [quickstart](https://docs.graphene-python.org/en/latest/quickstart/)

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

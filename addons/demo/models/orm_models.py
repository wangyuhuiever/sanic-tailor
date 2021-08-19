from tortoise.models import Model
from tortoise import fields


class DemoORMModel(Model):

    id = fields.IntField(pk=True)
    col1 = fields.IntField(description='Col 1')
    col2 = fields.TextField(description='Col 2')
    # col3 = fields.CharField(max_length=128, description='Col 3')

    class Meta:
        table = 'test_table'


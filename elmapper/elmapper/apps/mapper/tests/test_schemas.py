from django.test import TestCase


class SchemaTestCase(TestCase):

    def test_serialize_fields(self):
        from elmapper.apps.mapper.schemas import Fields
        schema = Fields()
        data = [{
            'external_name': 'test',
            'model_name': 'test',
            'foreign_key_mapping': [{
                'internal_value': 1,
                'external_fk': 1
            }]
        }]
        expected = [{
            'external_name': 'test',
            'model_name': 'test',
            'foreign_key_mapping': [{
                'internal_value': u'1',
                'external_fk': u'1',
                'pattern': 'pk',
            }]
        }]

        result = schema.deserialize(schema.serialize(data))

        assert result == expected

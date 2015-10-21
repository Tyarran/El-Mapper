import json
import os

from django.test import TestCase


HERE = os.path.abspath(os.path.basename(__file__))
PROJECT_DIR = os.path.join(HERE, '..')
CSV_PATH = os.path.join(PROJECT_DIR, 'products.csv')


class MapperTestCase(TestCase):

    def setUp(self):
        from elmapper.apps.mapper.models import (
            Brand,
            Category,
            Color,
            ImportedProductCSV,
            MappingConfig,
        )
        mapping_config = MappingConfig()
        mapping_config.title = 'test config'
        mapping_config.description = 'test config'
        mapping_config.json = json.dumps([{
            'external_name': 'name',
            'model_name': 'name',
            'foreign_key_mapping': [],
        }])
        self.imported_csv = ImportedProductCSV(csv_file=CSV_PATH)
        self.color = Color.objects.create(name='red')
        self.brand = Brand.objects.create(name='RCommande Corp', description="my fictive company")
        self.category = Category.objects.create(label='test', description="a test category")

    def test_get_value_no_fk(self):
        from elmapper.apps.mapper.views import Mapper
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = '{}'
        mapper = Mapper(self.imported_csv, mapping_config)
        config = {
            'external_name': 'name',
            'model_name': 'name',
            'foreign_key_mapping': [],
        }

        result = mapper.get_value('name', 'a name', config)

        self.assertEqual(result, 'a name')

    def test_get_value_with_fk_with_pattern(self):
        from elmapper.apps.mapper.views import Mapper
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': 3,
                'internal_value': 1,
                'pattern': 'pk'
            }],
        }])

        mapper = Mapper(self.imported_csv, mapping_config)
        config = {
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': 3,
                'internal_value': 1,
                'pattern': 'pk'
            }],
        }

        result = mapper.get_value('category', '3', config)

        self.assertEqual(result, self.category.pk)

    def test_get_value_with_fk_with_attribute_pattern(self):
        from elmapper.apps.mapper.views import Mapper
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'label',
            }],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)
        config = {
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'label',
            }],
        }

        result = mapper.get_value('category', 'value', config)

        self.assertEqual(result, self.category.pk)

    def test_get_mapping_config_by_external_name(self):
        from elmapper.apps.mapper.views import Mapper
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'label',
            }],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)

        result = mapper.get_mapping_config_by_external_name('category')

        self.assertEqual(result, mapper.mapping_config[0])

    def test_get_mapping_config_by_external_name_with_multiple_field_mapping(self):
        from elmapper.apps.mapper.views import Mapper
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'label',
            }],
        }, {
            'external_name': 'brand',
            'model_name': 'brand',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)

        result = mapper.get_mapping_config_by_external_name('brand')

        self.assertEqual(result, mapper.mapping_config[1])

    def test__call__(self):
        from elmapper.apps.mapper.views import Mapper, Product
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': '3',
                'internal_value': '1',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'brand',
            'model_name': 'brand',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'price',
            'model_name': 'price',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'description',
            'model_name': 'description',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'color',
            'model_name': 'color',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'name',
            'model_name': 'name',
            'foreign_key_mapping': [],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)

        result = mapper()

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['imported'], 1)

    def test__call__with_missing_column_mapping(self):
        from elmapper.apps.mapper.views import Mapper, Product
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'brand',
            'model_name': 'brand',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'price',
            'model_name': 'price',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'description',
            'model_name': 'description',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'color',
            'model_name': 'color',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'name',
            'model_name': 'name',
            'foreign_key_mapping': [],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)

        result = mapper()

        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['imported'], 0)

    def test__call__with_unknown_category_mapping(self):
        from elmapper.apps.mapper.views import Mapper, Product
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'brand',
            'model_name': 'brand',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'price',
            'model_name': 'price',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'description',
            'model_name': 'description',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'color',
            'model_name': 'color',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'name',
            'model_name': 'name',
            'foreign_key_mapping': [],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)

        result = mapper()

        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['imported'], 0)

    def test__call__with_unknow_reference(self):
        from elmapper.apps.mapper.views import Mapper, Product
        from elmapper.apps.mapper.models import MappingConfig
        mapping_config = MappingConfig()
        mapping_config.json = json.dumps([{
            'external_name': 'category',
            'model_name': 'category',
            'foreign_key_mapping': [{
                'external_fk': '3',
                'internal_value': '2',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'brand',
            'model_name': 'brand',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'price',
            'model_name': 'price',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'description',
            'model_name': 'description',
            'foreign_key_mapping': [],
        }, {
            'external_name': 'color',
            'model_name': 'color',
            'foreign_key_mapping': [{
                'external_fk': 'value',
                'internal_value': 'test',
                'pattern': 'pk',
            }],
        }, {
            'external_name': 'name',
            'model_name': 'name',
            'foreign_key_mapping': [],
        }])
        mapper = Mapper(self.imported_csv, mapping_config)

        result = mapper()

        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(result['errors'][0][1], ['Category matching query does not exist.'])
        self.assertEqual(len(result['errors']), 1)
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['imported'], 0)

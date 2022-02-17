# -*- coding: utf-8 -*-

from odoo.tests.common import SavepointCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import Form

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        property_type = cls.env['estate.property.type'].create({'name': 'Tipo1'})
        cls.properties = cls.env['estate.property'].create([{
            'name': 'Big Villa (3)', 
            'state': 'new', 
            'description': 'A nice big villa', 
            'postcode': 12345,
            'date_availability': '2020-02-02',
            'expected_price': 1600000,
            'bedrooms': 6,
            'living_area': 100,
            'facades': 4,
            'garage': False,
            'garden': False,
            'property_type_id': property_type.id,
        }])
        cls.env['estate.property.offer'].create({'price': 1600000, 'validity': 14, 'property_id' : cls.properties[0].id, 'partner_id': cls.env.ref('base.res_partner_12').id})
        cls.properties[0].state = 'sold'

    def test_offer(self):
        self.assertEqual(len(self.properties.offer_ids), 1)        
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({'price': 1600001, 'validity': 14, 'property_id' : self.properties[0].id, 'partner_id': self.env.ref('base.res_partner_12').id})

    def test_garden(self):
        f = Form(self.env['estate.property'])
        f.garden = True
        self.assertEqual(f.garden_area, 10)
        self.assertEqual(f.garden_orientation, 'north')
        f.garden = False
        self.assertEqual(f.garden_area, 0)
        self.assertEqual(f.garden_orientation, False)

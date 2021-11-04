# -*- coding: utf-8 -*-

from odoo import models, fields

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'

    name = fields.Char(required=True)

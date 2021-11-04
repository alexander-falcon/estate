# -*- coding: utf-8 -*-

from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'

    name = fields.Char(required=True)
    
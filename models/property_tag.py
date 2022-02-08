# -*- coding: utf-8 -*-

from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)', 'Tag name must be unique.')
    ]
    
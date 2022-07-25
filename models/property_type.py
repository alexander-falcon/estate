# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_number_offers")

    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)', 'Type name must be unique.')
    ]

    @api.depends("offer_ids")
    def _compute_number_offers(self):
        for record in self:
            if record.offer_ids is not None:
                record.offer_count = len(record.offer_ids)
            
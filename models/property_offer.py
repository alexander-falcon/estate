# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", readonly=False, store=True)
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one ('res.partner', required=True)
    property_id = fields.Many2one ('estate.property', required=True)
    create_date = fields.Date(default=lambda self: fields.Date.today())
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not (record.create_date and record.validity):
                record.date_deadline = record.create_date
                continue
            duration = timedelta(days=record.validity, seconds=-1)
            record.date_deadline = record.create_date + duration

    def _inverse_date_deadline(self):
        for record in self:
            if not (record.create_date and record.date_deadline):
                continue
            record.validity = (record.date_deadline - record.create_date).days + 1

    def action_accept(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("Refused offer cannot be accepted.")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("Accepted offer cannot be refused.")
            record.status = "refused"
        return True


# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = "price desc"

    price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", readonly=False, store=True)
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one ('res.partner', required=True)
    property_id = fields.Many2one ('estate.property', required=True)
    create_date = fields.Date(default=lambda self: fields.Date.today())
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Price must be positive.')
    ]
    
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
        # deberia iterar y poner en refused el resto
        #for record in self:
        record = self
        if record.status == 'refused':
            raise UserError("Refused offer cannot be accepted.")
        if self.property_id.offer_ids and (len(self.property_id.offer_ids) > 0):
            self.property_id.offer_ids.status = "refused"
        record.status = "accepted"
        record.property_id.buyer_id = record.partner_id
        record.property_id.selling_price = record.price
        record.property_id.state = 'accepted'
        return True

    def action_refuse(self):
        record = self
        #for record in self:
        if record.status == 'accepted':
            raise UserError("Accepted offer cannot be refused.")
        record.status = "refused"
        return True

    @api.model
    def create(self, vals_list):
        prop = self.env['estate.property'].browse(vals_list['property_id'])
        if prop.offer_ids and len(prop.offer_ids) > 0:
            min_offer =  min(prop.offer_ids.mapped('price'))
            if vals_list['price'] < min_offer:
                raise UserError(f"The offer must be higher than {min_offer}") 
        if prop.state == 'new':
            prop.state = 'received'        
        return super().create(vals_list)



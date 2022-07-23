# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    state = fields.Selection(default='new', required=True, copy=False, selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')])
    postcode = fields.Char()
    #date_availability = fields.Date(string='Available From', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    date_availability = fields.Date(string='Available From', copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)) 
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean(help='Si tiene garage')
    garden = fields.Boolean(help='Si tiene jardin')
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user) # _id
    tag_ids = fields.Many2many("estate.property.tag") # _ids
    offer_ids = fields.One2many("estate.property.offer", "property_id") # _ids
    total_area = fields.Integer(compute="_compute_total_area", string='Total Area (sqm)') # _ el metodo es privado
    best_price = fields.Float(compute="_compute_best_price", string='Best Offer')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'Selling price must be positive.')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_percent(self):
        for record in self: # siempre usar float_is_zero y float_compare para floats
            if not float_is_zero(record.selling_price, 2) and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError(_('Selling price cannot be less than 90 percent of expected price.'))
                
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            # best_price = None
            # for offer in record.offer_ids:
            #     if not best_price or offer.price > best_price:
            #         best_price = offer.price
            # record.best_price = best_price
            if record.offer_ids and len(record.offer_ids) > 0:
              record.best_price = max(record.offer_ids.mapped('price'))  
            else:
              record.best_price = None

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # @api.onchange("offer_ids")
    # def _onchange_offers_ids(self):
    #     if self.state == 'received' and not self.offer_ids:
    #         self.state = 'new'
    #     elif self.state == 'new' and self.offer_ids and len(self.offer_ids) > 0:
    #         for offer in self.offer_ids:
    #             if offer.status == 'accepted':
    #                 return
    #         self.state = 'received'

    def sold_property(self):
        for record in self: # todo revisar las ofertas
            if record.state == 'canceled':
                raise UserError(_("Canceled properties cannot be sold."))
            record.state = "sold"
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be canceled."))
            record.state = "canceled"
        return True

    def unlink(self):
        for record in self:
            if record.state != 'new' and record.state != 'canceled':
                raise UserError(_('No se puede eliminar una propiedad que no sea nueva o cancelada.'))
        return super().unlink()
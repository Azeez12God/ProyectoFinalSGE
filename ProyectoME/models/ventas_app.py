from odoo import models, fields


class VentasModel(models.Model):
	_name = 'ventas.model'

	name = fields.Char(string='Nombre', required=True)
	date = fields.Date(string='Fecha de venta', default=fields.Date.today)
	client = fields.Many2one('res.users', string='Cliente', required=True)
	product_id = fields.Many2one('producto.model', string='Producto vendido', required=True)
	total = fields.Float(string='Total de la venta', required=True)

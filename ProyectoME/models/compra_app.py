from odoo import models, fields, api
from odoo.exceptions import UserError


class CompraModel(models.Model):
	_name = 'compra.model'

	name = fields.Char(string='Nombre', required=True)
	date = fields.Date(string='Fecha de venta', default=fields.Date.today)
	client = fields.Many2one('res.users', string='Cliente', required=True)
	total = fields.Float(string='Total de la venta', store=True, compute='_precio_total')
	producto = fields.Many2one('producto.model', string='Producto', required=True)
	cantidad = fields.Integer(string='Cantidad productos', required=True)

	@api.constrains('cantidad')
	def _check_cantidad(self):
		for linea in self:
			if linea.cantidad < 1:
				raise UserError("La cantidad debe ser mayor que cero.")
			if linea.cantidad > linea.producto.stock:
				raise UserError("La cantidad no puede ser mayor que el stock disponible.")

	@api.depends('producto', 'cantidad')
	def _precio_total(self):
		for compra in self:
			total = 0
			for producto in compra.producto:
				total += producto.sale_price * compra.cantidad
			compra.total = total

	@api.model
	def create(self, vals):
		record = super(CompraModel, self).create(vals)
		producto = self.env['producto.model'].browse(vals['producto'])
		producto.stock -= vals['cantidad']
		return record
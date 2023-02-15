from odoo import models, fields, api
from odoo.exceptions import UserError


class CompraModel(models.Model):
	_name = 'compra.model'

	name = fields.Char(string='Nombre', required=True)
	date = fields.Date(string='Fecha de compra', default=fields.Date.today)
	client = fields.Many2one('res.users', string='Cliente', required=True)
	total = fields.Float(string='Total de la compra', store=True, compute='_precio_total')
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
		if producto.stock < 10:
			producto.state = 'running_out'
		if producto.stock == 0:
			producto.state = 'sold_out'
		return record

	@api.constrains('date')
	def _check_date(self):
		for record in self:
			if record.date < fields.Date.today():
				raise UserError("La fecha de compra no puede ser menor a la fecha actual.")

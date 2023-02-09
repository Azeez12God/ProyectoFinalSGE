from odoo import models, fields, api
from odoo.exceptions import UserError


class CompraModel(models.Model):
	_name = 'compra.model'

	name = fields.Char(string='Nombre', required=True)
	date = fields.Date(string='Fecha de venta', default=fields.Date.today)
	client = fields.Many2one('res.users', string='Cliente', required=True)
	total = fields.Float(string='Total de la venta', required=True)
	productos = fields.Many2many('producto.model', string='Productos comprados')
	cantidad = fields.Float(string='Cantidad productos', required=True)

	@api.constrains('cantidad')
	def _check_cantidad(self):
		for linea in self:
			if linea.cantidad < 1:
				raise UserError("La cantidad debe ser mayor que cero.")
			if linea.cantidad > linea.productos.stock:
				raise UserError("La cantidad no puede ser mayor que el stock disponible.")

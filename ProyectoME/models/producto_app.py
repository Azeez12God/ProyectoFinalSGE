from odoo import fields, models, api
from odoo.exceptions import UserError


class ProductoModel(models.Model):
	_name = "producto.model"
	_description = "La descripción del módulo"

	# Campos básicos
	name = fields.Char('Nombre', required=True)
	code = fields.Integer('Código', default=lambda self: self._generate_code())
	description = fields.Text('Descripción', help='Introduce una descripción de la propiedad')
	category = fields.Selection([('salado', 'Salado'), ('dulce', 'Dulce'), ('bebida', 'Bebida'), ('varios', 'Varios')], string='Categoría')
	sale_price = fields.Float(string='Precio de venta', required=True)
	image = fields.Binary(string='Imagen')
	stock = fields.Integer(string='Stock', required=True)
	# supplier = fields.Many2One('res.partner', string='Proveedor')
	state = fields.Selection([('available', 'Disponible'), ('sold_out', 'Agotado'), ('running_out', 'Escaso')], string='Estado', required=True, default='available')
	compras = fields.Many2many('compra.model', string='Compras', through='compra.producto.model')
	inventory_percentage = fields.Float(string='Porcentaje de inventario restante', compute='_compute_inventory_percentage')

	@api.depends('stock')
	def _compute_inventory_percentage(self):
		for record in self:
			if record.stock <= 0:
				record.inventory_percentage = 0.0
			else:
				record.inventory_percentage = (record.stock / 30) * 100

	def _generate_code(self):
		return self.env['ir.sequence'].next_by_code('producto.model.sequence')

	@api.constrains('stock')
	def _check_stock(self):
		for record in self:
			if record.stock < 0:
				raise UserError("El stock no puede ser negativo.")
			if record.stock > 30:
				raise UserError("El stock no puede ser mayor que 30.")

	@api.model
	def create(self, values):
		last_code = self.search([], order='code desc', limit=1).code
		values['code'] = last_code + 1
		record = super(ProductoModel, self).create(values)
		return record

	@api.onchange('stock')
	def _onchange_stock(self):
		for record in self:
			if record.stock == 0:
				record.state = 'sold_out'
			elif record.stock < 5:
				record.state = 'running_out'
			else:
				record.state = 'available'

	def restock(self):
		for producto in self:
			producto.stock += (30 - producto.stock)

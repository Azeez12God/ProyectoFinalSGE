from odoo import fields, models


class ProductoModel(models.Model):
	_name = "producto.model"
	_description = "La descripción del módulo"

	# Campos básicos
	name = fields.Char('Nombre', required=True)
	code = fields.Char('Código', required=True)
	description = fields.Text('Descripción', help='Introduce una descripción de la propiedad')
	category = fields.Selection([('salado', 'Salado'), ('dulce', 'Dulce'), ('bebida', 'Bebida'), ('varios', 'Varios')],
								string='Categoría')  # TODO posible eliminación
	sale_price = fields.Float(string='Precio de venta', required=True)
	image = fields.Binary(string='Imagen')
	stock = fields.Float(string='Stock', required=True)
	# supplier = fields.Many2One('res.partner', string='Proveedor')
	state = fields.Selection([('available', 'Disponible'), ('sold_out', 'Agotado'), ('on_the_way', 'En camino')],
							string='Estado', required=True, default='available')

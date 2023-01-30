from odoo import fields, models

class Producto_Model(models.Model):
    _name = "producto.model"
    _description = "La descripción del módulo"

    # Campos básicos
    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código', required=True)
    description = fields.Text('Descripción', help='Introduce una descripción de la propiedad')

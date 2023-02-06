{
	'name': "máquinas_expendedoras",
	'author': "Alberto López Gil y Javier Escolástico Egido Luz",
	'version': '1.0',
	'summary': 'Gestión de máquinas expendedoras.',
	'Description': 'Gestión de máquinas expendedoras.',

	'category': 'Generic Modules/Others',
	'website': 'http://www.modules/Others',
	'depends': ['base'],
	'application': True,
	'installable': True,

	# data files always loaded at installation
	'data': [
		'security/ir.model.access.csv',
		'views/producto_view.xml',
		'views/ventas_view.xml'
	],
	# data files containing optionally loaded demonstration data

}

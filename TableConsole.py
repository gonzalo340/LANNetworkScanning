"""
	Clase en Python para mostrar datos en una tabla en la terminal.
"""
class Table:
	margin_left = 1
	margin_right = 1
	
	columns_str = '|'
	rows_str = ''
	columns_size = []
	
	def __init__(self):
		pass
		
	def formatText(self, text, width):
		content = text
		
		for i in range(0,width-len(content)):
			content += " "
		return content
		
	def addColumn(self, title, width):
		self.columns_str += self.formatText("", self.margin_left) + self.formatText(title, width) + self.formatText("", self.margin_right) + "|"
		self.columns_size.append(width)

	def addRow(self, data):
		col = 0
		row = '|'
		for d in data:
			row += self.formatText("", self.margin_left) + self.formatText(d, self.columns_size[col]) + self.formatText("", self.margin_right) + "|"
			col= col+1
		self.rows_str += row + "\r\n"
		
	def make(self):
		# Sumo los caracteres de todas las columnas
		max_chars = 0
		for i in list(self.columns_size):
			max_chars += i
			
		# Sumo los margenes left y right de todas las columnas
		max_chars += (self.margin_left*len(self.columns_size)) + (self.margin_right*len(self.columns_size))
		
		max_chars += len(self.columns_size)+1
		separator_str = ''
		for i in range(max_chars):
			separator_str += "-"

		print separator_str
		print self.columns_str
		print separator_str
		print self.rows_str.strip()
		print separator_str

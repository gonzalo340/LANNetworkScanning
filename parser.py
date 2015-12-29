#!/usr/bin/python
from xml.dom import minidom
from urllib import urlencode
from TableConsole import Table
import os
import sys
import httplib2
import json

# Url Admin: https://apirest-gfpsoft.rhcloud.com/admin/
# User: gonzalo
# Pass: Gonzalo340Admin

# Token para poder hacer POST al servidor
try:
	from config import Config
except:
	print "ERROR:"
	print "Renombrar el archivo 'config.py.default' por 'config.py', y configurar la variable 'token'."
	sys.exit(1)
	
__TOKEN__ = Config().getToken()

# Esta funcion retorna la descripcion de una determinada MAC
def getMacDescription(mac, data):
	content = "Desconocido"
	for d in data['macs']:
		if str(d['address']).upper() == mac.upper():
			content = str(d['description'])
	return content
	
def getMacIP(mac, data):
	content = ""
	for d in data['macs']:
		if str(d['address']).upper() == mac.upper():
			content = str(d['ip'])
	return content
	
# Si el usuario NO es root, detengo la ejecucion del script.
if os.geteuid() != 0:
	print "Debes tener privilegios root para este script."
	sys.exit(1)

# Obtengo el listado de MACS desde el servidor, enviando una peticion POST con el token
headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
resp, content = httplib2.Http().request("https://apirest-gfpsoft.rhcloud.com/macs/", "POST", urlencode({'token':__TOKEN__}), headers)

# Si el servidor responde con una respuesta incorrecta, detengo el script
if resp.status != 200:
	print "Error al obtener datos del servidor."
	sys.exit(1)

# Convierto el Json en objeto de datos
try:
	data = json.loads(content)
except ValueError:
	print "Error al obtener los datos del servidor."
	sys.exit(1)

"""
	Obtengo el XML con las direcciones ip y mac del escaneo de hosts.
	Este fichero se genera en el bash script scanner mediante el comando nmap.
"""
xmldoc = minidom.parse('tmp/out.xml')

# Obtengo el tag host del XML
items = xmldoc.getElementsByTagName('host')

# Defino un objeto de tipo tabla para mostrar los datos en distintas columnas
t = Table()

# Agrego las columnas con el titulo y el largo
t.addColumn("MAC", 20)
t.addColumn("IP", 38)
t.addColumn("Descripcion de la MAC.", 50)

# Recorro los items del tag host
for item in items:
	ipConn = "" # Texto para saber si la conexion esta con una IP permitida
	
	# Si el item host trae una sola address, es porque NO trae la MAC, esto significa que es la ip de mi pc.
	if len(item.getElementsByTagName('address')) == 1:
		ip  = str(item.getElementsByTagName('address')[0].getAttribute('addr'))
		mac = "--- MI EQUIPO ---"
		desc = "Tu"
	elif len(item.getElementsByTagName('address')) == 2:
		ip  = str(item.getElementsByTagName('address')[0].getAttribute('addr'))
		mac = str(item.getElementsByTagName('address')[1].getAttribute('addr'))
		desc = getMacDescription(mac, data)
		
		# Chequeo si la conexion tiene una IP valida para la mac.
		if ip != getMacIP(mac, data):
			#ipConn = " CONECTADO CON IP NO PERMITIDA."
			ipConn = " IP NO PERMITIDA"
		
	# Imprimo los datos escaneados en una fila nueva
	t.addRow([str(mac), str(ip)+str(ipConn), desc])

# Muestro la tabla en la terminal
t.make()

import csv
import sys

turnos = {'DISCONTINU':'400','MATUTINO':'100','NOCTURNO':'300','VESPERTINO':'200'}

with open(sys.argv[1], 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
	for row in spamreader:
		row[1] = turnos[row[1]]
		if len(row[2])>0:
			if row[2][:row[2].find(' ')]=="EXTENSION":
				try:
					int(row[2][row[2].find(' ')+1:])
					row[0] = row[0]+row[2][row[2].find(' ')+1:]
				except ValueError:
					#solucion para limpiar registros que existen en ENLACE 2013 pero que en 2014 tienen una letra al final del registro.
					#requerimos esto para empatar los registros historicos y no insertar nuevos valores en escuelas.
					row[0] = row[0]+row[2][row[2].find(' ')+1:-1]
			else:
				#son registros que no tienen extension sino nombres de lugares. creamos una clave para homologarlos de la siguiente manera:
				#cct + primer caracter de la clave de turno + ultimas dos letras de la extension (sin espacios)
				row[0] = row[0]+row[1][0:1]+row[2][-2:].strip()
		row = row[:2] + row[3:]
		print row
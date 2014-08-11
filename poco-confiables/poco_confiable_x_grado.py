#python poco_confiable_x_grado.py primaria_poco_confiable.psv 4 primaria
import MySQLdb
import gc
import csv
import sys

turnos = {'DISCONTINU':'400','MATUTINO':'100','NOCTURNO':'300','VESPERTINO':'200'}

def buscaRegistroEnlace(archivo, grados, nivel, inicio_grados):
	global turnos
	
	with open(archivo, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter='|', quotechar='"')
		db=MySQLdb.connect("localhost","root","Imco12345","imco_cte_optimizada")
		cursor = db.cursor()
		registros = 0
		for row in spamreader:
			i=3
			j=0
			n = i+grados
			while i < n:
				sql = 'update enlaces_v2 set poco_confiables='+row[2+j]+' where anio=2013 and nivel="'+nivel+'" and cct="'+row[0]+'" and turnos='+turnos[row[1]]+' and grado='+str(j+inicio_grados)+';'
				try:
					cursor.execute(sql)
				except MySQLdb.Warning, e:
					print sql
				i+=1
				j+=1
				registros+=1
		db.commit()
		print registros
	pass


if len(sys.argv)==5:
	buscaRegistroEnlace(sys.argv[1],int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
else:
	print "Faltan parametros"

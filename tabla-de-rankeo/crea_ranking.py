#python crea_ranking.py bachillerato | sed -r "s/(\[|'|\]| )//g" > ranking_bachillerato_v1.csv
import MySQLdb
import gc
import csv
import sys

def revisaGrado(calificaciones,iterador,grados):
	i=iterador
	n=iterador+grados
	temp_esp=[]
	temp_mat=[]
	temp_alumnos=[]
	turno = calificaciones[i][1] 
	pct_mat = []
	pct_esp = []
	mat_x=[[],[],[]]
	esp_x=[[],[],[]]
	poco_confiables = []
	while i<n:
		if calificaciones[i][2]>0 and calificaciones[i][3]>0:
			temp_esp.append(calificaciones[i][2])
			temp_mat.append(calificaciones[i][3])
			temp_alumnos.append(calificaciones[i][4])
			pct_mat.append(calificaciones[i][5])
			pct_esp.append(calificaciones[i][6])

			mat_x[0].append(calificaciones[i][7])
			mat_x[1].append(calificaciones[i][8])
			mat_x[2].append(calificaciones[i][9])

			esp_x[0].append(calificaciones[i][10])
			esp_x[1].append(calificaciones[i][11])
			esp_x[2].append(calificaciones[i][12])

			poco_confiables.append(calificaciones[i][13])
			#turnos_usados.append(puntaje[1])
		else:
			temp_esp=[]
			temp_mat=[]
			temp_alumnos=[]
			pct_mat = []
			pct_esp = []
			mat_x=[[],[],[]]
			esp_x=[[],[],[]]
			poco_confiables = []
			i+=n
		i+=1
	return temp_mat,temp_esp,temp_alumnos,turno, pct_mat,pct_esp, mat_x,esp_x, poco_confiables

def actualizaRanking(grados,sql1,sql2):
	db=MySQLdb.connect("localhost","root","Imco12345","imco_cte_optimizada")
	cursor = db.cursor()
	cursor.execute(sql1)
	data = cursor.fetchall()
	for db_row in data:
		cursor.execute(sql2.replace("*",str(db_row[0])))
		data_por_cct = cursor.fetchall()
		n = len(data_por_cct)
		valores=[]
		turnos=[]
		mat=[]
		esp=[]
		pct_rep = 0
		x = []
		alumnos=0
		poco_confiables = 0
		i=0
		while i< n/grados:
			temp = revisaGrado(data_por_cct,i*grados,grados)
			
			if len(temp[0])==grados:
				mat.append(sum(temp[0])/float(grados))
				esp.append(sum(temp[1])/float(grados))
				alumnos+=sum(temp[2])
				turnos.append(str(temp[3]))
				pct_rep =round( (sum(temp[4])+sum(temp[5]))/(float(2*alumnos)),6)
				x.append(round( (sum(temp[6][0])+sum(temp[7][0]))/(float(2*alumnos)) ,6))
				x.append(round( (sum(temp[6][1])+sum(temp[7][1]))/(float(2*alumnos)) ,6))
				x.append(round( (sum(temp[6][2])+sum(temp[7][2]))/(float(2*alumnos)) ,6))
				poco_confiables = int(sum(temp[8]))
				
				print [int(db_row[0]), mat[0],esp[0],mat[0]*.8 + esp[0]*.2, int(alumnos), int(turnos[0]), pct_rep ,x[0],x[1],x[2],poco_confiables]
			else:
				print [int(db_row[0]),0,0, 0, 0, 'NULL',0,0,0,0,0]
			i+=1
	gc.collect()
	db.close()

def verificaPromGral(sql):
	db=MySQLdb.connect("localhost","root","Imco12345","imco_cte_optimizada")
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()
	print len(data)
	for db_row in data:
		if float(db_row[2])!=float(db_row[3]):
			print db_row
	gc.collect()
	db.close()

if sys.argv[1]=='primaria':
	#Primaria
	sql1 ='select e.id,e.cct,count(*) from escuelas e, enlaces_v2 en where e.id>0 and e.nivel=12 and e.cct=en.cct and en.anio=2013 group by cct;'
	sql2 = 'select id_cct,turnos,puntaje_espaniol,puntaje_matematicas, alumnos_que_contestaron_total, alumnos_en_nivel0_espaniol,alumnos_en_nivel0_matematicas,alumnos_en_nivel1_matematicas,alumnos_en_nivel2_matematicas,alumnos_en_nivel3_matematicas,alumnos_en_nivel1_espaniol,alumnos_en_nivel2_espaniol,alumnos_en_nivel3_espaniol, poco_confiables from enlaces_v2 where anio=2013 and id_cct=* order by turnos;';
	actualizaRanking(4,sql1,sql2)
else:
	if sys.argv[1]=='secundaria':
		#Secundaria
		sql1 ='select e.id,e.cct,count(*) from escuelas e, enlaces_v2 en where e.id>0 and e.nivel=13 and e.cct=en.cct and en.anio=2013 group by cct;'
		sql2 = 'select id_cct,turnos,puntaje_espaniol,puntaje_matematicas, alumnos_que_contestaron_total, alumnos_en_nivel0_espaniol,alumnos_en_nivel0_matematicas,alumnos_en_nivel1_matematicas,alumnos_en_nivel2_matematicas,alumnos_en_nivel3_matematicas,alumnos_en_nivel1_espaniol,alumnos_en_nivel2_espaniol,alumnos_en_nivel3_espaniol, poco_confiables from enlaces_v2 where anio=2013 and id_cct=* order by turnos;';
		actualizaRanking(3,sql1,sql2)
	else:
		if sys.argv[1]=='bachillerato':
			#Prepa
			sql1 ='select e.id,e.cct,count(*) from escuelas e, enlaces_v2 en where e.id>0 and e.nivel=22 and e.cct=en.cct and en.anio=2013 group by cct;'
			sql2 = 'select id_cct,turnos,puntaje_espaniol,puntaje_matematicas, alumnos_que_contestaron_total, alumnos_en_nivel0_espaniol,alumnos_en_nivel0_matematicas,alumnos_en_nivel1_matematicas,alumnos_en_nivel2_matematicas,alumnos_en_nivel3_matematicas,alumnos_en_nivel1_espaniol,alumnos_en_nivel2_espaniol,alumnos_en_nivel3_espaniol, poco_confiables from enlaces_v2 where anio=2013 and id_cct=* order by turnos;';
			actualizaRanking(1,sql1,sql2)
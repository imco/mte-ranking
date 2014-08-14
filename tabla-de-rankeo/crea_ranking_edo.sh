#!/bin/bash

for i in 12 13 22
do
	for j in {1..32}
	do
		mysql -u root -p'Imco12345' imco_cte_optimizada -e "create temporary table temp_rank(rank_nacional bigint not null auto_increment primary key,turno int, id_cct bigint);alter table temp_rank add index (id_cct, turno);insert into temp_rank (id_cct,turno) select e.id,r.turnos_eval from escuelas e, escuelas_para_rankeo r where e.entidad=$j and e.nivel=$i and e.id=r.id and r.rank_nacional is not null and r.poco_confiables / r.total_evaluados<.1 order by e.promedio_general desc, e.poco_confiables/e.total_evaluados asc, e.pct_reprobados asc, pct_nivel3 desc, pct_nivel2 desc, pct_nivel1 desc;update escuelas_para_rankeo r, temp_rank t set r.rank_entidad =t.rank_nacional where r.id=t.id_cct and r.turnos_eval=t.turno;"
	done
done
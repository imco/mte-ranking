#!/bin/bash
rm *.csv
python crea_ranking.py primaria|sed -r "s/(\[|'|\]| )//g" > ranking_primaria.csv
python crea_ranking.py secundaria|sed -r "s/(\[|'|\]| )//g" > ranking_secundaria.csv
python crea_ranking.py bachillerato|sed -r "s/(\[|'|\]| )//g" > ranking_bachillerato.csv
cat ranking* > ranking_total.csv
#!/bin/bash
#./enlace_bachillerato.sh NAC_ESCUELAS_EMS2014.csv enlace_prepas_2014
rm $2.psv $2_bis.psv $2_v2.psv $2_v3.psv $2_v4.csv
cut -d "|" -f3-5,13,18-21,30-33 $1 > $2.psv
cut -d "|" -f12 $1 > $2_bis.psv
awk 'BEGIN{FS="|";OFS="|"}{for(i=5; i<=NF; i++){$i=$i/100;} print $0}' $2.psv> $2_v2.psv
paste -d "|" $2_v2.psv $2_bis.psv > $2_v3.psv
python crea_base_prepas_2013_v2.py $2_v3.psv | sed -r "s/(\[|'|\]| )//g"  > $2_v4.csv
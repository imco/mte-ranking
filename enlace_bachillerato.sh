#!/bin/bash
#./enlace_bachillerato.sh NAC_ESCUELAS_EMS2014.csv enlace_prepas_2014
rm $2.psv $2_v2.psv $2_v3.csv
cut -d "|" -f3-5,13,18-21,30-33 $1 > $2.psv
awk 'BEGIN{FS="|";OFS="|"}{for(i=5; i<=NF; i++){$i=$i/100;} print $0}' $2.psv> $2_v2.psv
python crea_base_prepas_2013_v2.py $2_v2.psv | sed -r "s/(\[|'|\]| )//g"  > $2_v3.csv
#!/bin/bash
rm primaria_poco_confiable.psv secundaria_poco_confiable.psv
cut -d "|" -f3-4,71-75 NACIONAL_RESUL_ESC_GRADO_ASIGNATURA_primaria.csv > primaria_poco_confiable.psv
cut -d "|" -f3-4,51-54 NACIONAL_RESUL_ESC_GRADO_ASIGNATURA_sec.csv > secundaria_poco_confiable.psv
python  -W error poco_confiable_x_grado.py primaria_poco_confiable.psv 4 primaria 3
python  -W error poco_confiable_x_grado.py secundaria_poco_confiable.psv 3 secundaria 1
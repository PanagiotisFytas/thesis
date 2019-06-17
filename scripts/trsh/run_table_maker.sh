#!/bin/bash

OUT_DIR=/home/yannis/Thesis/scripts/outputs
TEX_DIR=/home/yannis/Thesis/tables
for i in 0 1 2 3 4; do
    python3 table_maker.py $OUT_DIR/SP_nopriority_$i.out $OUT_DIR/PB_$i.out > $TEX_DIR/naivevsbpor$i.tex
done

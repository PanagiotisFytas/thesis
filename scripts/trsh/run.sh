for prees in $(seq 1 3)
do
	for mem_model in SB PB
	do 
	 ./driver.sh $mem_model $prees
	done
done

#!/bin/env bash

export NSETS=4

for setnum in `seq 1 $NSETS`;
do
    for corner in "LF" "LR" "RF" "RR";
    do
	export filename="SET$setnum-$corner.sh" 
	echo "#!/usr/bin/env bash"        > $filename
	echo "export SETNUM=$setnum"     >> $filename
	echo "export POSITION=$corner"   >> $filename
	cat base.sh                      >> $filename

	chmod +x $filename
    done
	

done

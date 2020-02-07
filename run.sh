for i in 1 2 3 4
do
	python main.py -d $i &
done

wait

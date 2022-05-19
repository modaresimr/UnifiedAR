onINT() {
	read -n1 -p "Kill runnings? [y,n]" doit 
	case $doit in
	  y|Y) pkill -P $$ ;;
	  n|N) echo no ;;
	  *) echo dont know ;; 
	esac
        exit
}

trap "onINT" SIGINT

parallel --eta   -j 8 'echo run {1} on data {2} and segm {3};GOTOBLAS_MAIN_FREE=1 python main.py -c {1} -d {2} -s {3}  -st 0 ' ::: 0 :::  {1..3}  ::: {0..2}


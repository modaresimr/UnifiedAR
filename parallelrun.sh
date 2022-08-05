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
export logdir=logs/$(date +%Y-%m-%d-%H-%M-%S)
mkdir -p $logdir
parallel --eta  -j 8 'echo run {1} on data {2} and segm {3};GOTOBLAS_MAIN_FREE=1 python main.py -c {1} -d {2} -s {3} -f 0  -st 0 > $logdir/c={1}-d={2}-s={3}-f=0-st=0 2> >(tee -a $logdir/c={1}-d={2}-s={3}-f=0-st=0 >&2)' ::: 0 :::  {0..3}  ::: {0..2}


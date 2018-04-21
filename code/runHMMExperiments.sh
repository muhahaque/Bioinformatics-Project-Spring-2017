#a quick shell script for running our experiments for HMMs
get_data() {
  echo ""
  echo "STARTED"
  echo ""
#train on sets of size 1 through 10, incrementing by 1
  for ((k=1; k <= 10; k=k+1)) do
    #echo "K: $k"
    python parseData.py benchmark1975.txt $k 0
    #echo "===================="
  done

      #train on sets of size 20 through 90, incrementing by 10
  for ((k=20; k <= 90; k=k+10)) do
    #echo "K: $k"
    python parseData.py benchmark1975.txt $k 0
    #echo "===================="
  done

      #train on sets of size 100 through 1300, incrementing by 300
  for ((k=100; k <= 1300; k=k+300)) do
    #echo "K: $k"
    python parseData.py benchmark1975.txt $k 0
    #echo "===================="
  done
}

get_data

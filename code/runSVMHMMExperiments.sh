#a quick shell script for running our experiments for svm hmms
get_data() {
  echo ""
  echo "STARTED"
  echo ""

  for ((k=1; k <= 10; k=k+1)) do
    echo "K: $k"
    for ((trial=1; trial<=1; trial=trial+1)) do
      #echo "Trial: $trial"
      for h in 0.01 0.1 1 5
      do
        echo "C-val: $h"
        python parseData.py benchmark1975.txt $k 1
        mv svmTrainInput svm_binaries/
        mv svmTestInput svm_binaries/
        cd svm_binaries/
        ./svm_hmm_learn -c $h -e 0.55 svmTrainInput protein_learner.model
        ./svm_hmm_classify svmTestInput protein_learner.model classify.tags
        cd ..
        python parseData.py benchmark1975.txt $k 0
        cd svm_binaries/
        rm svmTrainInput
        rm svmTestInput
        cd ..
        echo ""
      done
      echo ""
    done
    echo "===================="
  done

  for ((k=20; k <= 90; k=k+10)) do
    echo "K: $k"
    for ((trial=1; trial<=1; trial=trial+1)) do
      echo "Trial: $trial"
      for h in 0.01 0.1 1 5
      do
        echo "C-val: $h"
        python parseData.py benchmark1975.txt $k 1
        mv svmTrainInput svm_binaries/
        mv svmTestInput svm_binaries/
        cd svm_binaries/
        ./svm_hmm_learn -c $h -e 0.55 svmTrainInput protein_learner.model
        ./svm_hmm_classify svmTestInput protein_learner.model classify.tags
        cd ..
        python parseData.py benchmark1975.txt $k 0
        cd svm_binaries/
        rm svmTrainInput
        rm svmTestInput
        cd ..
        echo ""
      done
      echo ""
    done
    echo "===================="
  done
  
  for ((k=100; k <= 1300; k=k+300)) do
    echo "K: $k"
    for ((trial=1; trial<=1; trial=trial+1)) do
      echo "Trial: $trial"
      for h in 0.01 0.1 1 5 
      do
        echo "C-val: $h"
        python parseData.py benchmark1975.txt $k 1
        mv svmTrainInput svm_binaries/
        mv svmTestInput svm_binaries/
        cd svm_binaries/
        ./svm_hmm_learn -c $h -e 0.55 svmTrainInput protein_learner.model
        ./svm_hmm_classify svmTestInput protein_learner.model classify.tags
        cd ..
        python parseData.py benchmark1975.txt $k 0
        cd svm_binaries/
        rm svmTrainInput
        rm svmTestInput
        rm classify.tags
        cd ..
        echo ""
      done
      echo ""
    done
    echo "===================="
  done
}

get_data

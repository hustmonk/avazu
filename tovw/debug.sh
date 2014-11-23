set -e
vw=~/local/vowpal_wabbit-7.6/vowpalwabbit/vw
local_dir="./"
function train(){
    train_file=$1
    test_file=$2
    ${vw} ${local_dir}${train_file} -c -k -b 26 --loss_function logistic --passes 5 -q ab -q bc -q ac -f ${local_dir}rotten.model.vw
    ${vw} ${local_dir}${test_file} -t -i ${local_dir}rotten.model.vw -p ${local_dir}rotten.rawpreds.txt
}

train_file="train.csv"
test_file="test.csv"
if [ "$1" == "train" ]; then
    train ${train_file} ${test_file}
    python out.py >sub.csv
    zip sub.zip sub.csv
elif [ "$1" == "debug" ]; then
    train ${train_file} ${test_file}
    cut -f1 -d$' ' ${test_file} > y
    python out.py >sub.csv
    python metric.py 
fi

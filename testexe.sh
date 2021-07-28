sleep 1
read varname
#line=$(head -n 1 /home/melkan/work/FastCGI/count)
#echo $(($line + 1)) >> /home/melkan/work/FastCGI/ledger
#echo $(($line + 1)) > /home/melkan/work/FastCGI/count
echo $varname >> /home/melkan/work/FastCGI/ledger
#date
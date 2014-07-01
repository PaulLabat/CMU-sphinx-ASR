cut -d" " -f 2- frenchtraining.dic > tmp.list.phone
sed 's/ /\n/g' tmp.list.phone > tmp2.list.phone
sort -u tmp2.list.phone > tmp3.list.phone
tail -n +2 "tmp3.list.phone" >> frenchtraining.phone
rm tmp.list.phone tmp2.list.phone tmp3.list.phone
echo "SIL" >> frenchtraining.phone


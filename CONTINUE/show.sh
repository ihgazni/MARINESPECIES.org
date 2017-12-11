cat seq.record
printf '\n'
cat children_seq.record
printf '\n'
tree ../Biota | egrep -v "json" | egrep "files"

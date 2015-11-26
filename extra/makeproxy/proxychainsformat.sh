cat file | grep -v '!'|awk -F' ' '{ print $7" "$3 }' | tr ':' ' ' | tr '[A-z]' '[a-z]'| uniq | shuf | awk 'NF'
cat file | grep '!' |awk -F' ' '{ print $6" "$3 }' |tr ':' ' ' | tr '[A-z]' '[a-z]'| uniq | shuf | awk 'NF'

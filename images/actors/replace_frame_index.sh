for action in $(ls dog)
do
    for frame in $(ls dog/"$action"/*svg)
    do
        chain=$(echo "$frame" | cut -d "/" -f 3 | cut -d "." -f 1 | cut -d "_" -f 2-3)
        bbe $frame -e s/$action\ 0_0/$action\ $chain/ > temp
        mv temp $frame
    done
done


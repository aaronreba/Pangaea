for action in $(ls dog)
do
    for frame in $(ls dog/"$action"/*svg)
    do
        saveas=$(echo $frame | cut -d "." -f 1).png
        echo $frame $saveas
        inkscape -f $frame -e $saveas -w 45 -h 45
    done
done


#!/bin/bash

#converts ps to pdf
#reads file number from prompt
read -p "name: " name

#calls ps2pdf from ghostscript
ps2pdf "$name.ps" "$name.pdf"

#ask if .ps should be removed
while true
do
    read -p "Del .ps? (y/n) " answer
    case $answer in
        [yYjJ]* )   rm "$name$num.ps"
                    break;;
        [nN]* )     break;;
        * )         echo "No."
                    break;;
    esac
done

#ask if result should be shown
while true
do
    read -p "Show? (y/n) " answer
    case $answer in
        [yYjJ]* )   xreader "$name$num.pdf"
                    break;;
        [nN]* )     exit;;
        * )         echo "No."
                    break;;
    esac
done

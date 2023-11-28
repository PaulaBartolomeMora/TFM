#!/bin/bash

dir_zip="zipped/"
dir_dest="unzipped/"
dir_results="results/"

pip freeze > "before.txt" 

if [ -f requirements.txt ]; then
    echo "Instalando paquetes"
    pip install -r requirements.txt
    echo "Instalación completada"
    #pip freeze > "after.txt" 
else
    echo "El archivo requirements.txt no existe"
fi

if [ ! -d "$dir_dest" ]; then
    echo "Creando directorio destino unzipped/"
    mkdir -p $dir_dest
else
    echo "Existe $dir_dest"
fi

if [ ! -d "$dir_results" ]; then
    echo "Creando directorio destino results/"
    mkdir -p $dir_results
else
    echo "Existe $dir_results"
fi

if [ ! -d "$dir_zip" ]; then
    echo "No existe $dir_zip" 
else
    ls $dir_zip
    if [ "$(ls -A $dir_dest)" ]; then
        echo "Descompresión ya realizada anteriormente"
    else
        unzip $dir_zip"*.zip" -d $dir_dest
        echo "Descompresión completada" 
    fi 
fi

if [ -f datasamples.py ]; then
    echo "-----------------------------------------------------"
    echo "Ejecutando archivo"
    echo "-----------------------------------------------------"
    python3 datasamples.py 
else
    echo "El archivo datasamples.py no existe"
fi

echo "Ejecución completada"

pip uninstall -r requirements.txt
pip freeze > "before2.txt" 
diff before.txt before2.txt

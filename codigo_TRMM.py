import pandas as pd
import os, patoolib

#Criar uma lista com todos os aquivos .gz
pasta_arqsgz = './Arquivos NASA/'
arquivos = os.listdir(pasta_arqsgz) #listdir fucntion: returns a list containing the names of the entries in the directory given by path 
gzip_files = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.gz')]
pasta_HDF = './Arquivos HDF/'

#https://www.youtube.com/watch?v=FdGploQo4Ko
def extrair_arquivos(arq_gzip, pasta_gzs, pasta_salvar):
    diret = pasta_gzs + arq_gzip
    patoolib.extract_archive(diret, outdir=pasta_salvar)

for gzip in gzip_files:
    extrair_arquivos(gzip, pasta_arqsgz, pasta_HDF)
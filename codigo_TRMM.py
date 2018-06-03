import pandas as pd
import os, patoolib
import numpy as np
from pyhdf.SD import SD, SDC

#Criar uma lista com todos os aquivos .gz
pasta_arqsgz = './Arquivos NASA/'
arquivos = os.listdir(pasta_arqsgz) #listdir fucntion: returns a list containing the names of the entries in the directory given by path 
gzip_files = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.gz')]
pasta_HDF = './Arquivos HDF/'

#https://www.youtube.com/watch?v=FdGploQo4Ko
def extrair_arquivos(arquivo, pasta_gzs, pasta_salvar):
    diret = pasta_gzs + arquivo
    patoolib.extract_archive(diret, outdir=pasta_salvar)
'''
for gzip in gzip_files:
    extrair_arquivos(gzip, pasta_arqsgz, pasta_HDF)'''

def ler_hdf_precipitacao(arquivo, pasta):
    diret = pasta + arquivo
    hdf = SD(diret, SDC.READ)
    
    #Conjuntos de dados disponíveis
    #print(hdf.datasets())
    #Atributos 
    #print(hdf.attributes())
    
    #Obter resolução espacial e as coordenadas das "bordas"
    lista = hdf.attributes()['GridHeader'].replace(';','').split('\n')
    atrs = {}
    for atr in ['LatitudeResolution=','LongitudeResolution=','NorthBoundingCoordinate=','SouthBoundingCoordinate=','EastBoundingCoordinate=','WestBoundingCoordinate=']:
        valor = [float(lista[n][len(atr):]) for n, x in enumerate(lista) if atr in x]
        atrs[atr] = valor[0]

    #Selecionar o conjunto de dados desejado ('precipitation'): dados de precipitação
    precip = hdf.select('precipitation')
    precip = precip[:] #Array com os dados de precipitação no formato nlon x nlat
    precip = np.transpose(precip) #Matriz transposta para termos nlat x nlon
    #  Missing value = -9999.9; Set all the missing values less than 0 to NaNs
    np.putmask(precip,precip<0,np.nan)

    return(precip)
    #Primeiro elemento de todos: print(d1[:1][0][0])

dados_precip = []    
for i in range(len(os.listdir(pasta_HDF))):
    dados_precip.append(ler_hdf_precipitacao(os.listdir(pasta_HDF)[i], pasta_HDF))
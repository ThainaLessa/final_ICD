import pandas as pd
import os, patoolib
import numpy as np
from pyhdf.SD import SD, SDC
from random import choice

import matplotlib.pylab as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker

#https://www.youtube.com/watch?v=FdGploQo4Ko
def extrair_arquivos(arquivo, pasta_gzs, pasta_salvar):
    diret = pasta_gzs + arquivo
    patoolib.extract_archive(diret, outdir=pasta_salvar)

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
    return precip

def criar_serie(dados, lats, longs):
    #Criar série de dados estimados por pixel, em um DataFrame
    df_series = pd.DataFrame(columns=longs, index=lats)
    df_acum = pd.DataFrame(columns=longs, index=lats)

    for nlat, lat in enumerate(lats):
        for nlon, lon in enumerate(longs):
            serie = []
            for precip in dados_precip:
                serie.append(precip[nlat][nlon])
            df_series[lon][lat] = serie
            df_acum[lon][lat] = np.sum(serie)
    
    return df_series, df_acum

#Funções para Bootstrap
METRICAS = {'max': max, 'acum': sum}
def reamostragem(dados, n):
    amostras = []
    for i in range(n):
        amostras.append([choice(dados) for i in range(len(dados))])
    return amostras

def intervalo_confiança(dados):
    df = pd.Series(dados)
    return {'média': df.mean(), 'q1': df.quantile(.025), 'q3': df.quantile(.975)}

def boots(dados_estimados, metrica):
    amostras = reamostragem(dados_estimados, 100)
    res = []
    for amostra in amostras:
        res.append(METRICAS[metrica](amostra))
    return intervalo_confiança(res)

def tabela_e_media(dados, lat, lon, metrica):
    calc = boots(dados[lon][lat], metrica)
    media = '%.2f'%calc['média']
    q1 = '%.2f'%calc['q1']
    q3 = '%.2f'%calc['q3']
    if metrica == 'acum':
        met = 'Acumulado |'
    else:
        met = 'Máximo    |'
    print(met+media.center(9)+'|'+q1.center(14)+'|'+q3.center(14))
    return calc['média']

def criar_mapa(dados, lats, longs, titulo):
    #https://github.com/SciTools/cartopy
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.set_extent([-37.1, -33.9, -11, -8], crs=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    
    m = ax.pcolormesh(longs,\
                    lats,\
                    dados,\
                    vmin=0,\
                    vmax=np.amax(dados))

    cbar = plt.colorbar(m,ax=ax)
    cbar.set_label('mm')

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, alpha=0.35)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlocator = mticker.FixedLocator([-34, -35, -36, -37])

    plt.title('Precipitação {}'.format(titulo))
    plt.savefig('{}.jpg'.format(titulo))

if __name__ == "__main__":
    #Criar uma lista com todos os aquivos .gz
    pasta_arqsgz = './Arquivos NASA/'
    arquivos = os.listdir(pasta_arqsgz) 
    gzip_files = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.gz')]
    pasta_HDF = './Arquivos HDF/'

    if os.listdir(pasta_HDF) == []:
        for gzip in gzip_files:
            extrair_arquivos(gzip, pasta_arqsgz, pasta_HDF)
    
    #Pegar dados dos arquivos .hdf
    dados_precip = []    
    for i in range(len(os.listdir(pasta_HDF))):
        dados_precip.append(ler_hdf_precipitacao(os.listdir(pasta_HDF)[i], pasta_HDF))

    latitudes = np.arange(-10.25, -9, 0.25)
    longitudes = np.arange(-36.5, -35, 0.25)

    series, acum = criar_serie(dados_precip, latitudes, longitudes)

    df_acum = pd.DataFrame(columns=longitudes, index=latitudes)
    #Pegar médias obtidas com bootstrap e imprimir média e intervalo de confiança de reamostragem por Bootstrap
    for lat in list(series.index):
        for lon in list(series.columns):
            print(13*' '+'Latitude: {}; Longitude: {}'.format(lat,lon),'\n',10*' '+38*'-')
            print(10*' '+'|  Média  |  1º quartil  |  3º quartil')
            for metrica in list(METRICAS.keys()):
                if metrica == 'acum':
                    df_acum[lon][lat] = tabela_e_media(series, lat, lon, metrica)
                else:
                    tabela_e_media(series, lat, lon, metrica)
    
    for i in list(acum.columns):
        acum[i] = pd.to_numeric(acum[i], errors='coerce')
        df_acum[i] = pd.to_numeric(df_acum[i], errors='coerce')

    latitudes = np.arange(-10.25, -8.75, 0.25)
    longitudes = np.arange(-36.5, -34.75, 0.25)
    criar_mapa(acum.values, latitudes, longitudes, 'acumulada TRMM')
    criar_mapa(df_acum.values, latitudes, longitudes, 'acumulada - Bootstrap')
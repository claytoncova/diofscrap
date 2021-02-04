#!/usr/local/bin/python3.6
"""
Pré-requisito instalar por padrão 'resquests', 'getopt' e 'bs4' via pip.

Código didático e prova de conceito para captura de massa de informação
do Diário Oficial do Estado de Rondônia. Pode ser utilizado para o
desenvolvimento de rotinas para análise de dados em amplitude, big data.
Basicamente o código consulta uma chamada http para listagem dos
arquivos e depois executa o download com ajuda de threads.

Código disponibilizado pela licença X11, licença MIT (c).
2018. Clayton G. C. Santos.
"""
import threading
import sys
import time
import os
import datetime
import getopt
import requests
from bs4 import BeautifulSoup

def get_help(error):
    """Erro padrão e parâmetros não obrigatórios"""
    print('Uso:')
    print('diofscrap.py -i <DataInicio> -f <DataFim> -o <Destino> -t <Threads>')
    if error:
        sys.exit(2)
    else:
        sys.exit()

def get_urls(date1, date2):
    """Busca as URLs dos arquivos"""
    start = datetime.datetime.strptime(date1, '%d-%m-%Y')
    end = datetime.datetime.strptime(date2, '%d-%m-%Y')
    link_list = []
    step = datetime.timedelta(days=1)
    print('Listando arquivos disponíveis de '+date1+' até '+date2+'...')
    while start <= end:
        #Busca o nome dos arquivos pdf da url abaixo
        response = requests.get('http://www.diof.ro.gov.br/diarios/?cf_time='\
        +start.date().strftime('%d-%m-%Y'))
        start += step
        #Faz o parser do HTML pra extrair a URL e adiciona a uma lista
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            link_list.append(link.get('href'))
            print(link.get('href'))
    return link_list

def download(link, filelocation):
    """Função de download acionada pelas threads"""
    req = requests.get(link, stream=True)
    with open(filelocation, 'wb') as fill:
        for chunk in req.iter_content(1024):
            if chunk:
                fill.write(chunk)

def check_thread(filelink, numt):
    """Define o número de threads e limita a execução, padrão 5 threads."""
    while threading.activeCount() > numt:
        os.system("clear")
        print('Baixando arquivos:')
        print("/"+" "+filelink.replace("\n", ""))
        time.sleep(0.05)


def main(argv):
    """Parâmetros padrão"""
    start_date = '01-04-2005'
    end_date = datetime.date.today().strftime('%d-%m-%Y')
    destino = ''
    threads = 5
    #Tratamento de parâmetros na linha de comando
    if len(sys.argv) == 1:
        get_help(False)
    else:
        try:
            opts, args = getopt.getopt(argv, "hi:f:o:t:",\
            ["data-inicio=", "data-fim=", "destino=", "threads=", ])
        except getopt.GetoptError:
            get_help(True)
    for opt, arg in opts:
        if opt == '-h':
            get_help(False)
        elif opt in ("-i", "--data-inicio"):
            start_date = arg
        elif opt in ("-f", "--data-fim"):
            end_date = arg
        elif opt in ("-o", "--destino"):
            destino = arg
        elif opt in ("-t", "--threads"):
            threads = int(arg)
    #Recupera a lista de arquivos disponíveis no Diof
    filelist = get_urls(start_date, end_date)
    #Efetua o download de cada arquivo
    for filelink in filelist:
        print(filelink)
        filename = destino+filelink.split('/')[-1].replace("\n", "")
        #Cria threads para download com a função de mesmo nome
        download_thread = threading.Thread(target=download, \
        args=(filelink.replace("\n", ""), filename))
        download_thread.start()
        check_thread(filelink, threads)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass

    finally:
        print("Finalizando...")

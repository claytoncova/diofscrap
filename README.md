# DIOFScrap - aplicação para download dos arquivos do Diário Oficial do Estado de Rondônia. 

Pré-requisito instalar por padrão 'resquests', 'getopt' e 'bs4' via pip.

Código didático e prova de conceito para captura de massa de informação
do Diário Oficial do Estado de Rondônia. Pode ser utilizado para o
desenvolvimento de rotinas para análise de dados em amplitude, big data.
Basicamente o código consulta uma chamada http para listagem dos
arquivos e depois executa o download com ajuda de threads.

Código disponibilizado pela licença X11, licença MIT (c).

2018. Clayton G. C. Santos.

Python: V. 3.6

SysOp testado: MacOs High Sierra

LibDep: 

    requests, bs4 e getopt

Instalação das dependências:

    pip install requests getopt bs4

Utilização: 

    diofscrap.py -i <DataInicio> -f <DataFim> -o <Destino> -t <Threads>
    diofscrap.py --data-inicio=<DataInicio> --data-fim=<DataFim> --destino=<Destino> --threads=<Threads>
    
Parâmetros:
    
    DataInicio: data inicial do diário a ser baixado. Default: 01-04-2005.
    DataFim: data final do diário a ser baixado. Default: data atual do sistema.
    Destino: caminho do destino. Default: pasta atual na execução.
    Threads: número de threads utilizada. Default: 5.
    
Clayton G. C. Santos

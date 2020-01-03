import psycopg2
import pyodbc
import unicodedata
import re
from configparser import ConfigParser
import fdb
from time import sleep

class conexao(object):
    def __init__(self, nome_conexao=None, host=None, port=None, db=None, usr=None, pwd=None):
        nome_conexao = nome_conexao.lower()
        
        if nome_conexao == "postgres":
            if port is None:
                port = "5432"
                
            self._conn = psycopg2.connect(host=host, port=port, database=db, user=usr, password=pwd)
            self._conn.autocommit = False
            self._cur = self._conn.cursor()
        elif nome_conexao == "dbmakerodbc":
            #self._conn = pyodbc.connect("DSN=%s" %db)
            self._conn = pyodbc.connect(f'DSN={db};UID={usr};PWD={pwd}')
            self._conn.autocommit = False
            self._cur = self._conn.cursor()
        elif nome_conexao == "sqlserverodbc":
            self._conn = pyodbc.connect(f'DSN={db};UID={usr};PWD={pwd}')
            self._conn.autocommit = False
            self._cur = self._conn.cursor()
        elif nome_conexao == "firebird":
            if port is None:
                port = "3050"            
            
            self._conn = fdb.connect(dsn=f'{host}/{port}:{db}', user=f'{usr}', password=f'{pwd}')
            self._conn.autocommit = False
            self._cur = self._conn.cursor()
        else:            
            self._conn = None
            self._cur = None

    def executar(self, sql, args=None):        
        if args is None:
            self._cur.execute(sql)
        else:
            self._cur.execute(sql, args)
        
        return None
    
    def consultar(self, sql):
        rs = None
        self._cur.execute(sql)
        rs = self._cur.fetchall()              
        return rs
    
    def proxima_chave(self, tabela, chave):
        sql = 'select max(' + chave + ') from ' + tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk + 1
        
    def efetivar(self):
        self._conn.commit()
        
    def fechar(self):
        self._cur.close()
        self._conn.close()

def remove_ace(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \/\\\-]', '', palavra_sem_acento)

class configurador(object):
    def __init__(self, file_config = "config/config.cfg"):
       self.file_config = file_config
       self.__config_parser = ConfigParser()
       self.__config_parser.read(file_config)

    def get_file_config(self):
        return self.file_config

    def set_file_config(self, file_config):
        self.file_config = file_config
        self.__config_parser = ConfigParser()
        self.__config_parser.read(file_config)

    def get_sessao(self, sessao):
        return dict(self.__config_parser[sessao])

    def get_item_sessao(self, sessao, item_sessao):
        return dict(self.__config_parser[sessao])[item_sessao]

class conexao_dbmaker(object):
    def __init__(self, tentativas_conexao=None, dsn=None, usr=None, pwd=None):
        self.__tentativas_conexao = tentativas_conexao
        self.__dsn = dsn
        self.__usr = usr
        self.__pwd = pwd

        if (tentativas_conexao and dsn and usr and pwd) != None:
            self.__conn_dbmaker = self.conectar(tentativas_conexao=tentativas_conexao, dsn=dsn, usr=usr, pwd=pwd)
        else:
            self.__conn_dbmaker = None

    def conectar(self, tentativas_conexao=None, dsn=None, usr=None, pwd=None):
        if self.__tentativas_conexao == None:
            self.__tentativas_conexao = tentativas_conexao
        
        if self.__dsn == None:
            self.__dsn = dsn

        if self.__usr == None:
            self.__usr = usr
        
        if self.__pwd == None:
            self.__pwd = pwd

        tentativas = 1

        while tentativas <= self.__tentativas_conexao: # quantidade de tentativas a cada 5 segundos em caso de "number of transactions exceeds" ou "number of connections exceeds"
            try:
                self.__conn_dbmaker = conexao(nome_conexao="DBMakerOdbc", db=self.__dsn, usr=self.__usr, pwd=self.__pwd)
                tentativas = self.__tentativas_conexao
            except Exception as e:
                if ("number of transactions exceeds" or "number of connections exceeds") in str(e).lower():
                    sleep(5)                    
                else:
                    tentativas = self.__tentativas_conexao
                
                if tentativas == self.__tentativas_conexao:
                   raise
                
            tentativas = tentativas + 1

        return self.__conn_dbmaker


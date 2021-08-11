import psycopg2
import pyodbc
import fdb
from time import sleep

class conexao(object):
    def __init__(self, nome_conexao=None, host=None, port=None, db=None, usr=None, pwd=None):
        nome_conexao = nome_conexao.lower()
        
        if nome_conexao == "postgres":
            if port is None:
                port = "5432"
                
            self.__conn = psycopg2.connect(host=host, port=port, database=db, user=usr, password=pwd)
            self.__conn.autocommit = False
            self.__cur = self.__conn.cursor()
        elif nome_conexao == "dbmakerodbc":
            self.__conn = pyodbc.connect(f'DSN={db};UID={usr};PWD={pwd}')
            self.__conn.autocommit = False
            self.__cur = self.__conn.cursor()
        elif nome_conexao == "sqlserverodbc":
            self.__conn = pyodbc.connect(f'DSN={db};UID={usr};PWD={pwd}')
            self.__conn.autocommit = False
            self.__cur = self.__conn.cursor()
        elif nome_conexao == "firebird":
            if port is None:
                port = "3050"            
            
            self.__conn = fdb.connect(dsn=f'{host}/{port}:{db}', user=f'{usr}', password=f'{pwd}')
            self.__conn.autocommit = False
            self.__cur = self.__conn.cursor()
        else:            
            self.__conn = None
            self.__cur = None

    def executar(self, sql, args=None):        
        if args is None:
            self.__cur.execute(sql)
        else:
            self.__cur.execute(sql, args)
        
        return None
    
    def consultar(self, sql):
        rs = None
        self.__cur.execute(sql)
        rs = self.__cur.fetchall()              
        return rs
    
    def proxima_chave(self, tabela, chave):
        sql = 'select max(' + chave + ') from ' + tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk + 1
        
    def efetivar(self):
        self.__conn.commit()
        
    def fechar(self):
        self.__cur.close()
        self.__conn.close()
    
    def cursor(self):
        return self.__cur
    
    def fechar_cursor(self):
        self.__cur.close()
    
    def fechar_conexao(self):
        self.__conn.close()
    
    def rollback(self):
        self.__conn.rollback()

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
                if (str(e).lower() == "number of transactions exceeds") or (str(e).lower() == "number of connections exceeds"):
                    sleep(5)                    
                else:
                    tentativas = self.__tentativas_conexao
                
                if tentativas == self.__tentativas_conexao:
                   raise
                
            tentativas = tentativas + 1

        return self.__conn_dbmaker
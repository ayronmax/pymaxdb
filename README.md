# pymaxdb
Projeto que visa padronizar a comunicação com alguns bancos de dados.
## Objetivo
- Padronizar a comunição para bancos de dados distintos; 
- Utilizar métodos padronizados para realizar operações em bancos de dados distintos;
- Controlar operações que envolvem atualizações no banco de dados.
## Instalação
```sh
pip install pymaxdb
```
## Utilização
A comunicação é realizada através da instanciação da classe ***conexao()***, que recebe em um de seus parâmetros o nome do banco de dados que se deseja conectar. O parmêtro ***nome_conexao*** recebe nomes pré-definidos, que podem ser: Postgres, (conexão PostgreSQL), DBMakerODBC (necessário criação prévia de uma conexão DBMaker ODBC), SQLServerODBC (conexão ODBC SQL Server) e Firebird (conexão Firebird).

```python
import pymaxdb

try:
    # Conexão PostgreSQL
    # con = pymaxdb.conexao(nome_conexao='postgres', host='127.0.0.1', port='5432', db='nome_database', usr='usuário', pwd='senha')

    # Conexão DBMaker ODBC
    # con = pymaxdb.conexao(nome_conexao='dbmakerodbc', db='nome_dsn', usr='usuário', pwd='senha')  
    
    # Conexão SQLServer ODBC
    # con = pymaxdb.conexao(nome_conexao='sqlserverodbc', db='nome_dsn', usr='usuário', pwd='senha')
    
    # Conexão Firebird
    # con = conexao(nome_conexao='firebird', host='127.0.0.1', port='3050', db='/caminho_database/nome_database.fdb', usr='usuário', pwd='senha')

    # Retirar comentário de uma das conexões acima para exutar exemplo abaixo 
    con.executar('insert into nome_database values(1)')
    con.efetivar() # commit
    rs = con.consultar('select * from nome_database')
    print(rs)
    proximo_registro = con.proxima_chave('nome_database', 'campo_chave')
    print(proximo_registro)
    con.fechar() # close connection       
except Exception as e:    
    print(e)
```
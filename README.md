# pymaxdb
Projeto que visa padronizar a comunicação com alguns bancos de dados.

## Objetivo
- Padronizar a conexão com bancos de dados distintos; 
- Utilizar métodos padronizados para realizar operações no bancos de dados;
- Melhorar controle de operações que envolvem atualizações no banco de dados.

## Instalação
```sh
pip install pymaxdb
```

## Utilização
A comunicação é realizada através da instanciação da classe ***conexao***, que recebe em um de seus parâmetros o nome do banco de dados que se deseja conectar. O parâmetro ***nome_conexao*** recebe nomes pré-definidos, que podem ser: Postgres, (conexão PostgreSQL), DBMakerODBC (necessário criação prévia de uma conexão DBMaker ODBC), SQLServerODBC (conexão SQL Server ODBC) e Firebird (conexão Firebird).

```python
from pymaxdb import conexao

try:
    # Conexão PostgreSQL
    con = conexao(nome_conexao='postgres', host='127.0.0.1', port='5432', db='nome_database', usr='usuário', pwd='senha')

    # Conexão DBMaker ODBC
    # con = conexao(nome_conexao='dbmakerodbc', db='nome_dsn', usr='usuário', pwd='senha')  
    
    # Conexão SQL Server ODBC
    # con = conexao(nome_conexao='sqlserverodbc', db='nome_dsn', usr='usuário', pwd='senha')
    
    # Conexão Firebird
    # con = conexao(nome_conexao='firebird', host='127.0.0.1', port='3050', db='/caminho_database/nome_database.fdb', usr='usuário', pwd='senha')

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

O pacote também possui mais algumas classes e funções utilitárias:

- ***conexao_dbmaker***
  - Permite controlar a quantidade de tentativas de conexão ao DBMaker no caso do número de conexões permitidas exceder.

```python
from pymaxdb import conexao_dbmaker

try:
    conn_dbmaker = conexao_dbmaker(tentativas_conexao=10, db='nome_dsn', usr='usuário', pwd='senha')
except Exception as e:
    print(e)
```

- ***remove_ace***
  - Recebe uma string e retorna apenas letras, números e espaços.

- ***configurador***
  - Recebe o caminho completo de um arquivo de configuração separado por sessões do tipo chave e valor.

```sh
[config1]
chave1 = valor1
chave2 = valor2

[config2]
chave1 = valor1
chave2 = valor2
```
# pymaxdb
Projeto que visa padronizar a comunicação com alguns bancos de dados.
## Objetivo
- Padronizar a comunição em bancos de dados distintos; 
- Utilizar métodos padronizados para realizar operações em bancos de dados distintos;
- Controlar operações que envolvem atualizações no banco de dados.
## Instalação
```sh
pip install pymaxdb
```
## Utilização
A comunicação é realizada através da instanciação da classe ***conexao()***, que recebe em um de seus parâmetros o nome do banco de dados que se deseja conectar. O parmêtro nome_coenxao recebe nomes pré-definidos, que podem ser: Postgres, (conexão PostgreSQL), DBMakerODBC (necessário criação prévia de uma conexão ODBC), SQLServerODBC (conexão ODBC SQL Server) e Firebird (conexão Firebird).




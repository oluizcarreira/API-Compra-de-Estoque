# API-Compra-de-Estoque
API de gestão de estoque (compra) usando Python, Flask e MySQL

## Preparando o ambiente virtual
Criar a pasta do projeto, colar o arquivo 'main.py' e abrir no seu editor de código;
Executar os seguintes comandos no terminal:
cd <caminho_da_pasta_do_projeto>
py -m venv venv
venv\Scripts\activate

## Instalando bibliotecas
No terminal realizar os seguintes comandos:
pip install Flask 
pip install mysql-connector-python
pip install Flask-Mail
pip install reportlab 

## Criando o arquivo para configuração do email e senha para receber o email de aviso de estoque baixo
Na pasta do projeto, criar o arquivo 'config.py' e colocas as seguintes váriaveis:
email = '<email>'
senha = '<senha>'

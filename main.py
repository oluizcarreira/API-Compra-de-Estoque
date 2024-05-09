import mysql.connector
from flask import Flask, make_response, jsonify, request
from flask_mail import Mail, Message
from config import email, senha
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
#from apscheduler.schedulers.background import BackgroundScheduler

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='produtos',
)
    
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'teste'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/produtos', methods=['GET'])
def get_produtos():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM produto')
    meus_produtos = cursor.fetchall()

    produto = list()
    for pr in meus_produtos:
        produto.append(
            {
                'id': pr[0],
                'nome': pr[1],
                'descrição': pr[2],
                'valor': pr[3],
                'alíquota': pr[4]
            }
        )

    return make_response(
        jsonify(
            mensagem='Lista de produtos',
            dados=pr
        )
    )

@app.route('/cadastro', methods=['POST'])
def create_produto():
    pr = request.json
    '''cursor = mydb.cursor()
    sql = f"INSERT INTO produto (nome_produto, descricao_produto, valor_produto, aliquota_produto) VALUES ('{pr['nome_produto']}', '{pr['descricao_produto']}', {pr['valor_produto']}, {pr['aliquota_produto']})"
    cursor.execute(sql)
    mydb.commit()'''
    cnv = canvas.Canvas("meu_pdf.pdf")
    cnv.drawString(250, 450, f"{pr['nome_produto']}, {pr['descricao_produto']}, {pr['valor_produto']}, {pr['aliquota_produto']}")
    cnv.save()
    return make_response(
        jsonify(
            mensagem='PDF gerado com sucesso!',
            dados=pr
        )
    )

@app.route('/update', methods=['POST', 'GET'])
def update_produto():
    pr = request.json
    cursor = mydb.cursor()
    sql = f"UPDATE produto SET nome_produto = '{pr['nome_produto']}', descricao_produto = '{pr['descricao_produto']}', valor_produto = {pr['valor_produto']}, aliquota_produto = {pr['aliquota_produto']} WHERE idproduto = {pr['idproduto']}"
    cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
            mensagem='Produto atualizado com sucesso!',
            dados=pr
        )
    )

@app.route('/send', methods=['GET', 'POST'])
def send():
    cursor = mydb.cursor()
    cursor.execute("SELECT count(*) FROM produto")
    qtd = cursor.fetchone()[0]
    if qtd < 3:
        msg = Message(
            subject = 'Aviso de Estoque Baixo!',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = [app.config.get("MAIL_USERNAME")],
            body = f'''
            Seu estoque está abaixo de 3 produtos!

            '''
        )
        mail.send(msg)
        return make_response(
            jsonify(
                mensagem='Email enviado com sucesso!',
            )
        )
    else:
        return make_response(
            jsonify(
                mensagem='O estoque não está acabando!',
            )
        )

'''scheduler = BackgroundScheduler()
scheduler.start()
def verifica_estoque():
    cursor = mydb.cursor()
    cursor.execute("SELECT count(*) FROM produto")
    qtd = cursor.fetchone()[0]
    if qtd < 3:
        msg = Message(
            subject = 'Aviso de Estoque Baixo!',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = [app.config.get("MAIL_USERNAME")],
            body = f
            Seu estoque está abaixo de 3 produtos!

            
        )
        mail.send(msg)
        print('Email Enviado!')
    else:
        print('O estoque não está baixo!')
scheduler.add_job(verifica_estoque, 'interval', minutes=2)'''

if __name__ == '__main__':
    app.run(debug=True)
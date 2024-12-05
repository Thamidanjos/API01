from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senac@localhost:3306/apiestilorei'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)
# Modelo de Cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
# Criar o banco de dados (executar uma vez)
# Criar as tabelas diretamente ao iniciar o aplicativo
with app.app_context():
    db.create_all()

@app.route('/getcliente', methods=['GET'])
def busca_cliente():
    return jsonify({'nome':'Pedro','telefone':'00000-0000'})

#criar uma rota para retornar dados do banco de dados
@app.route('/getclientes', methods=['GET'])
def busca_clientes():
    clientes = Cliente.query.all()
    return jsonify([{'id':cliente.id,
                     'nome':cliente.nome,
                      'telefone':cliente.telefone} for cliente in clientes]) 

@app.route('/addcliente', methods=['POST'])
def add_cliente():
    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')

    if not nome:
        return jsonify({"error":"Nome é obrigatório!"}),400

    novo_cliente = Cliente(nome=nome, telefone=telefone)
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({"messagem":"Cliente adicionado com sucesso!"}),201

@app.route('/excluircliente/<int:id>', methods=['GET'])
def excluir_cliente(id):
    clientes = Cliente.query.get(id)

    if not clientes:
        return jsonify({"error":"Cliente não encontrado!"}),404
    
    db.session.delete(clientes)
    db.session.commit()

    return jsonify({"message": "Cliente excluído com sucesso!"}),200

if __name__=='__main__':
    app.run(debug=True)


import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "produtosdatabase.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Produto(db.Model):
    
    nome = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    
    def __repr__(self):
        return "<Nome: {}>".format(self.nome)
    
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        nome_produto = request.form.get("nome")
        if nome_produto:
            if Produto.query.filter_by(nome=nome_produto).first():
                pass
            else:
                try:
                    produto = Produto(nome=nome_produto)
                    db.session.add(produto)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
        else:
            pass    
    produtos = Produto.query.all()
    return render_template("index.html", produtos=produtos)
    
@app.route("/update", methods=["POST"])
def update():
    novoNome = request.form.get("novoNome")
    nomeAntigo = request.form.get("nomeAntigo")
    if novoNome and nomeAntigo:
        produto = Produto.query.filter_by(nome=nomeAntigo).first()
        if produto:
            try:
                produto.nome = novoNome
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
        else:
            pass
    else:
        pass
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    nome = request.form.get("nome")
    if nome:
        produto = Produto.query.filter_by(nome=nome).first()
        if produto:
            db.session.delete(produto)
            db.session.commit()
        else:
            pass
    else:
        pass
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
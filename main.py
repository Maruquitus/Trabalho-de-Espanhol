from flask import Flask, render_template, request
import random
import conjugador

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("telaquestao.html", pergunta="Padrão", itens=["Letra A", "Letra B", "Letra C", "Letra D"], resultado = "Nada")

@app.route('/', methods =["GET", "POST"])
def conjugacao():
    if request.method == "POST":
        text = request.form.get("text")

        opcoes = conjugador.conjugacoes(text)
        escolhidas = []
        while len(escolhidas) < 4:
            r = random.randint(0, len(opcoes)-1)
            if r not in escolhidas:
                escolhidas.append(r)

        print(text)
        return render_template("telaquestao.html", pergunta=f"Completa la oración con la conjugación correcta del verbo {text}: Yo _______ mucho", itens=[opcoes[escolhidas[0]], opcoes[escolhidas[1]], opcoes[escolhidas[2]], opcoes[escolhidas[3]]], resultado = conjugador.conjugar(text, 0, "singular"))

if __name__ == '__main__':
    app.run()
    
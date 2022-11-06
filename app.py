from flask import Flask, render_template, request
import random
import conjugador
import time

app = Flask(__name__)
DADOS_QUESTÕES = {
    1:{
        "pergunta":0,
        "frase":"Yo ______ mucho",
        "verbo":"Hablar",
        "resposta certa":"Hablo"
    },

    2:{
        "pergunta":0,
        "frase":"Él _______ bién",
        "verbo":"Cantar",
        "resposta certa":"Canta"
    }
}
TIPOS_PERGUNTAS = ["Completa la oración con la conjugación correcta del verbo"]

questoesVistas = []
q = 1

@app.route('/')
def home():
    return render_template("telaquestao.html", enunciado="Padrão", itens=["Letra A", "Letra B", "Letra C", "Letra D"], resultado = "Nada", estado = ["", "", "", ""])

def novaQuestao():
    global q
    global opcoes
    global escolhidas
    global estado

    tentativas = 0
    while q in questoesVistas and tentativas < 30:
        q = random.randint(1, len(DADOS_QUESTÕES.keys()))
        tentativas += 1
    questoesVistas.append(q)

    pergunta, frase, verbo, respCerta = DADOS_QUESTÕES[q].values()

    opcoes = conjugador.conjugacoes(DADOS_QUESTÕES[q]['verbo'])
    escolhidas = []
    print(opcoes)
    ic = opcoes.index(respCerta)
    while len(escolhidas) < 4:
        r = random.randint(0, len(opcoes)-1)
        if r not in escolhidas:
            escolhidas.append(r)
        if len(escolhidas) == 4 and ic not in escolhidas:
            escolhidas[random.randint(0, 3)] = ic
    
    estado = []
    for i in "ABCD":
        if i == "ABCD"[escolhidas.index(ic)]:
            estado.append("certa")
        else:
            estado.append("")

    print(f"{opcoes.index(respCerta)} in {escolhidas} - {opcoes.index(respCerta) in escolhidas}")
    print(estado)
    return pergunta, frase, verbo, respCerta

@app.route('/questao', methods =["GET", "POST"])
def loop():
    global q
    global opcoes
    global escolhidas
    global estado

    if request.method == "GET":
        pergunta, frase, verbo, respCerta = novaQuestao()
        return render_template("telaquestao.html", enunciado=f"{TIPOS_PERGUNTAS[pergunta]} {verbo}: {frase}", itens=[opcoes[escolhidas[0]], opcoes[escolhidas[1]], opcoes[escolhidas[2]], opcoes[escolhidas[3]]], estado=estado)

    if request.method == "POST":
        alts = "ABCD"
        alternativa = list(request.form.keys())[0]
        pergunta, frase, verbo, respCerta = novaQuestao()
        return render_template("telaquestao.html", enunciado=f"{TIPOS_PERGUNTAS[pergunta]} {verbo}: {frase}", itens=[opcoes[escolhidas[0]], opcoes[escolhidas[1]], opcoes[escolhidas[2]], opcoes[escolhidas[3]]], estado=estado)

if __name__ == '__main__':
    app.run(debug=True)
    
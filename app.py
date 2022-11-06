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
        "frase":"Tú _______ bién",
        "verbo":"Cantar",
        "resposta certa":"Cantas"
    },

    3:{
        "pergunta":0,
        "frase":"El maestro _______ a los estudiantes",
        "verbo":"Educar",
        "resposta certa":"Educa"
    },

    4:{
        "pergunta":0,
        "frase":"Mi amigo siempre _____ en los juegos",
        "verbo":"Ganar",
        "resposta certa":"Gana"
    },
    5:{
        "pergunta":0,
        "frase":"La activista ______ la causa",
        "verbo":"Apoyar",
        "resposta certa":"Apoya"
    }

}
TIPOS_PERGUNTAS = ["Completa la oración con la conjugación correcta del verbo"]

acertos = 0
q = 1

@app.route('/')
def home():
    return render_template("telaquestao.html", enunciado="Padrão", itens=["Letra A", "Letra B", "Letra C", "Letra D"], resultado = "Nada", estado = ["", "", "", ""])

questoesVistas = []
respCerta = ""
estado = "    "

def novaQuestao():
    global q
    global opcoes
    global escolhidas
    global estado
    global questoesVistas

    while q in questoesVistas:
        q = random.randint(1, len(DADOS_QUESTÕES.keys()))
        if len(questoesVistas) == len(DADOS_QUESTÕES.keys()):
            questoesVistas = []
    questoesVistas.append(q)

    pergunta, frase, verbo, respCerta = DADOS_QUESTÕES[q].values()

    opcoes = conjugador.conjugacoes(DADOS_QUESTÕES[q]['verbo'])
    escolhidas = []
    ic = opcoes.index(respCerta)
    while len(escolhidas) < 4:
        r = random.randint(0, len(opcoes)-1)
        if r not in escolhidas:
            escolhidas.append(r)
        if len(escolhidas) == 4 and ic not in escolhidas:
            escolhidas[random.randint(0, 3)] = ic
    
    estado = []
    altCorreta = "ABCD"[escolhidas.index(ic)]
    for i in "ABCD":
        if i == altCorreta:
            estado.append("certa")
        else:
            estado.append("")

    print(questoesVistas)
    print(respCerta)

    return pergunta, frase, verbo, altCorreta

@app.route('/questao', methods =["GET", "POST"])
def loop():
    global q
    global opcoes
    global escolhidas
    global estado
    global acertos
    global respCerta

    if request.method == "GET":
        pergunta, frase, verbo, respCerta = novaQuestao()
        return render_template("telaquestao.html", enunciado=f"{TIPOS_PERGUNTAS[pergunta]} {verbo}: {frase}", itens=[opcoes[escolhidas[0]], opcoes[escolhidas[1]], opcoes[escolhidas[2]], opcoes[escolhidas[3]]], estado=estado, acertos=acertos)

    if request.method == "POST":
        alts = "ABCD"
        alternativa = list(request.form.keys())[0]

        if alternativa == respCerta:
            acertos += 1

        pergunta, frase, verbo, respCerta = novaQuestao()

        return render_template("telaquestao.html", enunciado=f"{TIPOS_PERGUNTAS[pergunta]} {verbo}: {frase}", itens=[opcoes[escolhidas[0]], opcoes[escolhidas[1]], opcoes[escolhidas[2]], opcoes[escolhidas[3]]], estado=estado, acertos=acertos)

if __name__ == '__main__':
    app.run(debug=True)
    
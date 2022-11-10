from flask import Flask, render_template, request, redirect
import random
import conjugador

app = Flask(__name__)
DADOS_QUESTÕES = { #Definição das perguntas para serem escolhidas
    1:{
        "pergunta":0, #Tipo do enunciado
        "frase":"Yo ______ mucho.",
        "verbo":"Hablar",
        "resposta certa":"Hablo"
    },

    2:{
        "pergunta":0,
        "frase":"Tú _______ bién.",
        "verbo":"Cantar",
        "resposta certa":"Cantas"
    },

    3:{
        "pergunta":0,
        "frase":"El maestro _______ a los estudiantes.",
        "verbo":"Educar",
        "resposta certa":"Educa"
    },

    4:{
        "pergunta":0,
        "frase":"Mi amigo siempre _____ en los juegos.",
        "verbo":"Ganar",
        "resposta certa":"Gana"
    },
    5:{
        "pergunta":0,
        "frase":"La activista ______ la causa.",
        "verbo":"Apoyar",
        "resposta certa":"Apoya"
    },
    6:{
        "pergunta":0,
        "frase":"Los alumnos __________ español.",
        "verbo":"Estudiar",
        "resposta certa": "Estudian"
    },
    7:{
        "pergunta":0,
        "frase":"María _________ bien el contenido.",
        "verbo":"Presentar",
        "resposta certa": "Presenta"
    },
    8:{
        "pergunta":0,
        "frase":"Me ______ el jugo de piña.",
        "verbo":"Gustar",
        "resposta certa": "Gusta"
    },
    9:{
        "pergunta":0,
        "frase":"¿Tu _________ con su madre todos los días?",
        "verbo":"Caminar",
        "resposta certa": "Caminas"
    },
    10:{
        "pergunta":0,   
        "frase":"Mis amigos _________ musica.",
        "verbo":"Escuchar",
        "resposta certa": "Escuchan"
    },
    11:{
        "pergunta":0,   
        "frase":"Siempre _____ al cielo por la noche porque la luna es hermosa.",
        "verbo":"Mirar",
        "resposta certa": "Miro"
    },
    12:{
        "pergunta":0,   
        "frase":"Ellos ______ a sus amigos cada vez que tienen una fiesta.",
        "verbo":"Invitar",
        "resposta certa": "Invitan"
    },
    13:{
        "pergunta":0,   
        "frase":"Yo ________ de ayuda para terminar la actividad.",
        "verbo":"Necesitar",
        "resposta certa": "Necesito"
    },
    14:{
        "pergunta":0,   
        "frase":"Miguel ______ paisajes muy bonitos.",
        "verbo":"Dibujar",
        "resposta certa": "Dibuja"
    },
    15:{
        "pergunta":0,   
        "frase":"Cuando ________ el año nuevo, llamo a todos los miembros de mi familia.",
        "verbo":"Celebrar",
        "resposta certa": "Celebro"
    }
}
""",
    8:{ #Tipo de questão para ser implementado futuramente
        "pergunta":1,
        "frases": ["Los hermanos se aman.",
        "Todas las vidas importas.",
        "Ellos tomaron una   decisión.",
        "Mi abuela cocino bién."
        ],
        "frase certa": "Los hermanos se aman."
    }"""
TIPOS_PERGUNTAS = ["Completa la oración con la conjugación correcta del verbo", 
"Marca la oración en la que la conjugación del verbo en el presente del indicativo es correcta"]

acertos = 0
q = 1
questoesVistas = []
respCerta = ""
estado = "    "
qatual = 0

def novaQuestao():
    global q, qatual, opcoes, escolhidas, estado
    global questoesVistas

    qatual += 1

    while q in questoesVistas: #Criar uma nova questão ainda não vista
        q = random.randint(1, len(DADOS_QUESTÕES.keys()))
        if len(questoesVistas) == len(DADOS_QUESTÕES.keys()):
            questoesVistas = [] #Resetar para começar a repetir questões
            ###Adicionar tela final
    questoesVistas.append(q)

    pergunta, frase, verbo, respCerta = DADOS_QUESTÕES[q].values()

    opcoes = conjugador.conjugacoes(DADOS_QUESTÕES[q]['verbo']) #Gerar as opções de conjugação
    escolhidas = []
    ic = opcoes.index(respCerta)
    while len(escolhidas) < 4: #Gerar itens aleatórios de acordo com as conjugações do verbo
        r = random.randint(0, len(opcoes)-1)
        if r not in escolhidas:
            escolhidas.append(r)
        if len(escolhidas) == 4 and ic not in escolhidas: #Caso a opção correta não tenha sido gerada, substituir um dos itens por ela
            escolhidas[random.randint(0, 3)] = ic
    
    estado = []
    altCorreta = "ABCD"[escolhidas.index(ic)]
    for i in "ABCD":
        if i == altCorreta: #Atualizar estado para fins do css
            estado.append("certa")
        else:
            estado.append("")

    return pergunta, frase, verbo, altCorreta

#Roteamento
@app.route('/')
def home():
    return redirect('/inicio') #Redirecionar a página vazia para o início

@app.route('/inicio', methods =["GET", "POST"])
def inicio():
    return render_template("inicio.html")

@app.route('/explicacao', methods =["GET", "POST"])
def explicacao():
    global qatual, acertos, questoesVistas
    #Resetar valores na página de início
    acertos = 0
    qatual = 0
    questoesVistas = []
    return render_template("explicacao.html")

@app.route('/questao', methods =["GET", "POST"])
def loop():
    global q, qatual, opcoes, escolhidas
    global estado, acertos, respCerta
    global pergunta, frase, verbo, respCerta

    passar = False #Variável para impedir a geração de novas questões com o refresh
    if request.method == "GET":
        passar = True
        if qatual == 0:
            pergunta, frase, verbo, respCerta = novaQuestao()

    if request.method == "POST" or passar: #Quando uma alternativa é escolhida
        if passar:
            alternativa = ""
        else:
            alternativa = list(request.form.keys())[0] #Identificar a alternativa marcada
            if alternativa == respCerta: #Verificar se está correta
                acertos += 1

            pergunta, frase, verbo, respCerta = novaQuestao() #Gerar nova questão

        return render_template("telaquestao.html", 
        qatual=qatual, 
        enunciado=f"{TIPOS_PERGUNTAS[pergunta]} {verbo}: {frase}", 
        itens=[opcoes[escolhidas[0]], opcoes[escolhidas[1]], 
        opcoes[escolhidas[2]], opcoes[escolhidas[3]]], 
        estado=estado, 
        acertos=acertos)

if __name__ == '__main__':
    app.run(debug=True)
    
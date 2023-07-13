from flask import Flask, render_template, request, redirect, url_for
import random
import json
import conjugador

#Importar dados de um arquivo .json
with open("dados.json", "r", encoding='utf-8') as a:
    DADOS_QUESTÕES = json.load(a)

TIPOS_PERGUNTAS = ["Completa la oración con la conjugación correcta del verbo", 
"¿Es correcta la conjugación del verbo en el presente del indicativo en esta oración?"]

app = Flask(__name__)
respCerta = ""

def reset():
    global questoesVistas, qAtual, acertos, dataQVistas
    questoesVistas = []
    qAtual = 0
    acertos = 0
    dataQVistas = [0, 0, 0, 0]

def novaQuestao(ovrd=-1):
    global questoesVistas, qAtual, dataQVistas, tipoQuestao
    if ovrd == -1:
        qAtual += 1

        q = 0
        while True: #Criar uma nova questão ainda não vista
            q = random.randint(1, len(DADOS_QUESTÕES))
            if [q, False] not in questoesVistas and [q, True] not in questoesVistas:
                break
    else:
        q = ovrd
        
    if [q, False] not in questoesVistas and [q, True] not in questoesVistas:
        questoesVistas.append([q, False])
    tipoQuestao = DADOS_QUESTÕES[q-1]["pergunta"]

    if tipoQuestao == 0:
        if ovrd == -1:
            dataQVistas[1] += 1
        pergunta, frase, verbo, respCerta = DADOS_QUESTÕES[q-1].values()

        opcoes = conjugador.conjugacoes(DADOS_QUESTÕES[q-1]['verbo']) #Gerar as opções de conjugação
        escolhidas = []
        ic = opcoes.index(respCerta)
        while len(escolhidas) < 4: #Gerar itens aleatórios de acordo com as conjugações do verbo
            r = random.randint(0, len(opcoes)-1)
            if r not in escolhidas:
                escolhidas.append(r)
            if len(escolhidas) == 4 and ic not in escolhidas: #Caso a opção correta não tenha sido gerada, substituir um dos itens por ela
                escolhidas[random.randint(0, 3)] = ic
        
        estado = []
        respCerta = "ABCD"[escolhidas.index(ic)]
        for i in "ABCD":
            if i == respCerta: #Atualizar estado para fins do css
                estado.append("certa")
            else:
                estado.append("")
        
        alts = []
        for i in escolhidas:
            alts.append(opcoes[i])
        return [pergunta, frase, verbo, alts, respCerta, estado]
    else:
        if ovrd == -1:
            dataQVistas[3] += 1
        alts = ["Verdadero", "Falso"]

        pergunta, frase, respCerta = DADOS_QUESTÕES[q-1].values()
        estado = []
        for i in alts:
            if i == respCerta:
                estado.append("certa")
            else:
                estado.append("")
        return [pergunta, frase, respCerta, estado]

def processarQuestao(questao):
    global respCerta, dataQVistas, qAtual
    acertos = dataQVistas[0] + dataQVistas[2]
    vistas = dataQVistas[1] + dataQVistas[3]
    print(dataQVistas)
    #Gerenciar os botões de ir e voltar estarem habilitados
    dis = ["", ""]
    if qAtual == 1:
        dis[0] = 'disabled'
    if qAtual >= vistas:
        dis[1] = 'disabled'
    
    #Receber os dados e renderizar a página correta de acordo com o tipo da questão
    if questao[0] == 0:
        pergunta, frase, verbo, escolhidas, respCerta, estado = questao
        return render_template("telaquestao.html", 
            qAtual=qAtual, 
            enunciado=f"{TIPOS_PERGUNTAS[pergunta]} {verbo}: {frase}", 
            itens=escolhidas,
            estado=estado, 
            acertos=acertos, 
            roteador=roteador,
            disabled=dis
            )
    else:
        pergunta, frase, respCerta, estado = questao
        return render_template("telaquestao2.html", 
            qAtual=qAtual, 
            enunciado=f'{TIPOS_PERGUNTAS[pergunta]}',
            frase= frase,
            estado=estado,
            acertos=acertos, 
            roteador=roteador,
            disabled=dis
            )

def roteador(tela):
    return url_for(f'{tela}')

@app.route('/')
def home():
    return redirect('/inicio') #Redirecionar a página vazia para o início

@app.route('/inicio', methods =["GET", "POST"])
def inicio():
    reset()
    return render_template("inicio.html", roteador=roteador)

@app.route('/explicacao', methods =["GET", "POST"])
def explicacao():
    return render_template("explicacao.html", roteador=roteador)

@app.route('/resultados', methods =["GET", "POST"])
def resultados():
    global dataQVistas
    return render_template("resultados.html", roteador=roteador, completar=dataQVistas[0:2], verdFalso=dataQVistas[2:4])

@app.route('/questao', methods =["GET", "POST"])
def questao():
    global tipoQuestao, dataQVistas, qAtual

    if 'questoesVistas' not in globals():
        reset()

    if len(questoesVistas) == 15:
        return redirect('resultados')
    
    if request.method == "GET":
        if len(questoesVistas) == 0:
            questao = novaQuestao()
            return processarQuestao(questao)
    
    if request.method == "POST":
        formRes = []
        if request.form.keys():
            formRes = list(request.form.keys())[0]
        
        if formRes in ["vquestao", "aquestao"]: #Se não for navegando pelas questões
            if formRes == "vquestao":
                if qAtual > 1:
                    qAtual -= 1
            else:
                if qAtual < len(questoesVistas):
                    qAtual += 1
            questao = novaQuestao(ovrd=questoesVistas[qAtual-1][0])
        else:
            if formRes != "botaoproximo" or qAtual == 0:
                if formRes == respCerta:
                    dataQVistas[tipoQuestao*2] += 1
                questao = novaQuestao()

    if 'questao' not in locals():
        qAtual = len(questoesVistas)
        questao = novaQuestao(ovrd=questoesVistas[-1][0])
    return processarQuestao(questao)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
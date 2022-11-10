def conjugar(palavra, pessoa, numero):
    TERMINAÇÕES = ["o", "as", "a", "amos", "áis", "an"]
    id = pessoa + int(numero == "plural")*3
    ind = 0
    resultado = "NÃO ENCONTRADO"
    for t in TERMINAÇÕES:
        if id == ind:
            resultado = palavra.replace("ar", t)
            break
        ind += 1
    return resultado

def conjugacoes(palavra):
    resultado = []
    ind = 0
    for p in ["Yo", "Tu", "Él / Ella / Usted"]:
        resultado.append(conjugar(palavra, ind, 'singular'))
        ind += 1
    ind = 0
    for p in ["Nosotros/as", "Vosostros/as", "Ellos / Ellas/ Ustedes"]:
        resultado.append((conjugar(palavra, ind, 'plural')))
        ind += 1
    return resultado
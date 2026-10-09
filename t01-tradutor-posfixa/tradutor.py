import sys
entrada = "" # Linha que está sendo analisada.
pos = 0 # Posição do próximo caractere a ser lido em entrada.
lookahead = ("fim", "") # Token sendo examinado no momento.
saida = [] # Tokens da tradução pós-fixada.

def proximo():
    """
        - Lê e devolve o próximo token de entrada, a partir da posição pos.
        - O token é uma tupla (tipo, valor). Números de vários dígitos viram 
        um único token ("num", texto), e espaços e tabulações são ignorados.
    """

    global pos

    # Pular espaços e tabulações.
    while pos < len(entrada) and entrada[pos] in " \t":
        pos += 1

    # Fim da linha.
    if pos == len(entrada):
        return ("fim", "")

    c = entrada[pos]

    # Número: junta todos os dígitos consecutivos para formar um número.
    if c.isdigit():
        inicio = pos
        while pos < len(entrada) and entrada[pos].isdigit():
            pos += 1
        return ("num", entrada[inicio:pos])

    # Operador ou parêntese: o próprio símbolo é o tipo do token.
    if c in "+-*/()":
        pos += 1
        return (c, c)

    # Qualquer outro caractere é inválido.
    raise SyntaxError(f"Caractere inválido '{c}' na posição {pos}.")

def casar(tipo):
    """
        - Match: Confere se o token atual é do tipo esperado e avança para o 
        próximo.
    """

    global lookahead
    if lookahead[0] == tipo:
        lookahead = proximo()
    else:
        raise SyntaxError(
            f"Esperado '{tipo}', encontrado '{lookahead[1] or 'fim'}'"
        )

def emitir(valor):
    """
        - Ação semântica: acrescenta um token à saída pós-fixada.
    """

    saida.append(valor)

def expr():
    # expr -> term expr'.
    term()
    expr_linha()

def expr_linha():
    # expr' -> + term {emitir('+')} expr'
    if lookahead[0] == "+":
        casar("+")
        term()
        emitir("+")
        expr_linha()

    # expr' -> - term {emitir('-')} expr'
    elif lookahead[0] == "-":
        casar("-")
        term()
        emitir("-")
        expr_linha()

    # expr' -> vazio : não consome nada.

def term():
    # term -> fact term'
    fact()
    term_linha()

def term_linha():
    # term' -> * fact {emitir('*')} term'
    if lookahead[0] == "*":
        casar("*")
        fact()
        emitir("*")
        term_linha()

    # term' -> / fact {emitir('/')} term'
    elif lookahead[0] == "/":
        casar("/")
        fact()
        emitir("/")
        term_linha()
    # term' -> Vazio : não consome nada.

def fact():
    # fact -> ( expr )
    if lookahead[0] == "(":
        casar("(")
        expr()
        casar(")")

    # fact -> num {emitir(valor do número)}
    elif lookahead[0] == "num":
        # Emite antes de casar, porque casar substitui o lookahead.
        emitir(lookahead[1])
        casar("num")
    else:
        raise SyntaxError(
            f"Esperado número ou '(', encontrado '{lookahead[1] or 'fim'}'."
        )

def main():
    global entrada, pos, lookahead, saida

    if len(sys.argv) > 1:
        fonte = open(sys.argv[1], encoding="utf-8")
    else:
        fonte = sys.stdin

    for linha in fonte:
        linha = linha.strip()
        if not linha:
            continue

        entrada = linha
        pos = 0
        saida = []

        # Primeiro Token.
        lookahead = proximo()

        # Analisa a expressão inteira.
        expr()

        # Se sobrou entrada, a expressão terminou antes da hora (ex.: "9 5").
        if lookahead[0] != "fim":
            raise SyntaxError(f"Símbolo inesperado '{lookahead[1]}'.")

        print(" ".join(saida))

if __name__ == "__main__":
    main()
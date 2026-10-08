import sys
entrada = ""   # Linha que está sendo analisada.
pos = 0        # Posição do próximo caractere a ser lido em entrada.

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
    raise SyntaxError(f"caractere inválido '{c}' na posição {pos}.")

def main():
    global entrada, pos

    if len(sys.argv) > 1:
        fonte = open(sys.argv[1], encoding="utf-8")
    else:
        fonte = sys.stdin

    for linha in fonte:
        # Remove espaços, tabulações e o \n das pontas da linha.
        linha = linha.strip()
        # Linha em branco, pula.
        if not linha:
            continue

        # Prepara o estado para analisar esta linha.
        entrada = linha
        pos = 0

        # Teste provisório: imprime todos os tokens ('tipo','valor') da linha.
        token = proximo()
        while token[0] != "fim":
            print(token)
            token = proximo()
        print()  # Linha vazia para separar uma expressão da outra

    if fonte is not sys.stdin:
        fonte.close()

if __name__ == "__main__":
    main()
import sys

def main():
    if len(sys.argv) > 1:
        fonte = open(sys.argv[1], encoding="utf-8")
    else:
        fonte = sys.stdin

    for linha in fonte:
        # Tira os espaços em branco das extremidades.
        linha = linha.strip()
        # Linha em branco, pula.
        if not linha:          
            continue
        print(linha)           # por enquanto só imprime; depois vira a tradução

    if fonte is not sys.stdin:
        fonte.close()

if __name__ == "__main__":
    main()
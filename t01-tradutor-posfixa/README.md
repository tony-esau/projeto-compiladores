# Trabalho 01: Tradutor Infixa para Pós-fixa

Tradutor dirigido por sintaxe que converte expressões aritméticas da notação infixa para a notação pós-fixada, implementado como um **analisador descendente recursivo preditivo** escrito à mão em Python.

Trabalho 01 (AP1) da disciplina Compiladores. Estende o tradutor básico com precedência, parênteses e números de vários dígitos, e serve de base para a integração do analisador léxico.

## Exemplo

```
Entrada:  (9-5)*2
Saída:    9 5 - 2 *

Entrada:  10 + 20 * 3
Saída:    10 20 3 * +
```

## Funcionalidades

- Operadores `+`, `-`, `*` e `/`, com precedência de `*` e `/` sobre `+` e `-`;
- Associatividade à esquerda nos quatro operadores;
- Parênteses alterando a ordem de avaliação;
- Números inteiros com vários dígitos;
- Espaços e tabulações ignorados na entrada;
- Uma expressão por linha, com linhas em branco ignoradas.

## Gramática

Gramática original, com precedência e recursão à esquerda:

```
expr   → expr + term | expr - term | term
term   → term * fact | term / fact | fact
fact   → ( expr ) | num
num    → num digit | digit
digit  → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

Gramática completa após a eliminação da recursão à esquerda, usada pelo analisador:

```
expr   → term expr'
expr'  → + term expr' | - term expr' | ε
term   → fact term'
term'  → * fact term' | / fact term' | ε
fact   → ( expr ) | num
num    → digit num'
num'   → digit num' | ε
digit  → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

Os não-terminais `expr`, `expr'`, `term`, `term'` e `fact` correspondem, cada um, a um procedimento no código. As produções de `num`, `num'` e `digit` são reconhecidas pelo procedimento `proximo`, que agrupa dígitos consecutivos e entrega ao analisador um único token `num`.

## Requisitos

- Python 3.10 ou superior
- Apenas a biblioteca padrão (sem PLY ou geradores de analisadores)

## Como executar

Passando o arquivo de entrada como argumento:

```bash
python3 tradutor.py entradas.txt
```

Ou pela entrada padrão:

```bash
python3 tradutor.py < entradas.txt
```

Para cada linha da entrada, o programa imprime exatamente uma linha com a expressão correspondente em notação pós-fixada, com os tokens separados por um espaço.

## Testes

Os casos ficam na pasta `testes/`, sempre em pares: um arquivo com as entradas (uma expressão por linha) e outro com as saídas esperadas, na mesma ordem.

| Arquivo | Conteúdo |
|---|---|
| `testes/entrada_publica.txt` | os 7 casos públicos do enunciado |
| `testes/esperado_publica.txt` | saídas esperadas dos casos públicos |
| `testes/entrada_propria.txt` | casos próprios (associatividade, parênteses aninhados, vários dígitos, espaços, tabulação e linha em branco) |
| `testes/esperado_propria.txt` | saídas esperadas dos casos próprios |

A linha em branco em `entrada_propria.txt` é proposital: ela deve ser ignorada e não gera linha na saída, por isso o arquivo de saídas tem uma linha a menos.

O script `test.py` executa o tradutor sobre cada arquivo de entrada e compara, linha a linha, com o arquivo de saídas correspondente, mostrando os casos que falharam:

```bash
python3 test.py
```

Para conferir um arquivo isolado sem o script:

```bash
python3 tradutor.py testes/entrada_publica.txt | diff - testes/esperado_publica.txt
```

Se o `diff` não imprimir nada, todas as saídas estão corretas.

O arquivo `testes.txt` exigido na entrega é montado a partir de `testes/entrada_propria.txt`.

## Estrutura da pasta

```
t01-tradutor-posfixa/
├── tradutor.py      # implementação do tradutor
├── test.py          # executa os casos de teste e compara as saídas
├── relatorio.pdf    # relatório (Parte A, decisões de implementação e limitações)
├── testes/          # pares de arquivos de entrada e saída esperada
└── README.md
```

## Andamento

- [ ] Parte A: gramática sem recursão à esquerda, ações semânticas, FIRST e árvores
- [ ] Item 5: tradutor base com `match` e `proximo`
- [ ] Item 6: precedência e parênteses
- [ ] Item 7: números com vários dígitos e espaços
- [ ] Relatório e `testes.txt`
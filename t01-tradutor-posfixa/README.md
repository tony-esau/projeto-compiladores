# Trabalho 01: Tradutor Infixa para Pós-fixa

Tradutor dirigido por sintaxe que converte expressões aritméticas da notação infixa para a notação pós-fixada, implementado como um **analisador descendente recursivo preditivo** escrito à mão em Python.

Trabalho 01 da disciplina Compiladores. Estende o tradutor básico com precedência, parênteses e números de vários dígitos, e serve de base para a integração do analisador léxico.

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
- Uma expressão por linha, com linhas em branco ignoradas;
- Linhas inválidas geram uma mensagem `erro: ...` no lugar da tradução, sem interromper as demais.

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
- O tradutor usa apenas a biblioteca padrão (sem PLY ou geradores de analisadores)
- Para rodar os testes automatizados: [pytest](https://docs.pytest.org/) (`pip install pytest`)

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

### Testes automatizados com pytest

O arquivo `test_tradutor.py` transforma cada linha dos pares `entrada_<nome>.txt` e `esperado_<nome>.txt` em um caso de teste separado (com `pytest.mark.parametrize`) e executa o tradutor como um programa à parte, por meio de uma fixture. Novos pares colocados na pasta `testes/` entram nos testes automaticamente.

```bash
python3 -m pytest -v
```

Cada caso aparece com o nome do arquivo e o número da linha (por exemplo, `publica.txt:2`), e os que falharem mostram a saída esperada e a obtida.

### Sem pytest

Para conferir um arquivo isolado usando só o terminal:

```bash
python3 tradutor.py testes/entrada_publica.txt | diff - testes/esperado_publica.txt
```

Se o `diff` não imprimir nada, todas as saídas estão corretas.

O arquivo `testes.txt` exigido na entrega é montado a partir de `testes/entrada_propria.txt`.

## Estrutura da pasta

```
t01-tradutor-posfixa/
├── tradutor.py      # implementação do tradutor
├── test_tradutor.py # testes automatizados (pytest)
├── relatorio.pdf    # relatório (Parte A, decisões de implementação e limitações)
├── testes/          # pares de arquivos de entrada e saída esperada
└── README.md
```

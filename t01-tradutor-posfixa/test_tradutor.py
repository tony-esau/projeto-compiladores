import subprocess
import sys
from pathlib import Path

import pytest

PASTA = Path(__file__).resolve().parent
TESTES = PASTA / "testes"

def casos():
    """Gera um caso de teste para cada linha dos pares entrada/esperado."""
    for arq_entrada in sorted(TESTES.glob("entrada_*.txt")):
        nome = arq_entrada.name.removeprefix("entrada_")
        arq_esperado = TESTES / f"esperado_{nome}"
        entradas = [l for l in arq_entrada.read_text(encoding="utf-8")
                    .splitlines() if l.strip()]
        esperadas = arq_esperado.read_text(encoding="utf-8").splitlines()
        for i, (entrada, esperado) in enumerate(zip(entradas, esperadas), 
        start=1):
            yield pytest.param(entrada, esperado, id=f"{nome}:{i}")

@pytest.fixture
def traduzir():
    """Fixture: devolve uma função que roda o tradutor com uma expressão."""
    def _traduzir(expressao):
        resultado = subprocess.run(
            [sys.executable, str(PASTA / "tradutor.py")],
            input=expressao + "\n", 
            capture_output=True, 
            text=True, 
            encoding="utf-8",
        )
        return resultado.stdout.strip()
    return _traduzir

@pytest.mark.parametrize("entrada, esperado", list(casos()))
def test_traducao(traduzir, entrada, esperado):
    assert traduzir(entrada) == esperado
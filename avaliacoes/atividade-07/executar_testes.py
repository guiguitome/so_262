#!/usr/bin/env python3
"""Executa os cinco testes da atividade 7 e salva suas saídas reais em UTF-8."""

import argparse
import copy
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True
from bankers_algorithm import BankersAlgorithm


ALUNO = "Guilherme Tomé Frazão"
PASTA = Path(__file__).resolve().parent
SEQUENCIA = ["P1", "P3", "P0", "P2", "P4"]
TESTES = {
    1: ("Estado inicial seguro", "teste_01_estado_seguro"),
    2: ("Requisição segura de P1", "teste_02_requisicao_segura"),
    3: ("Recursos indisponíveis para P4", "teste_03_recursos_indisponiveis"),
    4: ("Estado inseguro e rollback", "teste_04_estado_inseguro"),
    5: ("Requisição acima da necessidade", "teste_05_acima_da_necessidade"),
}


def criar_banqueiro():
    return BankersAlgorithm(
        ["P0", "P1", "P2", "P3", "P4"],
        [10, 5, 7],
        [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
        [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    )


def estado(banqueiro):
    return copy.deepcopy((banqueiro.available, banqueiro.allocation, banqueiro.need))


def conferir(condicao, mensagem):
    if not condicao:
        raise AssertionError(mensagem)


def executar_teste(numero):
    titulo, _ = TESTES[numero]
    banqueiro = criar_banqueiro()
    print(f"Aluno: {ALUNO}")
    print(f"ATIVIDADE 7 | TESTE {numero:02d} - {titulo}")
    print(f"Comando: python -X utf8 executar_testes.py --teste {numero}")
    print("=" * 70)
    print("Recursos totais: [10, 5, 7]")
    print(f"Disponíveis no estado inicial: {banqueiro.available}")

    if numero == 3:
        # Reproduz a ordem da demonstração original: P1 é atendido antes de P4.
        with redirect_stdout(io.StringIO()):
            concedida = banqueiro.request_resources(1, [1, 0, 2])
        conferir(concedida, "A preparação com P1 deveria ser concedida.")
        print("Preparação: P1 recebeu [1, 0, 2] (mesmo cenário do teste 02).")
        print(f"Disponíveis antes do pedido de P4: {banqueiro.available}")

    antes = estado(banqueiro)
    if numero == 1:
        seguro, sequencia = banqueiro.is_safe_state(verbose=True)
        conferir(seguro and sequencia == SEQUENCIA, "Sequência segura inesperada.")
        conferir(estado(banqueiro) == antes, "A verificação alterou o estado real.")
        print("\nConferência: sequência segura encontrada; estado real inalterado.")
    else:
        indice, pedido = {
            2: (1, [1, 0, 2]),
            3: (4, [3, 3, 0]),
            4: (4, [3, 3, 0]),
            5: (1, [2, 0, 0]),
        }[numero]
        print(f"Necessidade de P{indice} antes: {banqueiro.need[indice]}")
        concedida = banqueiro.request_resources(indice, pedido)
        conferir(concedida == (numero == 2), "Resultado da requisição inesperado.")
        if numero == 2:
            conferir(banqueiro.available == [2, 3, 0], "Disponíveis incorretos.")
            conferir(banqueiro.allocation[1] == [3, 0, 2], "Alocação de P1 incorreta.")
            conferir(banqueiro.need[1] == [0, 2, 0], "Necessidade de P1 incorreta.")
            conferir(banqueiro.is_safe_state(False) == (True, SEQUENCIA), "Estado inseguro.")
        else:
            conferir(estado(banqueiro) == antes, "A requisição negada alterou o estado.")
        print(f"\nRetorno da requisição: {concedida}")
        print(f"Disponíveis após o teste: {banqueiro.available}")
        print(f"Alocação de P{indice} após o teste: {banqueiro.allocation[indice]}")
        print(f"Necessidade de P{indice} após o teste: {banqueiro.need[indice]}")
        if numero == 2:
            print("Conferência: alocação concedida; estado resultante seguro.")
        elif numero == 4:
            print("Conferência: available, allocation e need restaurados pelo rollback.")
        else:
            print("Conferência: available, allocation e need permanecem inalterados.")
    print(f"RESULTADO: TESTE {numero:02d} APROVADO")



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teste", type=int, choices=TESTES, help="Executar só um teste.")
    parser.add_argument("--gerar-saidas", action="store_true", help="Salvar os logs em saidas/.")
    args = parser.parse_args()
    if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    for numero in [args.teste] if args.teste is not None else TESTES:
        captura = io.StringIO()
        with redirect_stdout(captura):
            executar_teste(numero)
        texto = captura.getvalue()
        if args.gerar_saidas:
            pasta_saidas = PASTA / "saidas"
            pasta_saidas.mkdir(exist_ok=True)
            (pasta_saidas / f"{TESTES[numero][1]}.txt").write_text(texto, encoding="utf-8")
        print(texto)


if __name__ == "__main__":
    main()

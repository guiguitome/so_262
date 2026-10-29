# Atividade 7

Execute o algoritmo dos Banqueiros definido na aula anterior.

Gere arquivos que evidenciam a execução no GitHub na pasta atividade-07 como definido abaixo:

1) Explicando cada teste proposto e sua saída gerada;
2) Print da execução de cada Teste.
3) Identifique o seu nome nos prints.

## Resolução

**Aluno:** Guilherme Tomé Frazão

- [Algoritmo do Banqueiro](bankers_algorithm.py)
- [Execução dos testes](executar_testes.py)
- [Explicação dos testes e passo a passo](RESOLUCAO.md)
- [Saídas completas da execução](saidas/)
- [Orientações para os prints](prints/README.md)

## Testes executados

| Teste | Cenário | Resultado obtido |
| --- | --- | --- |
| 01 | Verificação do estado inicial | Seguro; sequência P1 → P3 → P0 → P2 → P4 |
| 02 | P1 solicita `[1, 0, 2]` | Concedido; disponíveis `[2, 3, 0]` |
| 03 | Após atender P1, P4 solicita `[3, 3, 0]` | Bloqueado por falta de R0; estado inalterado |
| 04 | No estado inicial, P4 solicita `[3, 3, 0]` | Negado por estado inseguro; rollback confirmado |
| 05 | No estado inicial, P1 solicita `[2, 0, 0]` | Negado por exceder a necessidade de R0 |

Todos os testes passaram nas verificações automáticas. As recusas dos testes 03, 04 e 05 são os resultados esperados.

## Como executar

A partir da raiz do repositório, com Python 3 instalado:

```bash
cd avaliacoes/atividade-07
python -X utf8 bankers_algorithm.py
python -X utf8 executar_testes.py --gerar-saidas
```

Para executar um teste isolado, substitua `1` pelo número desejado, de 1 a 5:

```bash
python -X utf8 executar_testes.py --teste 1
```

## Evidências da entrega

- [x] Executar o algoritmo.
- [x] Explicar cada teste e sua saída.
- [x] Salvar as saídas reais dos cinco testes em arquivos de texto, com o nome do aluno.
- [ ] Adicionar os prints reais da execução dos cinco testes, com o nome do aluno visível.

**Pendência:** as capturas de tela ainda precisam ser adicionadas. Os arquivos `.txt` contêm as saídas da execução e não substituem os prints solicitados no enunciado.

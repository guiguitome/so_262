# Resolução da atividade 7 — Algoritmo do Banqueiro

**Aluno:** Guilherme Tomé Frazão
**Data da execução:** 29/10/2026

## 1. Objetivo

Executar o algoritmo fornecido, analisar as decisões de concessão de recursos e registrar as saídas de cada teste. O algoritmo só confirma uma alocação quando consegue encontrar uma sequência em que todos os processos possam terminar, considerando suas necessidades máximas declaradas.

Foi mantida a lógica de `bankers_algorithm.py`. A demonstração recebeu a identificação do aluno, e o comentário sobre o pedido de P4 foi corrigido para descrever o bloqueio por falta de recursos. O arquivo `executar_testes.py` importa a classe original e executa cinco cenários com verificações automáticas dos resultados.

## 2. Dados iniciais

Os vetores seguem a ordem dos recursos **R0, R1 e R2**. Há cinco processos e recursos totais `E = [10, 5, 7]`.

| Processo | Alocação atual (C) | Máximo declarado (Max) | Necessidade restante (Need) |
| --- | --- | --- | --- |
| P0 | `[0, 1, 0]` | `[7, 5, 3]` | `[7, 4, 3]` |
| P1 | `[2, 0, 0]` | `[3, 2, 2]` | `[1, 2, 2]` |
| P2 | `[3, 0, 2]` | `[9, 0, 2]` | `[6, 0, 0]` |
| P3 | `[2, 1, 1]` | `[2, 2, 2]` | `[0, 1, 1]` |
| P4 | `[0, 0, 2]` | `[4, 3, 3]` | `[4, 3, 1]` |

A necessidade é calculada por `Need = Max - C`. A soma dos recursos alocados é `[7, 2, 5]`, portanto os recursos disponíveis são:

```text
Available = E - soma(C)
Available = [10, 5, 7] - [7, 2, 5] = [3, 3, 2]
```

Cada teste começa com uma nova instância desses dados. No teste 03, a preparação concede o pedido de P1 antes de executar o pedido de P4, reproduzindo a ordem da demonstração original.

## 3. Teste 01 — Estado inicial seguro

**Proposta:** verificar se os recursos iniciais permitem encontrar uma sequência segura.

**Execução:** `python -X utf8 executar_testes.py --teste 1`

O vetor de trabalho `Work` começa em `[3, 3, 2]`. O algoritmo procura um processo cuja necessidade seja menor ou igual a `Work` em todos os recursos. Ao simular seu término, adiciona a alocação desse processo ao vetor de trabalho.

| Passo | Processo escolhido | Necessidade | Work antes | Work após a liberação |
| --- | --- | --- | --- | --- |
| 1 | P1 | `[1, 2, 2]` | `[3, 3, 2]` | `[5, 3, 2]` |
| 2 | P3 | `[0, 1, 1]` | `[5, 3, 2]` | `[7, 4, 3]` |
| 3 | P0 | `[7, 4, 3]` | `[7, 4, 3]` | `[7, 5, 3]` |
| 4 | P2 | `[6, 0, 0]` | `[7, 5, 3]` | `[10, 5, 5]` |
| 5 | P4 | `[4, 3, 1]` | `[10, 5, 5]` | `[10, 5, 7]` |

**Saída obtida:** estado seguro, com sequência `P1 -> P3 -> P0 -> P2 -> P4`. A função retorna `(True, sequência)`. A verificação também confirmou que essa simulação não altera os dados reais de alocação, necessidade e disponibilidade.

O vetor `Work` ao final contém todos os recursos, mas `Available` real continua em `[3, 3, 2]`: a verificação apenas simula os términos.

[Saída completa do teste 01](saidas/teste_01_estado_seguro.txt)

## 4. Teste 02 — Requisição segura de P1

**Proposta:** solicitar `[1, 0, 2]` para P1 e verificar a concessão.

**Execução:** `python -X utf8 executar_testes.py --teste 2`

1. O pedido respeita a necessidade de P1: `[1, 0, 2] <= [1, 2, 2]`.
2. Os recursos estão disponíveis: `[1, 0, 2] <= [3, 3, 2]`.
3. A alocação provisória deixa `Available = [2, 3, 0]`, `Allocation[P1] = [3, 0, 2]` e `Need[P1] = [0, 2, 0]`.
4. A verificação encontra a sequência `P1 -> P3 -> P0 -> P2 -> P4`.
5. O pedido é confirmado porque o estado resultante é seguro.

**Saída obtida:** `REQUISIÇÃO CONCEDIDA A P1!`, retorno `True`. As verificações automáticas confirmaram os três vetores atualizados e a sequência segura.

[Saída completa do teste 02](saidas/teste_02_requisicao_segura.txt)

## 5. Teste 03 — Pedido bloqueado por recursos indisponíveis

**Proposta:** depois de conceder `[1, 0, 2]` a P1, solicitar `[3, 3, 0]` para P4, como na demonstração original.

**Execução:** `python -X utf8 executar_testes.py --teste 3`

Após atender P1, há `[2, 3, 0]` recursos disponíveis. O pedido de P4 respeita sua necessidade `[4, 3, 1]`, mas pede **3 unidades de R0 quando só há 2 disponíveis**.

**Saída obtida:** `PROCESSO BLOQUEADO: Recursos insuficientes disponíveis no momento.`, retorno `False`.

Não ocorre alocação provisória nem verificação de segurança desse pedido. P4 deve aguardar. Os vetores permanecem em `Available = [2, 3, 0]`, `Allocation[P4] = [0, 0, 2]` e `Need[P4] = [4, 3, 1]`. A comparação das matrizes completas confirmou que o estado não foi alterado.

Neste simulador, a mensagem de bloqueio representa a recusa do pedido naquele momento; o programa não cria uma fila de processos bloqueados.

[Saída completa do teste 03](saidas/teste_03_recursos_indisponiveis.txt)

## 6. Teste 04 — Estado inseguro e rollback

**Proposta:** solicitar `[3, 3, 0]` para P4 diretamente no estado inicial, antes de qualquer concessão a P1. Esse cenário exercita a verificação de segurança e a reversão da alocação.

**Execução:** `python -X utf8 executar_testes.py --teste 4`

1. O pedido respeita a necessidade de P4 `[4, 3, 1]` e cabe na disponibilidade inicial `[3, 3, 2]`.
2. A alocação provisória deixa `Available = [0, 0, 2]`, `Allocation[P4] = [3, 3, 2]` e `Need[P4] = [1, 0, 1]`.
3. Nenhum processo tem sua necessidade restante satisfeita por `[0, 0, 2]`. P3 ainda precisa de R1; P0, P1, P2 e P4 ainda precisam de R0.
4. A verificação retorna estado inseguro.
5. O algoritmo desfaz a alocação provisória, restaurando todos os vetores e matrizes ao estado anterior.

**Saída obtida:** `O SISTEMA ENCONTRA-SE EM UM ESTADO INSEGURO!`, seguida de `REQUISIÇÃO NEGADA A P4!` e da confirmação de rollback. O pedido retorna `False`.

Após a reversão, `Available = [3, 3, 2]`, `Allocation[P4] = [0, 0, 2]` e `Need[P4] = [4, 3, 1]`. A comparação de `available`, `allocation` e `need` completos confirmou a restauração.

Um estado inseguro indica que não há garantia de conclusão de todos os processos sob suas necessidades máximas declaradas. Isso não demonstra, por si só, que um deadlock já ocorreu. A concessão é recusada para evitar esse risco.

[Saída completa do teste 04](saidas/teste_04_estado_inseguro.txt)

## 7. Teste 05 — Pedido acima da necessidade declarada

**Proposta:** solicitar `[2, 0, 0]` para P1 no estado inicial.

**Execução:** `python -X utf8 executar_testes.py --teste 5`

P1 já possui `[2, 0, 0]` e declarou máximo `[3, 2, 2]`. Sua necessidade restante é `[1, 2, 2]`. Pedir mais 2 unidades de R0 excede a necessidade restante de 1 unidade.

**Saída obtida:** `REQUISIÇÃO NEGADA: P1 solicitou mais do que sua necessidade máxima declarada.`, retorno `False`.

A recusa ocorre na primeira validação, mesmo havendo recursos disponíveis. Não há alocação provisória. Os vetores e matrizes completos permanecem inalterados, incluindo `Available = [3, 3, 2]`, `Allocation[P1] = [2, 0, 0]` e `Need[P1] = [1, 2, 2]`.

[Saída completa do teste 05](saidas/teste_05_acima_da_necessidade.txt)

## 8. Passo a passo para reproduzir

1. Abra um terminal na raiz do repositório e entre na pasta:

   ```bash
   cd avaliacoes/atividade-07
   ```

2. Execute a demonstração fornecida. Ela mostra o estado inicial, a sequência segura, o pedido concedido de P1 e o pedido bloqueado de P4:

   ```bash
   python -X utf8 bankers_algorithm.py
   ```

3. Execute os cinco testes e gere novamente os arquivos `.txt` em `saidas/`:

   ```bash
   python -X utf8 executar_testes.py --gerar-saidas
   ```

4. Confira `RESULTADO: TESTE NN APROVADO` no final de cada caso. A aprovação significa que o comportamento obtido coincide com o esperado, inclusive nos pedidos negados. Uma divergência encerra a execução com `AssertionError`.

5. Execute um teste por vez para capturar as telas, alterando o número de 1 a 5:

   ```bash
   python -X utf8 executar_testes.py --teste 1
   ```

6. Capture a execução com o nome **Guilherme Tomé Frazão** e o resultado visíveis. Para saídas longas, faça duas capturas, incluindo o início e o final. Salve em `prints/`, seguindo as [orientações dos prints](prints/README.md).

7. Confira os arquivos no GitHub após o envio das alterações e utilize o link da pasta `avaliacoes/atividade-07` na entrega da atividade.

O parâmetro `-X utf8` preserva acentos e símbolos no terminal do Windows. Os testes usam apenas a biblioteca padrão do Python; não é necessário instalar pacotes.

## 9. Situação das evidências

Os cinco cenários foram executados e seus resultados foram verificados automaticamente. Os arquivos de texto registram as saídas reais, com identificação do aluno. **Os prints de execução ainda estão pendentes**, pois a ferramenta de captura foi interrompida antes de obtê-los.

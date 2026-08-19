# Concentração e Entrega

Notebook: `03_concentracao_e_entrega.ipynb`
Autor: Evanio Alves Carvalho

Este notebook parte de duas perguntas que o `02` deixou em aberto: por que a receita está presa a São Paulo, e
por que o cliente parou de vir em 2018.

## Como o atraso é medido

A data prometida vem sem hora na base, sempre meia-noite. A data real vem com hora cheia. Comparar as duas
direto conta como atrasado um pedido entregue no dia certo às 15h. São 1.292 pedidos, e isso sozinho muda o
atraso de 6,8% para 8,1%.

Critério adotado no projeto: **atraso é comparado apenas pela data, ignorando a hora.** A coluna já vem
pronta do notebook 01.

## Métricas principais

- Atraso na janela analisada: 6,79% dos pedidos entregues
- Top 5 estados: 73,1% da receita, entrega média de 10,5 dias
- Outros 22 estados: 26,9% da receita, entrega média de 17,3 dias
- Correlação entre dias de entrega e participação na receita: -0,60

| Estado | % receita | Dias até entregar | % atraso | Frete sobre produto |
|---|---|---|---|---|
| SP | 37,4% | 8,3 | 4,5% | 13,8% |
| RJ | 13,4% | 14,8 | 12,1% | 16,8% |
| MG | 11,7% | 11,5 | 4,6% | 17,1% |
| MA | 0,95% | 21,1 | 17,5% | 26,2% |
| AL | 0,61% | 24,0 | 21,5% | 19,8% |
| RR | 0,06% | 29,5 | 12,5% | 27,8% |

## Achados

1. **A entrega explica parte da concentração, mas não tudo.** Os cinco estados que fazem 73% da receita
   recebem em 8 a 15 dias. Os que quase não vendem esperam de 21 a 29 dias. A correlação entre tempo de
   entrega e participação na receita é -0,60. Não dá para afirmar causa, porque SP também concentra população
   e renda, mas a entrega é a parte do problema que a empresa consegue mudar.

2. **Não é só o tempo, é o custo.** Em SP o frete é 13,8% do valor do produto. No Maranhão e em Roraima passa
   de 26%, quase o dobro. Comprar fora do Sudeste é mais caro e mais demorado ao mesmo tempo.

3. **Atrasar e demorar são coisas diferentes.** Alagoas entrega em 24 dias e atrasa 21,5% das vezes. Roraima
   demora mais, 29,5 dias, e atrasa 12,5%. Amapá demora 26,7 dias e atrasa só 3%. Onde o atraso é alto sem
   que o tempo seja o pior, o problema é o prazo prometido estar mal calibrado, o que é bem mais barato de
   corrigir do que a operação.

4. **O atraso reduz a recompra, mas pouco.** Entre clientes cuja primeira compra foi entregue no prazo, 4,08%
   voltaram a comprar. Entre os que tiveram atraso, 3,16%. Queda de 22,6% em termos relativos, com p-valor de
   0,007, então não é acaso. Mas a diferença absoluta é de 0,92 ponto percentual.

## O cuidado que o achado 4 exige

Mesmo entregando tudo no prazo, cerca de 96% dos clientes não voltam. O atraso agrava um problema que já é
grave por outro motivo.

Isso importa para não superestimar perda de receita. Estimativas que multiplicam o número de clientes
insatisfeitos pelo ticket médio cheio assumem que todos teriam voltado, o que os dados não sustentam. O
cálculo honesto usa a diferença entre os dois grupos, 0,92 ponto percentual, e não o valor integral.

## Ligação com o notebook 02

A receita parou de crescer porque faltou cliente, e o cliente é mais difícil de conquistar exatamente onde
entregar é caro e lento. Melhorar logística regional ataca as duas coisas ao mesmo tempo.

Mas como o atraso explica menos de 1 ponto percentual da recompra, resolver só a entrega não vai criar uma
base fiel. A retenção precisa ser atacada por outro caminho.

## Decisões de dados

- Receita usa o mesmo recorte do notebook 02: jan/2017 a ago/2018, sem `canceled` e `unavailable`.
- Métricas de entrega usam apenas pedidos com status `delivered` e data de entrega preenchida, porque pedido
  que não chegou não tem tempo mensurável.
- A análise de recompra limita a primeira compra a antes de março de 2018, garantindo pelo menos seis meses de
  janela para o cliente voltar. Sem esse corte, quem comprou em agosto de 2018 puxaria a recompra para baixo
  sem motivo.
- Recompra medida por `customer_unique_id`, não por `customer_id`, que muda a cada pedido.
- Frete sobre produto calculado pelo método agregado (soma do frete dividida pela soma dos produtos). O método
  alternativo, média das razões item a item, resulta em 47% a 59% para os mesmos estados, porque item barato
  com frete fixo gera razão muito alta e pesa igual a uma venda grande.

# Concentração e Entrega

Notebook: `03_concentracao_entrega.ipynb`

Responde à pergunta deixada pelo `02`: por que a receita está presa a poucos estados, e isso tem relação com
o cliente ter parado de vir.

## Critério de atraso

A data prometida vem sem hora na base e a data real vem com hora cheia. Comparar as duas diretamente
classifica como atrasado um pedido entregue no dia certo às 15h, o que afeta 1.292 registros e move o atraso
de 6,8% para 8,1%. Adotada a comparação apenas por data.

## Métricas

- Atraso no período: 6,79% dos pedidos entregues
- Top 5 estados: 73,1% da receita, entrega em 10,5 dias
- Outros 22 estados: 26,9% da receita, entrega em 17,3 dias
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

1. **A entrega explica parte da concentração.** Os estados que concentram receita recebem em 10,5 dias, os
   demais em 17,3. Correlação de -0,60. É correlação e não prova de causa, já que SP concentra população e
   renda, mas é a parcela do problema que a empresa controla.

2. **Não é só o tempo, é o custo.** O frete equivale a 13,8% do valor do produto em SP e ultrapassa 26% no
   Maranhão e em Roraima. Fora dos cinco estados líderes, comprar demora quase o dobro e custa quase o dobro
   de frete.

3. **Atrasar não é demorar.** Alagoas atrasa 21,5% entregando em 24 dias, enquanto Roraima atrasa 12,5%
   entregando em 29,5. Onde o atraso é alto sem que o tempo seja o pior, o problema está no prazo prometido,
   cuja correção é mais rápida e barata que mudar a operação.

4. **O atraso reduz a recompra, mas pouco.** Clientes atendidos no prazo voltam em 4,08% dos casos, contra
   3,16% dos que sofreram atraso. Queda de 22,6% em termos relativos, com p-valor de 0,007. A diferença
   absoluta, porém, é de 0,92 ponto percentual.

## O cuidado que o achado 4 exige

Mesmo com entrega pontual, cerca de 96% dos clientes não retornam. O atraso agrava um problema de retenção
preexistente.

Isso invalida estimativas de perda que multiplicam clientes insatisfeitos pelo ticket médio integral, porque
elas pressupõem que todos retornariam. A conta correta usa a diferença entre os dois grupos.

## Decisões de dados

- Receita usa o mesmo recorte do `02`.
- Métricas de entrega usam apenas pedidos com status `delivered` e data de entrega preenchida.
- A análise de recompra limita a primeira compra a antes de março de 2018, garantindo seis meses de janela.
- Recompra medida por `customer_unique_id`, que identifica a pessoa, e não por `customer_id`, que muda a cada
  pedido.
- Frete sobre produto pelo método agregado. A média das razões item a item resultaria em 55,0% no Maranhão e
  58,0% em Roraima, porque itens baratos com frete fixo geram razões muito altas e pesam igual a vendas grandes.

## Fechando com o notebook 02

O crescimento parou por falta de clientes, e conquistar cliente é mais difícil onde entregar é lento e caro.
Logística regional ataca os dois problemas. Mas como o atraso explica menos de um ponto percentual da
recompra, a retenção precisa de uma frente própria.

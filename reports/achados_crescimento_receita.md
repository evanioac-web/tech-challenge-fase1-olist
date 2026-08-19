# Crescimento e Receita

Notebook: `02_crescimento_e_receita.ipynb`
Autor: Evanio Alves Carvalho

## Período analisado

Janeiro de 2017 a agosto de 2018.

A base cobre de setembro de 2016 a outubro de 2018, mas as pontas são resíduo de operação: set/2016 tem 4
pedidos, out/2016 tem 324, nov/2016 não existe e dez/2016 tem 1. No outro extremo, set e out de 2018 somam
20 pedidos.

Escolher outro mês de partida distorce completamente o resultado:

| Mês base | Crescimento até ago/2018 |
|---|---|
| set/2016 | 356.357% |
| dez/2016 | 5.081.314% |
| out/2016 | 1.841% |
| jan/2017 | 628% |

## Métricas principais

- Receita: R$ 15.683.706,74 (R$ 13,45mi de produto e R$ 2,23mi de frete)
- Pedidos: 97.905
- Crescimento de jan/2017 a ago/2018: cerca de 628%
- Valor do pedido: média R$ 160,19, mediana R$ 105,28, coeficiente de variação 137%
- Concentração: SP 37,4% | top 5 estados 73,1% | top 5 categorias 39,3% (de 72) | top 10 vendedores 12,9% (de 3.029)

## Achados

1. **O crescimento descreve 2017, não 2018.** A receita sobe forte no primeiro ano e estaciona depois. A média
   mensal do segundo quadrimestre de 2018 é 4,3% menor que a do primeiro. Projetar 628% para frente seria o
   erro mais caro possível com esses dados.

2. **O platô é de demanda, não de oferta.** Ao longo de 2018 os vendedores ativos subiram 31% (968 para 1.266)
   e mesmo assim a receita não cresceu. Os clientes caíram 10% (7.088 para 6.380) e a receita por vendedor
   encolheu 31% (R$ 1.138 para R$ 788). A plataforma continuou atraindo quem vende sem atrair quem compra.

3. **O maior mês da série é sazonalidade, não patamar novo.** Novembro de 2017 supera qualquer mês de 2018,
   mas 24/11 sozinho teve 1.166 pedidos contra média de 191 nos outros dias, 6 vezes um dia comum. É Black
   Friday. Dezembro já cai de volta.

4. **O crescimento veio de volume, não de ticket.** O valor do pedido ficou estável no período todo. A média
   bem acima da mediana indica distribuição assimétrica, com poucos pedidos caros puxando a média.

5. **O risco é geográfico, não de portfólio.** Por categoria e por vendedor a receita está bem distribuída.
   Por estado não: SP sozinho é 37,4% e os cinco maiores somam 73,1%, sobrando 26,9% para os outros 22.

## Projeção

Com a receita estável, a média dos últimos três meses estima cerca de R$ 1 milhão/mês, ou R$ 3,06 milhões no
trimestre seguinte, 15,2% acima do mesmo trimestre de 2017.

O valor importa menos que o recado: a melhor estimativa possível é repetir os últimos meses. A projeção
confirma o platô em número. Serve como referência de ordem de grandeza, não como meta, e novembro
provavelmente ficaria acima por causa da Black Friday.

## Decisões de dados

- Receita é preço do produto mais frete, no grão de item.
- Excluídos os status `canceled` e `unavailable`: 0% dos `unavailable` e apenas 77,2% dos `canceled` têm
  produto associado, ou seja, a venda não se concretizou. Os demais status têm 100% e foram mantidos.
- Outliers de preço mantidos. O IQR aponta 7,5% dos itens acima de R$ 277, chegando a R$ 6.735, mas são
  valores plausíveis para móvel e eletrônico e não há preço negativo nem zerado. A assimetria é tratada
  reportando mediana junto com a média.

## Limitação

A base não informa a comissão que a Olist retém por venda. O que este trabalho chama de receita é o valor
transacionado, então não é possível calcular lucro, margem ou retorno. Nenhuma conclusão aqui fala sobre
rentabilidade.

## Pergunta que fica

Por que a receita está tão presa a São Paulo, e o que impede os outros 22 estados de comprarem mais? É o que
o notebook 03 investiga.

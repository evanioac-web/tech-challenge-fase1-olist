# Crescimento e Receita

Notebook: `02_receita.ipynb`

## Recorte

Janeiro de 2017 a agosto de 2018, excluídos os status `canceled` e `unavailable`.

Agosto de 2018 tem coleta só até o dia 29 e está incompleto. Ele fica no recorte por ter três semanas de
venda real, mas não é usado como ponto de comparação: as variações de 2018 abaixo usam janeiro e julho.

As pontas da base distorcem qualquer cálculo de crescimento. O efeito de escolher outro mês de partida:

| Mês base | Pedidos no mês | Crescimento até ago/2018 |
|---|---|---|
| set/2016 | 4 | 356.357% |
| out/2016 | 324 | 1.841% |
| dez/2016 | 1 | 5.081.314% |
| jan/2017 | 787 | 628% |

## Métricas

- Valor transacionado: R$ 15.683.706,74 (R$ 13,45mi produto, R$ 2,23mi frete). Não é a comissão da Olist.
- Pedidos: 97.905 | Clientes: 94.703 | Vendedores: 3.029
- Valor do pedido: média R$ 160,19, mediana R$ 105,28, CV 137%
- Concentração: SP 37,4% | top 5 estados 73,1% | top 5 categorias 39,3% de 73 | top 10 vendedores 12,9% de 3.029

## Achados

1. **O crescimento de 628% descreve 2017, não 2018.** A receita estaciona no último ano da série, e a média
   mensal recua 2,6% de jan-abr para mai-jul de 2018, comparando apenas meses fechados.

2. **O limite está na demanda.** Entre janeiro e julho de 2018 os vendedores ativos cresceram 28,6% (968 para
   1.245), os clientes caíram 12,9% (7.088 para 6.172) e o valor por vendedor recuou 26,6% (R$ 1.138 para
   R$ 835). Ampliar a oferta antes de resolver a demanda deteriora o resultado de quem já opera na plataforma.

3. **O crescimento veio de volume, não de valor.** O ticket permaneceu estável no período inteiro.

4. **O maior mês da série é sazonalidade, e custou caro na entrega.** Novembro de 2017 supera todos os meses
   de 2018 por causa de um único dia: 24/11 registrou 1.166 pedidos contra média de 191 nos dias fora do fim
   de semana promocional, seis vezes o volume normal. Quem comprou naquele fim de semana esperou 16,9 dias
   contra 12,1 da média do período e atrasou em 18,3% dos casos contra 6,8%.

5. **O risco é geográfico.** Categoria e vendedor estão diversificados. Estado não.

## Projeção

Média dos últimos três meses: cerca de R$ 1,02 milhão por mês, R$ 3,06 milhões no trimestre, 15,2% acima do
mesmo período de 2017.

A leitura importa mais que o valor: a melhor estimativa possível é repetir os últimos meses. A projeção
confirma o platô, e é conservadora porque agosto entra na média incompleto. Novembro tende a superá-la por causa da Black Friday, e a base termina em agosto de 2018,
o que impede verificar o acerto.

## Limitação

A base não informa a comissão retida pela Olist. O que este documento chama de valor transacionado é preço
dos itens mais frete, então não é possível calcular margem, lucro ou retorno. Nenhuma decisão de aporte deve
tratar esse número como receita da plataforma.

## Pergunta que fica

Se o limite está na demanda e a demanda se concentra em São Paulo, o que impede os outros 22 estados de
comprarem mais?

# Indicadores calculados

Estes arquivos não são dados originais nem foram editados à mão. Todos são gerados pelos notebooks e podem
ser reproduzidos rodando o projeto do zero.

## De onde vêm

```
Kaggle (9 CSVs originais)
   ↓  data/raw/
01_limpeza.ipynb          corrige tipos, valida, monta o modelo dimensional
   ↓  data/processed/fato_itens.csv          (112.650 linhas, 1 por item de pedido)
   ↓  data/processed/pedidos_tratados.csv    (99.441 linhas, 1 por pedido)
02_receita.ipynb / 03_concentracao_entrega.ipynb
   aplicam o recorte e agregam
   ↓  data/kpis/*.csv
```

O recorte aplicado nos notebooks 02 e 03 é sempre o mesmo: período de janeiro de 2017 a agosto de 2018, sem
os status `canceled` e `unavailable`. As métricas de entrega usam adicionalmente apenas pedidos com status
`delivered` e data de entrega preenchida.

## O que cada arquivo sustenta

| Arquivo | Gerado em | Como | Sustenta no relatório |
|---|---|---|---|
| `kpi_evolucao_mensal.csv` | 02, célula 35 | receita e pedidos agrupados por mês | crescimento de 628% e a queda de 4,3% no 2º quadrimestre de 2018 |
| `kpi_serie_completa.csv` | 02 | receita por mês em toda a base, sem recorte | justificativa de excluir 2016 |
| `kpi_novembro_diario.csv` | 02, célula 35 | pedidos únicos por dia em novembro de 2017 | os 1.166 pedidos do dia 24 contra média de 191 |
| `kpi_vendedores_clientes.csv` | 02, célula 35 | contagem de vendedores e clientes distintos por mês | vendedores +30,8%, clientes -10,0%, receita por vendedor -30,8% |
| `kpi_receita_categoria.csv` | 02, célula 27 | soma de receita por categoria | 72 categorias, top 5 com 39,3% |
| `kpi_receita_estado.csv` | 02, célula 27 | soma de receita e pedidos por UF do cliente | SP com 37,4%, top 5 com 73,1% |
| `kpi_top_sellers.csv` | 02, célula 27 | soma de receita por vendedor | 3.029 vendedores, top 10 com 12,9% |
| `kpi_previsao.csv` | 02, célula 33 | média dos últimos 3 meses replicada | projeção de cerca de R$ 1 milhão por mês |
| `kpi_entrega_estado.csv` | 03, célula 5 | receita, dias médios de entrega e % de atraso por UF | 10,5 dias no top 5 contra 17,3 nos demais, correlação -0,60 |
| `kpi_frete_estado.csv` | 03, célula 15 | frete e produto somados por UF, nos dois métodos | frete de 13,8% em SP contra mais de 26% em MA e RR |
| `kpi_recompra_atraso.csv` | 03, célula 21 | recompra agrupada por atraso na primeira compra | 4,08% no prazo contra 3,16% com atraso |

## Uma observação sobre a projeção

O `kpi_previsao.csv` é o único arquivo que não é observação. Ele é resultado de um cálculo: a média dos três
últimos meses replicada para os três meses seguintes. Está aqui para tornar a projeção auditável, mas não
deve ser lido como dado histórico.

## Sobre o arquivo de vendedores

O `kpi_top_sellers.csv` tem 3.029 linhas e é o maior da pasta. Ele foi mantido completo de propósito: sem a
lista inteira não é possível verificar a afirmação de que os dez maiores concentram 12,9% do total, porque
faltaria o denominador.

## Como conferir um número

Abra o CSV correspondente e some ou filtre a coluna. Não é necessário baixar a base do Kaggle nem executar os
notebooks para validar qualquer percentual citado no relatório.

Se preferir refazer do zero, siga as instruções do README principal e execute os notebooks na ordem numerada.
Os arquivos desta pasta são reescritos a cada execução.

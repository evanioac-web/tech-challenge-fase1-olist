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
| `kpi_evolucao_mensal.csv` | notebook 02, variável `por_mes` | receita e pedidos agrupados por mês | crescimento de 628% e a queda de 2,6% na média mensal de mai-jul/2018 frente a jan-abr/2018 |
| `kpi_serie_completa.csv` | notebook 02, variável `todos_meses` | receita por mês em toda a base, sem recorte | justificativa de excluir 2016 |
| `kpi_novembro_diario.csv` | notebook 02, variável `nov_por_dia` | pedidos únicos por dia em novembro de 2017 | os 1.166 pedidos do dia 24 contra média de 191 |
| `kpi_vendedores_clientes.csv` | notebook 02, variável `por_mes_detalhe` | contagem de vendedores e clientes distintos por mês | jan-vs-jul/2018: vendedores +28,6%, clientes -12,9%, valor transacionado por vendedor -26,6% |
| `kpi_receita_categoria.csv` | notebook 02, variável `por_categoria` | soma de receita por categoria | 73 categorias, top 5 com 39,3% |
| `kpi_receita_estado.csv` | notebook 02, variável `por_estado` | soma de receita e pedidos por UF do cliente | SP com 37,4%, top 5 com 73,1% |
| `kpi_top_sellers.csv` | notebook 02, variável `por_vendedor` | soma de receita por vendedor | 3.029 vendedores, top 10 com 12,9% |
| `kpi_previsao.csv` | notebook 02, variável `previsao` | média dos últimos 3 meses replicada | projeção de cerca de R$ 1 milhão por mês |
| `kpi_entrega_estado.csv` | notebook 03, variável `uf` | receita, dias médios de entrega e % de atraso por UF | 10,5 dias no top 5 contra 17,3 nos demais, correlação -0,60 |
| `kpi_frete_estado.csv` | notebook 03, variável `frete_uf` | frete e produto somados por UF, nos dois métodos | frete de 13,8% em SP contra mais de 26% em MA e RR |
| `kpi_recompra_atraso.csv` | notebook 03, variável `comparacao` | recompra agrupada por atraso na primeira compra | 4,08% no prazo contra 3,16% com atraso |

## Sobre o arquivo de categorias

O `kpi_receita_categoria.csv` soma R$ 15,48 milhões, e não os R$ 15,68 milhões do período. A diferença de
R$ 206 mil, equivalente a 1,3% da receita, vem de 1.587 itens cujo produto não tem categoria preenchida na
base original. Esses itens entram na receita total, mas não podem ser atribuídos a nenhuma categoria. Os
39,3% das cinco maiores são calculados sobre a receita total do período, não sobre a soma desta planilha.

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

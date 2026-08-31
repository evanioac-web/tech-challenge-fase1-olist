# Case E-commerce Olist | Tech Challenge Fase 1

Relatório executivo para investidores, baseado no Brazilian E-Commerce Public Dataset by Olist.

Neste projeto, **valor transacionado** é o preço dos itens somado ao frete. Não é a receita líquida nem a
comissão da Olist, que a base não informa.

POSTECH Data Analytics

## Integrantes

- Eduardo Zancanaro Vilela
- Evanio Alves Carvalho
- Marcela Morillas de Souza
- Mateus Araújo

## Entregáveis

| Item | Arquivo | Leitura direta |
|---|---|---|
| Repositório com os códigos | este repositório | |
| Relatório executivo | [`.docx`](reports/relatorio_executivo_olist.docx) | [ler em PDF](reports/relatorio_executivo_olist.pdf) |
| Apresentação executiva | [`.pptx`](reports/apresentacao_crescimento_receita.pptx) | [ler em PDF](reports/apresentacao_crescimento_receita.pdf) |
| Vídeo executivo (até 5 min) | _link a incluir_ | |

Os PDFs são cópias dos arquivos ao lado, geradas sem edição, para abrir direto no navegador. O GitHub não
exibe `.docx` nem `.pptx`.

---

## A pergunta

A Olist é um bom investimento, e onde o capital renderia mais?

A análise segue a progressão descritiva, diagnóstica, preditiva e prescritiva. Cada notebook responde à
pergunta que o anterior deixou em aberto.

## A resposta, em três linhas

A receita cresceu cerca de 628% entre janeiro de 2017 e agosto de 2018, mas esse número descreve o primeiro
ano. Em 2018 o crescimento para.

O motivo é demanda, não oferta. Entre janeiro e julho de 2018, os dois meses fechados que delimitam o ano na
base, os vendedores ativos cresceram 28,6% enquanto os clientes caíram 12,9% e o valor por vendedor recuou
26,6%.

A demanda não aparece onde a operação é pior. Os cinco estados que concentram 73,1% da receita recebem em 10,5
dias, os outros 22 esperam 17,3 dias e pagam quase o dobro de frete em proporção ao produto.

| Indicador | Resultado |
|---|---|
| Valor transacionado (jan/2017 a ago/2018) | R$ 15,68 milhões |
| Pedidos | 97.905 |
| Crescimento no período | cerca de 628% |
| Jan-abr para mai-jul de 2018 | -2,6% |
| Valor do pedido (média / mediana) | R$ 160,19 / R$ 105,28 |
| São Paulo | 37,4% da receita |
| Cinco maiores estados | 73,1% |
| Vendedores ativos (jan a jul/2018) | 968 para 1.245 (+28,6%) |
| Clientes (jan a jul/2018) | 7.088 para 6.172 (-12,9%) |
| Valor por vendedor (jan a jul/2018) | R$ 1.138 para R$ 835 (-26,6%) |
| Projeção do trimestre seguinte | cerca de R$ 1 milhão por mês |

---

## Estrutura

```
data/
  raw/         CSVs originais do Kaggle, não versionados
  processed/   base tratada gerada pelo notebook 01, não versionada
  kpis/        indicadores calculados, em CSV
notebooks/
  01_limpeza.ipynb              preparação da base, sem filtros de análise
  02_receita.ipynb              crescimento, causa do platô e projeção
  03_concentracao_entrega.ipynb concentração geográfica e efeito da entrega
reports/       achados em markdown, relatório executivo e apresentação, em formato editável e em PDF
figures/       gráficos gerados pelos notebooks
```

Os notebooks rodam na ordem numerada. O `01` grava em `data/processed/`, de onde os outros leem.

### Por que a limpeza fica separada

O `01` não aplica nenhum filtro de análise. Não corta período e não remove status de pedido.

Isso é proposital: cada frente do projeto precisa de um recorte diferente, e quem analisa cancelamento precisa
justamente dos pedidos que o cálculo de receita descarta. Filtrar na base comum inviabilizaria outras
análises, e garante que todos partam dos mesmos números.

---

## Decisões de tratamento

Todas justificadas com evidência dentro dos notebooks.

**Receita = preço do produto + frete**, no grão de item. É o valor transacionado, não a receita própria da
plataforma.

**Período de janeiro de 2017 a agosto de 2018.** As pontas da base são resíduo de operação. Partindo de
setembro de 2016 o crescimento daria 356.357%, de dezembro de 2016 daria 5.081.314%. Janeiro de 2017 é o
primeiro mês com volume constante.

**Exclusão de `canceled` e `unavailable` nas análises de receita.** Apenas 1,0% dos pedidos `unavailable` tem
produto associado e 73,8% dos `canceled` têm, contra 99% ou mais nos demais status.

**Atraso comparado apenas pela data.** A data prometida vem sem hora e a data real vem com hora cheia.
Comparar diretamente classifica como atrasado um pedido entregue no dia certo às 15h, o que afeta 1.292
registros e move o atraso de 6,8% para 8,1%.

**`payments` e `reviews` agregados por pedido antes dos merges.** Ambas têm mais de uma linha por pedido, e
sem agregar a receita contaria em dobro.

**Outliers de preço mantidos.** O IQR aponta 7,4% dos itens acima de R$ 277, com máximo de R$ 6.735, valores
plausíveis para móvel e eletrônico. Não há preço negativo nem zerado. A assimetria é tratada reportando
mediana junto com média.

**Agosto de 2018 mantido, mas não usado como ponto de comparação.** A coleta para no dia 29 e os últimos seis
dias já vêm decaindo, contra 264 pedidos por dia nas três primeiras semanas. Falta perto de um quarto do mês.
Ele fica no recorte por ter três semanas de venda real, mas as variações de 2018 usam janeiro e julho.

**Meio de pagamento do pedido é o de maior valor**, quando há mais de um. Simplificação registrada, não
utilizada nas análises desta entrega.

**Recompra medida por `customer_unique_id`**, que identifica a pessoa, e não por `customer_id`, que é gerado a
cada pedido.

**`geolocation` fora do escopo**, por repetir coordenadas por prefixo de CEP enquanto a UF já vem em
`customers`.

---

## Modelagem

Modelo dimensional com tabela fato no grão de item de pedido:

```
fato_itens
  ├── dim_clientes
  ├── dim_produtos
  └── dim_vendedores
```

A tabela fato é validada após a construção: a contagem de linhas deve permanecer em 112.650, a soma de `price`
deve coincidir com a origem e as quatro chaves (`order_id`, `product_id`, `seller_id`, `customer_id`) devem
existir na tabela de origem. As verificações constam no notebook 01, com a saída salva.

---

## Como reproduzir

1. Baixe o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Coloque os 9 arquivos CSV em `data/raw/`
3. Instale as dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Abra os notebooks de `notebooks/` e execute na ordem numerada. Eles leem e escrevem com caminhos
   relativos à própria pasta, então funcionam abrindo direto pelo Jupyter

Cada percentual citado no relatório tem uma célula correspondente que o calcula.

---

## Limitações

A base não informa a comissão retida pela Olist nem o custo de aquisição de clientes. Não é possível calcular
margem, lucro ou retorno, e nenhuma conclusão trata de rentabilidade.

A relação entre tempo de entrega e receita por estado é correlação, não causa. São Paulo concentra também
população e renda.

O efeito do atraso sobre a recompra é estatisticamente significativo (p = 0,007) e pequeno em termos
absolutos: 0,92 ponto percentual. Mesmo com entrega no prazo, cerca de 96% dos clientes não retornam.

---

## Tecnologias

Python, pandas, matplotlib, seaborn, scipy, Jupyter.

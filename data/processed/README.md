# data/processed

Esta pasta recebe a base já tratada, gerada pelo notebook `01_limpeza.ipynb`.

Ela está vazia no repositório porque o conteúdo é reproduzível. A tabela fato sozinha passa de 40 MB, e
versionar arquivo grande que pode ser recriado a qualquer momento só polui o histórico.

## O que aparece aqui depois de rodar o notebook 01

| Arquivo | Conteúdo |
|---|---|
| `fato_itens.csv` | tabela fato, 112.650 linhas, uma por item de pedido |
| `pedidos_tratados.csv` | 99.441 pedidos, com as colunas `atrasou`, `dias_entrega` e `mes` já calculadas |
| `dim_clientes.csv` | dimensão de cliente |
| `dim_produtos.csv` | dimensão de produto, com categoria traduzida |
| `dim_vendedores.csv` | dimensão de vendedor |

Os notebooks `02` e `03` leem daqui. Rodar qualquer um deles sem ter executado o `01` antes resulta em erro
de arquivo não encontrado.

## Importante

Esta base não tem filtro de análise aplicado. O período completo e todos os status de pedido estão presentes,
inclusive `canceled` e `unavailable`. Cada notebook de análise aplica o próprio recorte e justifica a escolha.

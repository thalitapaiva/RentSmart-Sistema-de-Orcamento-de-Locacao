# RentSmart — Orçamento de Locação (R.M Imóveis)

Aplicação em Python que calcula o orçamento mensal de locação de imóveis da R.M Imóveis
(apartamento, casa ou estúdio), mostra o detalhamento do valor e gera um CSV com a
projeção dos 12 primeiros meses do contrato.

## Requisitos
- Python 3.8 ou superior
- Nenhuma biblioteca externa (só `csv`, que já vem com o Python)

## Como executar
```bash
git clone <link-do-repositorio>
cd rentsmart
python main.py
```
(no Linux/Mac pode ser `python3 main.py`)

Responda às perguntas no terminal. No final o resumo é exibido e o arquivo
`projecao_12_meses.csv` é criado na mesma pasta.

## Estrutura
| Arquivo | Conteúdo |
|---|---|
| `main.py` | Interação com o usuário e validação das entradas |
| `imoveis.py` | Classes `Imovel`, `ImovelComQuartos`, `Apartamento`, `Casa`, `Estudio` |
| `orcamento.py` | Classes `TaxaContratual` e `Orcamento` (resumo e CSV) |

## Regras implementadas
- Apartamento: R$ 700,00 | 2 quartos +R$ 200,00 | garagem +R$ 300,00 | sem crianças: 5% de desconto sobre o aluguel já com adicionais
- Casa: R$ 900,00 | 2 quartos +R$ 250,00 | garagem +R$ 300,00
- Estúdio: R$ 1.200,00 | estacionamento: pacote de 2 vagas R$ 250,00 + R$ 60,00 por vaga extra
- Taxa contratual de R$ 2.000,00 em até 5 parcelas, cobrada separada do aluguel (a última parcela ajusta os centavos)

## Exemplo de saída (CSV)
Apartamento 2 quartos, com garagem, sem crianças, taxa em 3x:
```
Mes;Aluguel (R$);Parcela taxa contratual (R$);Total do mes (R$)
1;1140,00;666,67;1806,67
...
12;1140,00;0,00;1140,00
```

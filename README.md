# pj-calc

Quanto da conta PJ (Simples Nacional, Anexo III) pode ir para a conta PF, a partir do
faturamento do mês e do pró-labore bruto.

O INSS do sócio sai **de dentro** do pró-labore (é retido), não é custo adicional:

```
lucros       = faturamento − DAS − pró-labore bruto − outras despesas
total à PF   = pró-labore líquido + lucros
             = faturamento − DAS − INSS − IRRF − outras despesas
```

## Instalação

```bash
uv tool install --editable ~/Playground/pj-calc
```

Para desenvolver:

```bash
uv sync
uv run pytest
```

## Uso

```bash
pj-calc 8704 2437,12
pj-calc 8.704,00 2.437,12 --despesas 250      # contador, tarifas...
pj-calc 15000 4500 --aliquota-das 0.112       # outra faixa do Simples
pj-calc 8704 2437,12 --json
```

Valores aceitam `8704`, `8704.00`, `8.704,00` ou `R$ 8.704,00`.

Alertas emitidos:

- Fator R do mês abaixo de 28% (risco de Anexo V), com o pró-labore mínimo;
- Fator R exatamente no limite (o Simples usa a média de 12 meses);
- pró-labore acima de R$ 5.000 (passa a haver IRRF no DARF);
- lucros negativos.

## Parâmetros tributários (vigência 2026)

Defaults em `src/pj_calc/config.py`. Podem ser sobrescritos por variável de ambiente
`PJ_CALC_*` (ex.: `PJ_CALC_ALIQUOTA_DAS=0.112`) ou por `~/.config/pj-calc/config.toml`:

```toml
aliquota_das = "0.06"
teto_inss = "8475.55"
```

| Parâmetro | Default | Observação |
|---|---|---|
| `aliquota_das` | 6% | alíquota **efetiva**; sobe com o faturamento acumulado de 12 meses |
| `aliquota_inss` / `teto_inss` | 11% / R$ 8.475,55 | teto do INSS 2026 — confira a portaria do ano |
| `tabela_ir` | tabela mensal de maio/2025 | base = pró-labore − max(INSS, desconto simplificado) |
| redutor | Lei 15.270/2025 | zera o IR até R$ 5.000; parcial até R$ 7.350 |

## Limitações

- Não calcula o Fator R de 12 meses, só o do mês.
- Assume que a distribuição de lucros é isenta: isso exige escrituração contábil completa.
  Sem ela, a parte isenta fica limitada à presunção (32% da receita − IRPJ).
- Não aplica a retenção de 10% sobre lucros acima de R$ 50 mil/mês (Lei 15.270/2025).
- Material de apoio; não substitui o contador.

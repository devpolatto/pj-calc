# Como funciona o cálculo: faturamento, impostos, pró-labore e lucros (Simples Nacional)

Este documento explica, passo a passo, quanto do faturamento de uma empresa do Simples Nacional chega à pessoa física do sócio e por qual caminho, usando uma simulação real como exemplo.

---

## 1. Dados da simulação

| Item | Valor |
|---|---|
| Faturamento do mês | R$ 8.704,00 |
| Pró-labore (definido automaticamente) | R$ 2.437,12 |
| DAS (Simples Nacional) | R$ 522,24 |
| DARF (INSS sobre o pró-labore) | R$ 268,08 |
| **Total de impostos** | **R$ 790,32** |
| **Faturamento líquido** | **R$ 7.913,68** |

---

## 2. Os conceitos

### DAS: imposto da empresa
É a guia única do Simples Nacional. Incide sobre o **faturamento** e reúne vários tributos (IRPJ, CSLL, PIS, COFINS, ISS e a contribuição previdenciária patronal, a CPP, no Anexo III).

> 8.704,00 × 6% = **R$ 522,24** (alíquota inicial do Anexo III)

### Pró-labore: "salário" do sócio
É a remuneração do sócio pelo trabalho na empresa. Sobre ele incidem:

- **INSS de 11%**, retido do próprio sócio (é descontado do pró-labore)
- **IRRF**, imposto de renda **da pessoa física** retido na fonte, conforme a tabela progressiva

### DARF: guia do INSS (e do IRRF, se houver)
É gerado pela DCTFWeb e recolhe o que foi **retido do pró-labore**.

> 2.437,12 × 11% = **R$ 268,08**

Nesta simulação o DARF é composto **só de INSS**: um pró-labore de R$ 2.437,12 fica bem abaixo da faixa de isenção do IR, que em 2026 subiu para R$ 5.000,00 mensais. Por isso o IRRF é zero.

### Distribuição de lucros
É o que sobra na empresa depois de pagar os impostos e o pró-labore. Na pessoa física ela é **isenta de IR**, desde que os lucros estejam apurados na escrituração da empresa.

---

## 3. O ponto principal: o INSS sai de dentro do pró-labore

O erro mais comum é tratar o DARF como um custo **adicional** ao pró-labore. Ele não é adicional:

```
Pró-labore bruto        2.437,12
(−) INSS retido (11%)     268,08   → vai para o governo via DARF
= Pró-labore líquido    2.169,04   → vai para a conta do sócio
```

A empresa desembolsa **R$ 2.437,12 no total** com o pró-labore: uma parte vai para o sócio e a outra para o INSS.

---

## 4. Fluxo completo do dinheiro

| Etapa | Valor | Saldo na conta PJ |
|---|---|---|
| Faturamento recebido | | 8.704,00 |
| (−) DAS | 522,24 | 8.181,76 |
| (−) Pró-labore bruto | 2.437,12 | 5.744,64 |
| ↳ DARF (INSS 11%) pago ao governo | 268,08 | |
| ↳ Pró-labore líquido transferido ao sócio | 2.169,04 | |
| (−) Distribuição de lucros ao sócio | 5.744,64 | 0,00 |

### O que chega à pessoa física

| Origem | Valor |
|---|---|
| Pró-labore líquido | R$ 2.169,04 |
| Lucros distribuídos | R$ 5.744,64 |
| **Total recebido** | **R$ 7.913,68** |

Esse total bate exatamente com o **faturamento líquido** da simulação:

> 8.704,00 − 522,24 (DAS) − 268,08 (DARF) = **R$ 7.913,68**

---

## 5. Formas erradas de fazer a conta

### ❌ Erro 1: pró-labore bruto + lucros

```
Pró-labore 2.437,12 + Lucros 5.476,56 = 7.913,68
```

O total está certo, mas a **divisão está errada**. O cálculo considera que os R$ 2.437,12 inteiros vão para o sócio, quando R$ 268,08 deles vão para o DARF. Por isso os lucros ficam subestimados (5.476,56 em vez de 5.744,64). O total só bate porque um erro compensa o outro.

### ❌ Erro 2: descontar o INSS duas vezes

```
Pró-labore 2.437,12 − INSS 268,08 + Lucros 5.476,56 = 7.645,60
```

Aqui o INSS foi descontado **duas vezes**: uma no total de impostos (R$ 790,32) e outra no pró-labore. Na prática o sócio receberia R$ 268,08 a menos do que realmente tem direito.

### ✅ Forma correta

```
Pró-labore líquido 2.169,04 + Lucros 5.744,64 = 7.913,68
```

---

## 6. Fórmulas resumidas

```
DAS                = Faturamento × alíquota do Simples
INSS (DARF)        = Pró-labore × 11%
IRRF               = tabela progressiva sobre (Pró-labore − INSS)  → zero até R$ 5.000 em 2026
Pró-labore líquido = Pró-labore − INSS − IRRF
Lucros             = Faturamento − DAS − Pró-labore bruto
Total ao sócio     = Pró-labore líquido + Lucros
                   = Faturamento − DAS − INSS − IRRF
```

---

## 7. Por que o pró-labore é 28% do faturamento? (Fator R)

Para algumas atividades de serviço, o Simples usa o **Fator R** para definir o anexo:

> Fator R = Folha de pagamento (inclui pró-labore) dos últimos 12 meses ÷ Faturamento dos últimos 12 meses

| Fator R | Anexo | Alíquota inicial |
|---|---|---|
| ≥ 28% | Anexo III | 6% |
| < 28% | Anexo V | 15,5% |

Na simulação: 2.437,12 ÷ 8.704,00 = **28%**. É por isso que o pró-labore é calculado "automaticamente" nesse valor: é o **mínimo** necessário para manter a empresa no Anexo III, onde a alíquota é menor.

No Anexo III, a contribuição patronal (CPP, 20%) já está **incluída no DAS**, então não existe INSS patronal à parte. Só há os 11% retidos do sócio.

---

## 8. Observações

- A isenção dos lucros pressupõe escrituração contábil adequada. Confirme com seu contador.
- A alíquota efetiva do DAS sobe conforme o faturamento acumulado dos últimos 12 meses.
- Se o pró-labore passar de R$ 5.000,00 mensais, o IRRF passa a incidir e entra no DARF.
- Este material é explicativo e não substitui a orientação de um contador.
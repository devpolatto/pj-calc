"""Cálculo de quanto da conta PJ chega à PF: pró-labore líquido + distribuição de lucros.

O INSS do sócio sai de DENTRO do pró-labore (é retido), não é custo adicional. Por isso:

    lucros         = faturamento − DAS − pró-labore bruto − outras despesas
    total à PF     = pró-labore líquido + lucros
                   = faturamento − DAS − INSS − IRRF − outras despesas
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, Field

from pj_calc.config import Settings

CENTAVO = Decimal("0.01")


def centavos(valor: Decimal) -> Decimal:
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


class Entrada(BaseModel):
    faturamento: Decimal = Field(gt=0)
    pro_labore: Decimal = Field(ge=0)
    outras_despesas: Decimal = Field(default=Decimal("0"), ge=0)


class Resultado(BaseModel):
    entrada: Entrada
    das: Decimal
    inss: Decimal
    irrf: Decimal
    darf: Decimal
    pro_labore_liquido: Decimal
    lucros: Decimal
    total_pf: Decimal
    total_impostos: Decimal
    fator_r: Decimal
    alertas: list[str]


def calcular_irrf(pro_labore: Decimal, inss: Decimal, cfg: Settings) -> Decimal:
    """IRRF mensal: tabela sobre a menor base (INSS ou desconto simplificado), menos o redutor."""
    base = pro_labore - max(inss, cfg.desconto_simplificado)
    if base <= 0:
        return Decimal("0")

    imposto = Decimal("0")
    for faixa in cfg.tabela_ir:
        if faixa.ate is None or base <= faixa.ate:
            imposto = base * faixa.aliquota - faixa.deducao
            break
    imposto = max(imposto, Decimal("0"))

    # O redutor da Lei 15.270/2025 é calculado sobre o rendimento bruto, não sobre a base.
    if pro_labore <= cfg.redutor_isencao_ate:
        redutor = cfg.redutor_maximo
    elif pro_labore <= cfg.redutor_parcial_ate:
        redutor = cfg.redutor_parcial_constante - cfg.redutor_parcial_fator * pro_labore
    else:
        redutor = Decimal("0")

    return centavos(max(imposto - max(redutor, Decimal("0")), Decimal("0")))


def calcular(entrada: Entrada, cfg: Settings) -> Resultado:
    das = centavos(entrada.faturamento * cfg.aliquota_das)
    inss = centavos(min(entrada.pro_labore, cfg.teto_inss) * cfg.aliquota_inss)
    irrf = calcular_irrf(entrada.pro_labore, inss, cfg)

    pro_labore_liquido = entrada.pro_labore - inss - irrf
    lucros = entrada.faturamento - das - entrada.pro_labore - entrada.outras_despesas
    fator_r = entrada.pro_labore / entrada.faturamento

    alertas: list[str] = []
    if fator_r < cfg.fator_r_minimo:
        minimo = centavos(entrada.faturamento * cfg.fator_r_minimo)
        alertas.append(
            f"Fator R do mês em {pct(fator_r)}, abaixo de {pct(cfg.fator_r_minimo, 0)}: "
            f"pró-labore mínimo seria R$ {brl(minimo)}. Abaixo disso o risco é cair no Anexo V."
        )
    elif fator_r == cfg.fator_r_minimo:
        alertas.append(
            "Fator R exatamente no limite: o Simples usa a média de 12 meses, "
            "então um mês de faturamento maior pode derrubar a média. Considere uma folga."
        )
    if lucros < 0:
        alertas.append("Lucros negativos: pró-labore + DAS + despesas maiores que o faturamento.")
    if entrada.pro_labore > cfg.redutor_isencao_ate:
        alertas.append(
            f"Pró-labore acima de R$ {brl(cfg.redutor_isencao_ate)}: há IRRF, que entra no DARF."
        )

    return Resultado(
        entrada=entrada,
        das=das,
        inss=inss,
        irrf=irrf,
        darf=inss + irrf,
        pro_labore_liquido=pro_labore_liquido,
        lucros=lucros,
        total_pf=pro_labore_liquido + lucros,
        total_impostos=das + inss + irrf,
        fator_r=fator_r,
        alertas=alertas,
    )


def brl(valor: Decimal) -> str:
    """1234.5 → '1.234,50'."""
    return f"{centavos(valor):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def pct(valor: Decimal, casas: int = 2) -> str:
    """0.28 → '28,00%'."""
    return f"{valor:.{casas}%}".replace(".", ",")

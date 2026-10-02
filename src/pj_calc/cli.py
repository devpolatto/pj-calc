"""CLI: pj-calc <faturamento> <pro-labore> [--despesas N] [--aliquota-das 0.06] [--json]."""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation

from pj_calc import __version__
from pj_calc.calc import Entrada, Resultado, brl, calcular, pct
from pj_calc.config import Settings


def valor(texto: str) -> Decimal:
    """Aceita '8704', '8704.00', '8.704,00' e '8704,00'."""
    limpo = texto.strip().replace("R$", "").strip()
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return Decimal(limpo)
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"valor inválido: {texto!r}") from None


def renderizar(r: Resultado, aliquota_das: Decimal) -> str:
    e = r.entrada
    linhas = [
        ("Faturamento", e.faturamento, ""),
        (f"(−) DAS ({pct(aliquota_das)})", r.das, "imposto da empresa"),
        ("(−) Pró-labore bruto", e.pro_labore, f"Fator R {pct(r.fator_r)}"),
        ("    ↳ INSS 11% (DARF)", r.inss, "vai para o governo"),
        ("    ↳ IRRF (DARF)", r.irrf, "vai para o governo"),
        ("    ↳ Pró-labore líquido", r.pro_labore_liquido, "vai para a PF"),
    ]
    if e.outras_despesas:
        linhas.append(("(−) Outras despesas", e.outras_despesas, ""))
    linhas.append(("= Lucros distribuíveis", r.lucros, "vai para a PF"))

    largura = max(len(rotulo) for rotulo, _, _ in linhas)
    saida = [f"{rotulo:<{largura}}  R$ {brl(v):>10}  {nota}".rstrip() for rotulo, v, nota in linhas]
    saida += [
        "",
        f"{'Impostos (DAS + DARF)':<{largura}}  R$ {brl(r.total_impostos):>10}",
        f"{'TRANSFERÍVEL PJ → PF':<{largura}}  R$ {brl(r.total_pf):>10}",
        f"{'  pró-labore líquido':<{largura}}  R$ {brl(r.pro_labore_liquido):>10}",
        f"{'  distribuição de lucros':<{largura}}  R$ {brl(r.lucros):>10}",
    ]
    if r.alertas:
        saida += ["", *(f"⚠ {a}" for a in r.alertas)]
    return "\n".join(saida)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pj-calc",
        description="Quanto da conta PJ (Simples Nacional, Anexo III) pode ir para a conta PF.",
    )
    parser.add_argument("faturamento", type=valor, help="faturamento do mês (ex.: 8704 ou 8.704,00)")
    parser.add_argument("pro_labore", type=valor, help="pró-labore bruto (ex.: 2437,12)")
    parser.add_argument("--despesas", type=valor, default=Decimal("0"),
                        help="outras despesas da PJ no mês (contador, tarifas...)")
    parser.add_argument("--aliquota-das", type=valor, help="alíquota efetiva do DAS (ex.: 0.06)")
    parser.add_argument("--json", action="store_true", help="saída em JSON")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    overrides = {"aliquota_das": args.aliquota_das} if args.aliquota_das is not None else {}
    cfg = Settings(**overrides)

    try:
        entrada = Entrada(
            faturamento=args.faturamento, pro_labore=args.pro_labore, outras_despesas=args.despesas
        )
    except ValueError as erro:
        print(f"pj-calc: entrada inválida: {erro}", file=sys.stderr)
        return 2

    resultado = calcular(entrada, cfg)
    if args.json:
        print(resultado.model_dump_json(indent=2))
    else:
        print(renderizar(resultado, cfg.aliquota_das))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from decimal import Decimal as D

import pytest

from pj_calc.calc import Entrada, brl, calcular, calcular_irrf
from pj_calc.cli import valor
from pj_calc.config import Settings


@pytest.fixture
def cfg() -> Settings:
    return Settings()


def test_simulacao_da_nota(cfg):
    r = calcular(Entrada(faturamento=D("8704.00"), pro_labore=D("2437.12")), cfg)
    assert r.das == D("522.24")
    assert r.inss == D("268.08")
    assert r.irrf == D("0")
    assert r.pro_labore_liquido == D("2169.04")
    assert r.lucros == D("5744.64")
    assert r.total_pf == D("7913.68")
    assert r.total_impostos == D("790.32")


def test_total_pf_e_faturamento_menos_impostos(cfg):
    e = Entrada(faturamento=D("12000"), pro_labore=D("6000"), outras_despesas=D("150"))
    r = calcular(e, cfg)
    assert r.total_pf == e.faturamento - r.das - r.inss - r.irrf - e.outras_despesas


def test_irrf_zero_ate_5000(cfg):
    inss = D("550.00")
    assert calcular_irrf(D("5000.00"), inss, cfg) == D("0")


def test_irrf_faixa_parcial(cfg):
    # 6000 − INSS 660 = 5340 de base → 27,5% − 908,73 = 559,77; redutor 978,62 − 798,87 = 179,75
    assert calcular_irrf(D("6000"), D("660.00"), cfg) == D("380.02")


def test_irrf_sem_redutor_acima_de_7350(cfg):
    inss = D("880.00")  # 8000 × 11%
    assert calcular_irrf(D("8000"), inss, cfg) == D("1049.27")  # 7120 × 27,5% − 908,73


def test_inss_limitado_ao_teto(cfg):
    r = calcular(Entrada(faturamento=D("40000"), pro_labore=D("12000")), cfg)
    assert r.inss == D("932.31")  # 8475,55 × 11%


def test_alerta_fator_r_abaixo(cfg):
    r = calcular(Entrada(faturamento=D("10000"), pro_labore=D("2000")), cfg)
    assert any("Anexo V" in a for a in r.alertas)


def test_alerta_fator_r_no_limite(cfg):
    r = calcular(Entrada(faturamento=D("8704.00"), pro_labore=D("2437.12")), cfg)
    assert any("limite" in a for a in r.alertas)


@pytest.mark.parametrize("texto", ["8704", "8704.00", "8.704,00", "8704,00", "R$ 8.704,00"])
def test_parse_valor(texto):
    assert valor(texto) == D("8704")


def test_brl():
    assert brl(D("7913.68")) == "7.913,68"
    assert brl(D("0")) == "0,00"

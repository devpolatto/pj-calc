"""Parâmetros tributários do pj-calc.

Precedência (da maior para a menor):

1. flags da linha de comando (`--aliquota-das`)
2. variáveis de ambiente `PJ_CALC_*` (ex.: `PJ_CALC_ALIQUOTA_DAS=0.112`)
3. arquivo `~/.config/pj-calc/config.toml`
4. defaults declarados aqui (vigência 2026)

Os valores mudam por lei ou portaria; confira antes de virar o ano.
"""

from __future__ import annotations

import os
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

CONFIG_FILE = (
    Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser() / "pj-calc" / "config.toml"
)


class FaixaIR(BaseModel):
    """Faixa da tabela progressiva mensal do IR: `ate` None = sem teto."""

    ate: Decimal | None
    aliquota: Decimal
    deducao: Decimal


# Tabela progressiva mensal vigente desde maio/2025 (mantida em 2026).
TABELA_IR_PADRAO = [
    FaixaIR(ate=Decimal("2428.80"), aliquota=Decimal("0"), deducao=Decimal("0")),
    FaixaIR(ate=Decimal("2826.65"), aliquota=Decimal("0.075"), deducao=Decimal("182.16")),
    FaixaIR(ate=Decimal("3751.05"), aliquota=Decimal("0.15"), deducao=Decimal("394.16")),
    FaixaIR(ate=Decimal("4664.68"), aliquota=Decimal("0.225"), deducao=Decimal("675.49")),
    FaixaIR(ate=None, aliquota=Decimal("0.275"), deducao=Decimal("908.73")),
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PJ_CALC_", toml_file=CONFIG_FILE)

    # DAS: alíquota efetiva do Simples (1ª faixa do Anexo III = 6%).
    aliquota_das: Decimal = Decimal("0.06")
    # Fator R mínimo para ficar no Anexo III.
    fator_r_minimo: Decimal = Decimal("0.28")

    # INSS do sócio (contribuinte individual) retido do pró-labore, limitado ao teto.
    aliquota_inss: Decimal = Decimal("0.11")
    teto_inss: Decimal = Decimal("8475.55")

    # IRRF: tabela progressiva + desconto simplificado + redutor da Lei 15.270/2025.
    tabela_ir: list[FaixaIR] = TABELA_IR_PADRAO
    desconto_simplificado: Decimal = Decimal("607.20")
    redutor_isencao_ate: Decimal = Decimal("5000.00")
    redutor_maximo: Decimal = Decimal("312.89")
    redutor_parcial_ate: Decimal = Decimal("7350.00")
    redutor_parcial_constante: Decimal = Decimal("978.62")
    redutor_parcial_fator: Decimal = Decimal("0.133145")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, env_settings, TomlConfigSettingsSource(settings_cls))

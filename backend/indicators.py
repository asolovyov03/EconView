from dataclasses import dataclass


@dataclass(frozen=True)
class IndicatorMeta:
    code: str
    name_ru: str
    category: str
    unit: str
    higher_is_better: bool | None = None


INDICATORS: dict[str, IndicatorMeta] = {
    "NY.GDP.MKTP.CD": IndicatorMeta("NY.GDP.MKTP.CD", "ВВП, текущие USD", "economy", "USD", True),
    "NY.GDP.PCAP.CD": IndicatorMeta("NY.GDP.PCAP.CD", "ВВП на душу, USD", "economy", "USD", True),
    "NY.GDP.MKTP.KD.ZG": IndicatorMeta("NY.GDP.MKTP.KD.ZG", "Рост ВВП, %", "economy", "%", True),
    "FP.CPI.TOTL.ZG": IndicatorMeta("FP.CPI.TOTL.ZG", "Инфляция (CPI), %", "economy", "%", False),
    "SL.UEM.TOTL.ZS": IndicatorMeta("SL.UEM.TOTL.ZS", "Безработица, %", "labor", "%", False),
    "SL.TLF.CACT.ZS": IndicatorMeta("SL.TLF.CACT.ZS", "Участие в рабочей силе, %", "labor", "%", True),
    "SP.POP.TOTL": IndicatorMeta("SP.POP.TOTL", "Население", "demography", "people", None),
    "SP.DYN.LE00.IN": IndicatorMeta("SP.DYN.LE00.IN", "Продолжительность жизни", "demography", "years", True),
    "SP.DYN.TFRT.IN": IndicatorMeta("SP.DYN.TFRT.IN", "Суммарный коэффициент рождаемости", "demography", "births/woman", None),
    "SP.URB.TOTL.IN.ZS": IndicatorMeta("SP.URB.TOTL.IN.ZS", "Городское население, %", "demography", "%", None),
    "SE.XPD.TOTL.GD.ZS": IndicatorMeta("SE.XPD.TOTL.GD.ZS", "Расходы на образование, % ВВП", "education", "%", True),
    "SE.ADT.LITR.ZS": IndicatorMeta("SE.ADT.LITR.ZS", "Грамотность взрослых, %", "education", "%", True),
    "SI.POV.GINI": IndicatorMeta("SI.POV.GINI", "Коэффициент Джини", "poverty", "index", False),
    "SI.POV.DDAY": IndicatorMeta("SI.POV.DDAY", "Бедность по $2.15/день, %", "poverty", "%", False),
    "NE.TRD.GNFS.ZS": IndicatorMeta("NE.TRD.GNFS.ZS", "Торговля, % ВВП", "economy", "%", None),
}

CATEGORIES_RU = {
    "economy": "Экономика",
    "labor": "Рынок труда",
    "demography": "Демография",
    "education": "Образование",
    "poverty": "Бедность и неравенство",
}

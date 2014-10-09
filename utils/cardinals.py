#!/usr/bin/env python
# coding: utf-8

CARDINALS = {     0: u'zero',
    1: u'um',     11: u'onze',      10: u'dez',       100: u'cem',
    2: u'dois',   12: u'doze',      20: u'vinte',     200: u'duzentos',
    3: u'três',   13: u'treze',     30: u'trinta',    300: u'trezentos',
    4: u'quatro', 14: u'quatorze',  40: u'quarenta',  400: u'quatrocentos',
    5: u'cinco',  15: u'quinze',    50: u'cinquenta', 500: u'quinhentos',
    6: u'seis',   16: u'dezesseis', 60: u'sessenta',  600: u'seiscentos',
    7: u'sete',   17: u'dezessete', 70: u'setenta',   700: u'setecentos',
    8: u'oito',   18: u'dezoito',   80: u'oitenta',   800: u'oitocentos',
    9: u'nove',   19: u'dezenove',  90: u'noventa',   900: u'novecentos',
}

ORDINALS = {
    10: u'décimo', 100: u'centésimo',
    2:  u'meio',   20: u'vigésimo',      200: u'ducentésimo',
    3:  u'terço',  30: u'trigésimo',     300: u'tricentésimo',
    4:  u'quarto', 40: u'quadragésimo',  400: u'quadringentésimo',
    5:  u'quinto', 50: u'quinquagésimo', 500: u'quingentésimo',
    6:  u'sexto',  60: u'sexagésimo',    600: u'sexcentésimo',
    7:  u'sétimo', 70: u'septuagésimo',  700: u'septingentésimo',
    8:  u'oitavo', 80: u'octogésimo',    800: u'octingentésimo',
    9:  u'nono',   90: u'nonagésimo',    900: u'noningentésimo',
}


def cardinal(n):
    if n in CARDINALS:
        return CARDINALS[n]
    else:
        pot10 = len(str(n))-1
        head, body = divmod(n, 10 ** pot10)
        round = head * 10 ** pot10
        if round == 100:
            prefix = 'cento'
        else:
            prefix = CARDINALS[round]
        return prefix + ' e ' + cardinal(body)


def ordinal(n):
    if n in ORDINALS:
        return ORDINALS[n]
    else:
        return cardinal(n) + ' avos'


def fractional(m, n):
    assert 0 <= n < 1000
    r = cardinal(m)
    s = ordinal(n)
    if m > 1 and not s.endswith('s'):
        s += 's'
    if ' e ' in r and ' ' in s:
        r += ','
    return r + ' ' + s

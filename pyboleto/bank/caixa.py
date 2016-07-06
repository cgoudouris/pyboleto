# -*- coding: utf-8 -*-
from pyboleto.data import BoletoData, CustomProperty


class BoletoCaixa(BoletoData):
    '''
    Gera Dados necessários para criação de boleto para o banco Caixa
    Economica Federal

    '''

    emissao_cliente = None

    nosso_numero_cliente = None

    conta_cedente = CustomProperty('conta_cedente', 6)

    _nosso_numero = CustomProperty('nosso_numero', 15)

    def __init__(self):
        super(BoletoCaixa, self).__init__()

        self.codigo_banco = "104"
        self.local_pagamento = "Preferencialmente nas Casas Lotéricas e \
            Agências da Caixa"
        self.logo_image = "logo_bancocaixa.jpg"

    @property
    def nosso_numero(self):
        if self.nosso_numero_cliente == None or self.emissao_cliente == None:
            raise ValueError("nosso_numero_cliente e emissao_cliente must be set")
        if self.nosso_numero_cliente:
            return self._nosso_numero
        else:
            return ('14' if self.emissao_cliente else '11') + self._nosso_numero

    @nosso_numero.setter
    def nosso_numero(self, n):
        self._nosso_numero = n

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11(self.nosso_numero.split('-')[0], 9, 1)
        digito = 11 - resto2

        if digito == 10 or digito == 11:
            dv = 0
        else:
            dv = digito

        return dv

    @property
    def campo_livre(self):  # 24 digits
        content = "%6s%1s%3s%1s%3s%1s%9s" % (
            self.conta_cedente.split('-')[0],
            self.modulo11(self.conta_cedente.split('-')[0]),
            self.nosso_numero[2:5],
            self.nosso_numero[0:1],
            self.nosso_numero[5:8],
            self.nosso_numero[1:2],
            self.nosso_numero[8:17]
        )
        dv_content = self.modulo11(content)

        return "%24s%1s" % (content, dv_content)

    def format_nosso_numero(self):
        return self.nosso_numero + '-' + str(self.dv_nosso_numero)

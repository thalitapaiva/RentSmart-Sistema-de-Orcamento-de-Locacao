# orcamento.py
# Taxa de contrato, orcamento final e geracao do CSV.

import csv


def formatar_moeda(valor):
    # 1234.5 -> "R$ 1.234,50"
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_numero(valor):
    # usado no CSV (padrao brasileiro, abre direto no Excel)
    return f"{valor:.2f}".replace(".", ",")


class TaxaContratual:
    VALOR_TOTAL = 2000.00
    MAX_PARCELAS = 5

    def __init__(self, parcelas):
        if parcelas < 1 or parcelas > self.MAX_PARCELAS:
            raise ValueError(f"A taxa pode ser parcelada de 1 a {self.MAX_PARCELAS} vezes.")
        self.parcelas = parcelas

    def valor_parcela(self):
        return round(self.VALOR_TOTAL / self.parcelas, 2)

    def parcela_do_mes(self, mes):
        """Quanto da taxa e cobrado no mes informado (1 a 12).
        A ultima parcela ajusta os centavos pra fechar exatamente R$ 2.000,00."""
        if mes > self.parcelas:
            return 0.0
        if mes == self.parcelas:
            return round(self.VALOR_TOTAL - self.valor_parcela() * (self.parcelas - 1), 2)
        return self.valor_parcela()


class Orcamento:
    MESES_PROJECAO = 12

    def __init__(self, imovel, taxa):
        self.imovel = imovel
        self.taxa = taxa

    def aluguel_mensal(self):
        return self.imovel.calcular_aluguel()

    def gerar_projecao(self):
        projecao = []
        for mes in range(1, self.MESES_PROJECAO + 1):
            aluguel = self.aluguel_mensal()
            parcela = self.taxa.parcela_do_mes(mes)
            projecao.append({
                "mes": mes,
                "aluguel": aluguel,
                "parcela_taxa": parcela,
                "total": round(aluguel + parcela, 2),
            })
        return projecao

    def exibir_resumo(self):
        imovel = self.imovel
        print("\n" + "=" * 50)
        print("          RENTSMART - RESUMO DO ORCAMENTO")
        print("=" * 50)
        print(f"Imovel: {imovel.descricao()}")
        print("-" * 50)
        print("ALUGUEL MENSAL")
        print(f"  Aluguel-base{'':.<26}{formatar_moeda(imovel.ALUGUEL_BASE):>12}")
        for descricao, valor in imovel.calcular_adicionais():
            print(f"  + {descricao:.<36}{formatar_moeda(valor):>12}")
        print(f"  Subtotal{'':.<30}{formatar_moeda(imovel.calcular_subtotal()):>12}")
        desconto = imovel.calcular_desconto(imovel.calcular_subtotal())
        if desconto:
            print(f"  - {desconto[0]:.<36}{formatar_moeda(desconto[1]):>12}")
        print(f"  TOTAL MENSAL{'':.<26}{formatar_moeda(self.aluguel_mensal()):>12}")
        print("-" * 50)
        print("TAXA CONTRATUAL (cobrada a parte do aluguel)")
        print(f"  Valor total{'':.<27}{formatar_moeda(self.taxa.VALOR_TOTAL):>12}")
        if self.taxa.parcelas == 1:
            print("  Pagamento: a vista no 1o mes")
        else:
            print(f"  Parcelamento: {self.taxa.parcelas}x de {formatar_moeda(self.taxa.valor_parcela())}")
        print("=" * 50)

    def exportar_csv(self, caminho="projecao_12_meses.csv"):
        projecao = self.gerar_projecao()
        # utf-8-sig e ; para abrir certinho no Excel em portugues
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel (R$)", "Parcela taxa contratual (R$)", "Total do mes (R$)"])
            for linha in projecao:
                escritor.writerow([
                    linha["mes"],
                    formatar_numero(linha["aluguel"]),
                    formatar_numero(linha["parcela_taxa"]),
                    formatar_numero(linha["total"]),
                ])
            total_ano = sum(l["total"] for l in projecao)
            escritor.writerow(["Total 12 meses", "", "", formatar_numero(total_ano)])
        return caminho

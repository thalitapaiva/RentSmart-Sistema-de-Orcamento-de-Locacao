# imoveis.py
# Classes que representam os tipos de imovel da R.M Imoveis.
# Cada imovel sabe calcular o proprio aluguel mensal.


class Imovel:
    """Classe base. As subclasses definem o aluguel-base e as regras especificas."""

    TIPO = "Imovel"
    ALUGUEL_BASE = 0.0

    def calcular_adicionais(self):
        # retorna uma lista de (descricao, valor)
        return []

    def calcular_desconto(self, subtotal):
        # por padrao nao tem desconto; retorna (descricao, valor) ou None
        return None

    def calcular_subtotal(self):
        total_adicionais = sum(valor for _, valor in self.calcular_adicionais())
        return self.ALUGUEL_BASE + total_adicionais

    def calcular_aluguel(self):
        subtotal = self.calcular_subtotal()
        desconto = self.calcular_desconto(subtotal)
        if desconto:
            subtotal -= desconto[1]
        return round(subtotal, 2)

    def descricao(self):
        return self.TIPO


class ImovelComQuartos(Imovel):
    """Casa e apartamento tem regras parecidas (quartos + vaga de garagem),
    entao essa parte fica aqui pra nao repetir codigo."""

    ADICIONAL_SEGUNDO_QUARTO = 0.0
    VALOR_GARAGEM = 300.00

    def __init__(self, quartos, garagem):
        if quartos not in (1, 2):
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.quartos = quartos
        self.garagem = garagem

    def calcular_adicionais(self):
        adicionais = []
        if self.quartos == 2:
            adicionais.append(("Adicional 2 quartos", self.ADICIONAL_SEGUNDO_QUARTO))
        if self.garagem:
            adicionais.append(("Vaga de garagem", self.VALOR_GARAGEM))
        return adicionais

    def descricao(self):
        texto = f"{self.TIPO} - {self.quartos} quarto(s)"
        if self.garagem:
            texto += " com garagem"
        return texto


class Apartamento(ImovelComQuartos):
    TIPO = "Apartamento"
    ALUGUEL_BASE = 700.00
    ADICIONAL_SEGUNDO_QUARTO = 200.00
    PERCENTUAL_DESCONTO = 0.05  # 5% para quem nao tem criancas

    def __init__(self, quartos, garagem, possui_criancas):
        super().__init__(quartos, garagem)
        self.possui_criancas = possui_criancas

    def calcular_desconto(self, subtotal):
        # desconto aplicado depois dos adicionais
        if not self.possui_criancas:
            valor = round(subtotal * self.PERCENTUAL_DESCONTO, 2)
            return ("Desconto 5% (sem criancas)", valor)
        return None


class Casa(ImovelComQuartos):
    TIPO = "Casa"
    ALUGUEL_BASE = 900.00
    ADICIONAL_SEGUNDO_QUARTO = 250.00


class Estudio(Imovel):
    TIPO = "Estudio"
    ALUGUEL_BASE = 1200.00
    VAGAS_PACOTE = 2
    VALOR_PACOTE = 250.00
    VALOR_VAGA_EXTRA = 60.00

    def __init__(self, vagas):
        # 0 = sem estacionamento; se quiser, o minimo e o pacote de 2 vagas
        if vagas != 0 and vagas < self.VAGAS_PACOTE:
            raise ValueError("Para estudio o estacionamento comeca no pacote de 2 vagas.")
        self.vagas = vagas

    def calcular_adicionais(self):
        if self.vagas == 0:
            return []
        adicionais = [("Pacote estacionamento (2 vagas)", self.VALOR_PACOTE)]
        extras = self.vagas - self.VAGAS_PACOTE
        if extras > 0:
            adicionais.append((f"Vagas extras ({extras} x R$ 60,00)", extras * self.VALOR_VAGA_EXTRA))
        return adicionais

    def descricao(self):
        if self.vagas:
            return f"{self.TIPO} com {self.vagas} vaga(s)"
        return f"{self.TIPO} sem estacionamento"

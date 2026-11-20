
from imoveis import Apartamento, Casa, Estudio
from orcamento import Orcamento, TaxaContratual


def ler_inteiro(mensagem, minimo, maximo=None):
    while True:
        entrada = input(mensagem).strip()
        if not entrada.isdigit():
            print("  Digite apenas numeros.")
            continue
        numero = int(entrada)
        if numero < minimo or (maximo is not None and numero > maximo):
            if maximo is None:
                print(f"  Valor minimo: {minimo}.")
            else:
                print(f"  Digite um valor entre {minimo} e {maximo}.")
            continue
        return numero


def ler_sim_nao(mensagem):
    while True:
        resposta = input(mensagem + " (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("  Responda com s ou n.")


def escolher_imovel():
    print("\nTipos de imovel:")
    print("  1 - Apartamento (a partir de R$ 700,00)")
    print("  2 - Casa        (a partir de R$ 900,00)")
    print("  3 - Estudio     (a partir de R$ 1.200,00)")
    tipo = ler_inteiro("Escolha o tipo: ", 1, 3)

    if tipo == 1:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+R$ 300,00)?")
        criancas = ler_sim_nao("Possui criancas?")
        return Apartamento(quartos, garagem, criancas)

    if tipo == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+R$ 300,00)?")
        return Casa(quartos, garagem)

    vagas = 0
    if ler_sim_nao("Deseja estacionamento? (pacote 2 vagas R$ 250,00, extras R$ 60,00 cada)"):
        vagas = ler_inteiro("Quantas vagas no total (minimo 2)? ", 2, 10)
    return Estudio(vagas)


def main():
    print("=" * 50)
    print("     RentSmart - R.M Imoveis")
    print("=" * 50)

    imovel = escolher_imovel()
    parcelas = ler_inteiro("\nEm quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ", 1, 5)
    taxa = TaxaContratual(parcelas)

    orcamento = Orcamento(imovel, taxa)
    orcamento.exibir_resumo()

    arquivo = orcamento.exportar_csv()
    print(f"\nProjecao de 12 meses salva em: {arquivo}")


if __name__ == "__main__":
    main()

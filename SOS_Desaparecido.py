def SosDesaparecido():
    import json
    import os
    from textwrap import indent

    from datetime import datetime

    class ValorInvalidoError(Exception):
        pass

    #Função Cadastro de Desaparecidos
    def cadastrarDesaparecido (p):

        while True:
            try:
                nome = input('Nome da Pessoa Desaparecida:\n-> ').strip()
                if not nome:
                    raise ValueError
                break
            except ValueError:
                print("⚠️ Nome é obrigatório!\n")


        while True:
            try:
                local = (input("\nÚltima localização conhecida:\n-> ")).strip()
                if not local:
                    raise ValueError("Localização é obrigatória!")
                break
            except ValueError as e:
                print("⚠️ Valor inválido! Por favor, digite um número.")
            except ValorInvalidoError:
                print("⚠️ O valor não pode ser negativo ou zero! Digite um valor válido")


        while True:
            try:
                entrada = input('\nData e hora aproximada do desaparecimento (Formato: DD/MM/AAAA HH:MM)::\n-> ').strip()
                tempo = datetime.strptime(entrada, "%d/%m/%Y %H:%M")
                break
            except ValueError:
                print("⚠️ Formato inválido! Use o padrão: DD/MM/AAAA HH:MM.")

        descricao = input("\n Descrição/Aparência da pessoa:\n-> ").strip()
        contato = input("\n Telefone para contato (opcional):\n-> ").strip()

        desaparecido = {
            "Nome": nome,
            "Local_ultimo_visto": local,
            "Tempo _desaparecido": tempo.strftime("%d/%m/%Y %H:%M"),  # salva como string
            "Descricao": descricao,
            "Contato": contato
        }

        print("\n✅ Relato registrado com sucesso.")
        p.append(desaparecido)

    #Lista para armazenar dados
    desaparecidos = []

    print("📢 Sistema SOS - Cadastro de Pessoa Desaparecida\n")

    #Cadastro minimo de 1 desaparecido
    cadastrarDesaparecido(desaparecidos)

    #Loop para cadastrar mais
    while input("\nDeseja cadastrar outro caso de desaparecido? [S/N]\n-> ").strip().upper() in ["S", "SIM"]:
        cadastrarDesaparecido(desaparecidos)

    #Nome do arquivo
    arquivo = "sos_desaparecidos.json"

    #Verifica se já existe conteúdo anterior
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            try:
                dados_anteriores = json.load(f)
            except json.JSONDecodeError:
                dados_anteriores = []
    else:
        dados_anteriores = []

    #Junta dados antigos e novos
    dados_anteriores.extend(desaparecidos)

    #Salva JSON
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_anteriores, f, indent=4, ensure_ascii=False)

    print("\n Dados salvos em 'sos_desaparecidos.json'")
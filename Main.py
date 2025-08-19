from SOS_Desaparecido import SosDesaparecido
from PrevisãoRisco import gs_function

def main_menu():
    print("🛡️ Bem Vindo ao programa SafeZone\n")
    
    while True:
        print("\nEscolha o número da funcionalidade desejada:")
        resposta = input("1 - Previsão de risco climático\n"
                         "2 - Pedido SOS Desaparecido\n"
                         "3 - Sair\n"
                         "-> ").strip()
        
        if resposta == "1":
            gs_function()  # Esta função agora deve conter toda a lógica diretamente
        elif resposta == "2":
            SosDesaparecido()
        elif resposta == "3":
            print("Encerrando o programa, obrigado pela participação")
            break
        else:
            print("Opção inválida! Por favor, escolha 1, 2 ou 3.")

if __name__ == "__main__":
    main_menu()
#---- Importação de Bibliotecas ----
import requests
import pandas as pd
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
import os

def gs_function():
    # --- 1. Dados Simulados ---
    dados = pd.DataFrame({
        'chuva_mm': [0, 5, 15, 30, 60, 90, 120, 70, 25, 0],
        'umidade': [45, 50, 65, 70, 85, 95, 98, 92, 75, 60],
        'vento_kmh': [5, 8, 12, 20, 30, 40, 35, 22, 18, 7],
        'relato_alagamento': [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
        'relato_rachadura': [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        'risco': [0, 0, 0, 1, 1, 1, 1, 1, 0, 0]
    })

    X = dados.drop('risco', axis=1)
    y = dados['risco']

    modelo_base = DecisionTreeClassifier()
    modelo = CalibratedClassifierCV(modelo_base, cv=3)
    modelo.fit(X, y)

    # --- Função para validar respostas 'S' ou 'N' ---
    def pergunta_sim_nao(pergunta):
        while True:
            resposta = input(f"{pergunta} (s/n): ").strip().lower()
            if resposta in ['s', 'n']:
                return resposta
            print("❌ Resposta inválida! Digite 's' para sim ou 'n' para não.")

    # --- Salvar resultado no .JSON ---
    def salvar_resultado_json(entrada, risco, prob, cidade):
        resultado = {
            "cidade": cidade,
            "chuva_mm": float(entrada['chuva_mm'].values[0]),
            "umidade": int(entrada['umidade'].values[0]),
            "vento_kmh": float(entrada['vento_kmh'].values[0]),
            "relato_alagamento": int(entrada['relato_alagamento'].values[0]),
            "relato_rachadura": int(entrada['relato_rachadura'].values[0]),
            "risco": int(risco),
            "probabilidade": float(round(prob * 100, 2))
        }

        arquivo_resultados = "resultados_previsao.json"

        dados_atuais = []
        if os.path.exists(arquivo_resultados):
            with open(arquivo_resultados, "r", encoding="utf-8") as f:
                dados_atuais = json.load(f)

        dados_atuais.append(resultado)

        with open(arquivo_resultados, "w", encoding="utf-8") as f:
            json.dump(dados_atuais, f, ensure_ascii=False, indent=4)

    # --- Programa Principal ---
    print("🌍  Bem-vindo ao Sistema de Previsão de Risco de Eventos Extremos!\n")

    while True:
        cidade = input("🏙️  Digite o nome da cidade (ou 'sair' para encerrar): ").strip()
        if cidade.lower() == "sair":
            print("👋 Encerrando o programa. Até a próxima!")
            break

        api_key = "9b6a9d5c707f6d5843009b01f5ed7a8e" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"

        resposta = requests.get(url)
        dados_clima = resposta.json()

        if resposta.status_code != 200 or "main" not in dados_clima:
            print(f"⚠️ Erro ao obter dados do clima para '{cidade}'. Mensagem: {dados_clima.get('message', 'Desconhecida')}\n")
            continue

        umidade = dados_clima["main"]["humidity"]
        vento = dados_clima["wind"]["speed"] * 3.6  # m/s para km/h
        chuva = dados_clima.get("rain", {}).get("1h", 0)

        print(f"\n📡 Dados do tempo em {cidade.capitalize()}:")
        print(f"   🌧️ Chuva: {chuva} mm")
        print(f"   💧 Umidade: {umidade}%")
        print(f"   🌬️ Vento: {vento:.1f} km/h\n")

        alagamento = pergunta_sim_nao("\n👀 Você observou alagamento?")
        rachadura = pergunta_sim_nao("🧱 Você observou rachaduras em muros ou solo?")

        entrada = pd.DataFrame([{
            'chuva_mm': chuva,
            'umidade': umidade,
            'vento_kmh': vento,
            'relato_alagamento': 1 if alagamento == "s" else 0,
            'relato_rachadura': 1 if rachadura == "s" else 0
        }])

        risco = modelo.predict(entrada)[0]
        prob = modelo.predict_proba(entrada)[0][1]

# ---- Resultado em probabilidade do evento climatico ---
        print("📊 Previsão de risco:")
        if prob >= 0.7:
            print(f"🚨 RISCO ALTO! Probabilidade de evento extremo: {prob*100:.2f}%\n")
            print("🔔 Medidas Preventivas:\n")
            print("- Evacuar da área IMEDIATAMENTE se estiver em zona de risco\n"
                    "- Ir para ponto de abrigo seguro definido pela Defesa Civil\n"
                    "- Desligar energia elétrica e o gás da residência antes de sair\n"
                    "- Manter comunicação com familiares e vizinhos\n")
        elif prob >= 0.4:
            print(f"⚠️ Risco Moderado. Probabilidade: {prob*100:.2f}%\n")
            print("🔔 Medidas Preventivas:\n")
            print("- Evite deslocamento desnecessário especialmente em áreas de risco (margens de rios, encostas, etc )\n"
                    "- Garantir que todos da casa saibam como agir em uma evacução\n")
        else:
            print(f"✅ Risco Baixo. Probabilidade: {prob*100:.2f}%\n")
            print("🔔 Medidas Preventivas:\n")
            print("- Fique atento a mudança de clima\n"
                    "- Verifique rotas de evacuação e pontos de abrigo\n")

        salvar_resultado_json(entrada, risco, prob, cidade)
import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from collections import defaultdict, Counter

def emoji_clima(descricao):
    descricao = descricao.lower()
    if "chuva" in descricao:
        return "🌧️"
    elif "nuvem" in descricao:
        return "☁️"
    elif "céu limpo" in descricao:
        return "☀️"
    elif "neve" in descricao:
        return "❄️"
    elif "tempestade" in descricao:
        return "⛈️"
    else:
        return "🌤️"

def obter_clima(event=None):
    for widget in previsao_frame.winfo_children():
        widget.destroy()

    cidade = entrada_cidade.get().strip()
    if not cidade:
        messagebox.showwarning("Atenção", "Digite o nome de uma cidade.")
        return

    cidade_formatada = cidade.replace(" ", "+")
    chave_api = "b52249fafac669c7db276e7f0ac8762b"
    url_atual = f"http://api.openweathermap.org/data/2.5/weather?q={cidade_formatada}&appid={chave_api}&lang=pt_br&units=metric"
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade_formatada}&appid={chave_api}&lang=pt_br&units=metric"

    try:
        resposta_atual = requests.get(url_atual)
        if resposta_atual.status_code == 200:
            dados = resposta_atual.json()
            temp = dados["main"]["temp"]
            descricao = dados["weather"][0]["description"]
            sensacao = dados["main"]["feels_like"]
            umidade = dados["main"]["humidity"]
            emoji = emoji_clima(descricao)

            texto_atual.config(text=(
                f"{emoji} {cidade.title()}\n"
                f"🌡️ {temp}°C  | 🤔 Sensação: {sensacao}°C\n"
                f"💧 Umidade: {umidade}% | {descricao}"
            ))
        else:
            texto_atual.config(text="❌ Erro ao buscar clima atual.")
            return

        resposta_forecast = requests.get(url_forecast)
        if resposta_forecast.status_code == 200:
            dados_forecast = resposta_forecast.json()
            dias = defaultdict(list)

            for item in dados_forecast["list"]:
                data_txt = item["dt_txt"]
                dia = data_txt.split()[0]
                temp = item["main"]["temp"]
                descricao = item["weather"][0]["description"]
                dias[dia].append((temp, descricao))

            dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            count = 0
            for dia, valores in dias.items():
                if count >= 5:
                    break
                temperaturas = [v[0] for v in valores]
                descricoes = [v[1] for v in valores]
                media = sum(temperaturas) / len(temperaturas)
                desc_mais_comum = Counter(descricoes).most_common(1)[0][0]
                emoji = emoji_clima(desc_mais_comum)

                data_obj = datetime.strptime(dia, "%Y-%m-%d")
                dia_semana = dias_semana[data_obj.weekday()]
                dia_formatado = f"{dia_semana} - {data_obj.strftime('%d/%m')}"

                bg_cor = "#ffffff"
                if "☀️" in emoji:
                    bg_cor = "#fff8dc"
                elif "☁️" in emoji:
                    bg_cor = "#e0e0e0"
                elif "🌧️" in emoji:
                    bg_cor = "#d0ecff"
                elif "⛈️" in emoji:
                    bg_cor = "#e6d8ff"
                elif "❄️" in emoji:
                    bg_cor = "#e6f8ff"

                card = tk.Frame(previsao_frame, bg=bg_cor, bd=1, relief="solid")
                card.pack(pady=5, padx=10, fill="x")

                tk.Label(card, text=dia_formatado, bg=bg_cor, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10)
                tk.Label(card, text=f"{emoji} {media:.1f}°C - {desc_mais_comum}", bg=bg_cor, font=("Segoe UI", 11)).pack(anchor="w", padx=10, pady=(0, 5))

                count += 1
        else:
            texto_atual.config(text="❌ Erro ao buscar previsão.")
    except Exception as e:
        texto_atual.config(text="Erro ao acessar API.")
        print(e)

# Interface
janela = tk.Tk()
janela.title("🌤️ Clima e Previsão")
janela.geometry("460x600")
janela.configure(bg="#f2f2f2")
janela.resizable(False, False)

tk.Label(janela, text="Cidade:", font=("Segoe UI", 12), bg="#f2f2f2").pack(pady=(15, 5))
entrada_cidade = tk.Entry(janela, font=("Segoe UI", 12), width=30)
entrada_cidade.pack()
entrada_cidade.bind("<Return>", obter_clima)

tk.Button(
    janela,
    text="Buscar Clima",
    font=("Segoe UI", 12, "bold"),
    bg="#007acc",
    fg="white",
    activebackground="#005f99",
    cursor="hand2",
    command=obter_clima
).pack(pady=10)

texto_atual = tk.Label(janela, text="", font=("Segoe UI", 12), bg="#f2f2f2", justify="center")
texto_atual.pack(pady=10)

previsao_frame = tk.Frame(janela, bg="#f2f2f2")
previsao_frame.pack(fill="both", expand=True)

janela.mainloop()

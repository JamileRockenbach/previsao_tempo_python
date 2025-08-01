import requests
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import messagebox

def buscar_previsao():
    cidade = entrada_cidade.get().strip()
    estado = entrada_estado.get().strip().upper()

    if not cidade or not estado:
        messagebox.showinfo("Info", "Digite o nome da cidade e a sigla do estado (ex: SP, RJ).")
        return
    
    estados = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo",
    "SE": "Sergipe", "TO": "Tocantins"
}
    
    nome_estado = estados.get(estado)
    if not nome_estado:
        messagebox.showerror("Erro", "Sigla de estado inválida.")
        return

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=10&language=pt&format=json"
        geo_resposta = requests.get(geo_url).json()

        resultado_geo = None
        for item in geo_resposta["results"]:
            if "admin1" in item and item["admin1"].lower() == nome_estado.lower():
                resultado_geo = item
                break

        if not resultado_geo:
            resultado.config(text="Não encontramos essa cidade nesse estado.")
            return

        latitude = resultado_geo["latitude"]
        longitude = resultado_geo["longitude"]

        clima_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,weathercode&timezone=auto"
        )
        clima_resposta = requests.get(clima_url).json()
        dados = clima_resposta["current"]
        temperatura = dados["temperature_2m"]
        umidade = dados["relative_humidity_2m"]
        codigo_clima = dados["weathercode"]
        descricao_clima = interpretar_codigo_clima(codigo_clima)

        resultado.config(
            text=(
                f"Cidade: {cidade.title()} - {estado}\n"
                f"Temperatura: {temperatura}°C\n"
                f"Umidade: {umidade}%\n"
                f"Clima: {descricao_clima}")
        )

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar previsão: {str(e)}")

def interpretar_codigo_clima(codigo):
    mapa = {
        0: "Céu limpo", 1: "Parcialmente nublado", 2: "Nublado", 3: "Encoberto",
        45: "Névoa", 48: "Névoa com gelo", 51: "Garoa leve", 53: "Garoa moderada",
        55: "Garoa densa", 61: "Chuva leve", 63: "Chuva moderada", 65: "Chuva forte",
        80: "Pancadas leves", 81: "Pancadas moderadas", 82: "Pancadas fortes"
    }
    return mapa.get(codigo, "Desconhecido")

janela = tk.Tk()
janela.title("Previsão do Tempo")
janela.geometry("700x400")
janela.iconbitmap("assets/icone_sol.ico")
janela.resizable(False, False)
fundo_img = Image.open("assets/fundoo.jpeg").resize((700, 400))
fundo_tk = ImageTk.PhotoImage(fundo_img)
label_fundo = tk.Label(janela, image=fundo_tk)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

titulo = tk.Label(janela, text="Previsão do Tempo", font=("Segoe UI", 17, "bold"), bg="#b8d8ff", fg="#2c2c2c")
titulo.pack(pady=15)

label_estado = tk.Label(janela, text="Digite seu estado (sigla, ex: SP):", font=("Segoe UI", 11), bg="#b8d8ff")
label_estado.pack()
entrada_estado = tk.Entry(janela, font=("Segoe UI", 12), width=25)
entrada_estado.pack(pady=5)

label_cidade = tk.Label(janela, text="Digite sua cidade:", font=("Segoe UI", 11), bg="#b8d8ff")
label_cidade.pack()
entrada_cidade = tk.Entry(janela, font=("Segoe UI", 12), width=25)
entrada_cidade.pack(pady=5)

btn_buscar = tk.Button(janela, text="Buscar Previsão", command=buscar_previsao, font=("Segoe UI", 11), bg="#4a90e2", fg="white")
btn_buscar.pack(pady=10)

resultado = tk.Label(janela, text="", font=("Segoe UI", 11), bg="#b8d8ff", justify="left")
resultado.pack(pady=12)

rodape = tk.Label(janela, text="Projeto de estudo em Python com dados reais e foco visual.", font=("Segoe UI", 9), bg="#b8d8ff", fg="gray25")
rodape.pack(side=tk.BOTTOM, pady=8)

janela.mainloop()
import tkinter as tk
from tkinter import ttk
import threading
import speedtest

def measure_speed():
    def update_ui():
        try:
            download_label.config(text="Testando velocidade de download...")
            st = speedtest.Speedtest()
            st.get_servers([52170])

            def download_thread():
                st.download()
                nonlocal download_speed
                download_speed = st.results.download / 10 ** 6
                update_download_label(download_speed)

            download_speed = None

            def update_download_label(speed):
                download_label.config(text=f"DOWNLOAD: {speed:.2f} Mbps")

            download_thread = threading.Thread(target=download_thread)
            download_thread.start()

            download_thread.join(timeout=3)

            if download_thread.is_alive():
                download_thread.join()

            if download_speed is None:
                download_label.config(text="Tempo limite excedido")
            else:
                download_label.config(text=f"DOWNLOAD: {download_speed:.2f} Mbps")

            upload_label.config(text="Testando velocidade de upload...")
            st.upload()  # Inicia o teste de upload
            upload_speed = st.results.upload / 10 ** 6  # Convertendo para Megabits
            upload_label.config(text=f"UPLOAD: {upload_speed:.2f} Mbps")

            ping_label.config(text="Testando ping...")
            ping = st.results.ping
            ping_label.config(text=f"PING: {ping} ms")
        except Exception as e:
            download_label.config(text="Erro ao testar velocidade.")
            upload_label.config(text="")
            ping_label.config(text=str(e))
        finally:
            start_button.config(state="active")

    start_button.config(state="disabled")
    download_label.config(text="")
    upload_label.config(text="")
    ping_label.config(text="")

    speed_thread = threading.Thread(target=update_ui)
    speed_thread.start()

window = tk.Tk()
window.title("TESTE DE VELOCIDADE")
window.geometry("870x250")
window.configure(bg="black")
result_font = ("Helvetica", 18)
window.resizable(False, False)

speed = ttk.Label(window, text="SPEED TEST", background="black", foreground="white", font=result_font)
test = ttk.Label(window, text="Teste de velocidade para sua conexão ADSL, VDSL, cabo, fibra ou satélite.",
                 background="black", foreground="white", font=result_font)
speed.pack()
test.pack()

style = ttk.Style()
style.configure("Snow.TButton", background="snow", font=("Helvetica", 16), borderwidth=5, relief="solid",
                borderradius=10)
start_button = ttk.Button(window, text="Iniciar Teste", command=measure_speed, style="Snow.TButton")
start_button.pack(pady=10)

download_label = ttk.Label(window, text="", background="black", foreground="white", font=result_font)
download_label.pack()
upload_label = ttk.Label(window, text="", background="black", foreground="white", font=result_font)
upload_label.pack()
ping_label = ttk.Label(window, text="", background="black", foreground="white", font=result_font)
ping_label.pack()

# Defina o ícone da janela
window.iconbitmap('./assets/speed.ico')

window.mainloop()

import datetime
import os
import socket
import sys
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk

from PIL import ImageDraw, ImageFont, ImageGrab, ImageTk


def graba():
    global directorio_base, directorio, intervalo, grabando

    grabando = True
    while grabando:
        nombre_equipo = socket.gethostname()
        momento_captura = (
            nombre_equipo + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        momento_archivo = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        nombre_archivo = f"captura-{momento_archivo}.png"
        texto_en_captura = momento_captura
        ruta_completa = os.path.join(directorio, nombre_archivo)
        captura = ImageGrab.grab(
            bbox=None, include_layered_windows=False, all_screens=True
        )
        dibujo = ImageDraw.Draw(captura)
        try:
            fuente = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            fuente = ImageFont.load_default()  # Si no encuentra la fuente
        posicion = (50, 50)
        color = (255, 0, 0)
        dibujo.text(posicion, texto_en_captura, fill=color, font=fuente)
        os.makedirs(directorio_base, exist_ok=True)
        os.makedirs(directorio, exist_ok=True)
        captura.save(ruta_completa)
        time.sleep(intervalo)


def lista():
    global directorio_base, directorio

    os.makedirs(directorio_base, exist_ok=True)
    os.makedirs(directorio, exist_ok=True)
    momento_listado = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    path = os.path.abspath(
        os.path.join(directorio, "listado-" + momento_listado + ".txt")
    )
    elementos = os.listdir(directorio)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Listado del directorio: {directorio}\n")
        f.write("=" * 80 + "\n")
        with os.scandir(directorio) as elementos:
            for entrada in elementos:
                if entrada.is_file():
                    try:
                        infor = entrada.stat()
                        tamano = infor.st_size
                        fecha_mod = datetime.datetime.fromtimestamp(infor.st_mtime)
                        f.write(
                            f"{entrada.name}  {tamano}   {fecha_mod.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        )
                    except Exception as e:
                        f.write(f"No se pudo leer {entrada.name}: {e}\n\n")
                elif entrada.is_dir():
                    f.write(f"{entrada.name}/\n\n")


def funcion_1():
    global info, ventana

    dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

    # path = os.path.abspath(os.path.join(dir, "img/circulo-rojo-128.png"))
    # icono = ImageTk.PhotoImage(file=path)
    # ventana.iconphoto(True, icono)

    path = os.path.abspath(os.path.join(dir, "img/circulo-rojo.ico"))
    ventana.after(201, lambda: ventana.iconbitmap(path))

    info.config(text="🔴 Grabando...", fg="red")

    hilo = threading.Thread(target=graba, daemon=True)
    hilo.start()


def funcion_2():
    global grabando, info, ventana

    dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

    # path = os.path.abspath(os.path.join(dir, "img/circulo-rojo-128.png"))
    # icono = ImageTk.PhotoImage(file=path)
    # ventana.iconphoto(True, icono)

    path = os.path.abspath(os.path.join(dir, "img/circulo-negro.ico"))
    ventana.after(201, lambda: ventana.iconbitmap(path))

    info.config(text="⚫ Inactivo", fg="black")

    hilo = threading.Thread(target=lista, daemon=True)
    hilo.start()

    grabando = False


def abrir_enlace(event):
    webbrowser.open("https://mclibre.org/")


def abrir_acerca_de():
    # Crear ventana "Acerca de"
    acerca = tk.Toplevel(ventana)
    acerca.title("Acerca de...")
    acerca.geometry("300x130")

    # Contenido
    # etiqueta = ttk.Label(
    #     acerca,
    #     text="mclibre Screenshots\nVersión 0.7\n(c) 2025 Bartolomé Sintes Marco\nhttps://mclibre.org",
    #     justify="center",
    # )
    # etiqueta.pack(expand=True, pady=20)

    # boton_cerrar = ttk.Button(acerca, text="Cerrar", command=acerca.destroy)
    # boton_cerrar.pack(pady=10)

    # Texto seleccionable
    texto_info = (
        "mclibre Capturas\nVersión 0.10 (2026.02.13)\n(c) 2026 Bartolomé Sintes Marco\n"
    )

    caja_texto = tk.Text(
        acerca,
        width=40,
        height=4,
        wrap="word",
        borderwidth=0,
        background=acerca.cget("background"),
    )
    caja_texto.pack(padx=10, pady=(10, 0))
    caja_texto.insert("1.0", texto_info)
    caja_texto.config(state="disabled")

    # ---- ENLACE CLICABLE ----
    enlace = tk.Label(
        acerca,
        text="https://mclibre.org/",
        fg="blue",
        cursor="hand2",
        font=("Arial", 10, "underline"),
    )
    enlace.pack(after=caja_texto)
    enlace.bind("<Button-1>", abrir_enlace)

    # Botón cerrar
    ttk.Button(acerca, text="Cerrar", command=acerca.destroy).pack(after=enlace)


def main():
    global directorio_base, directorio, intervalo, grabando, info, ventana

    intervalo = 30
    directorio_base = "C:/tmp/capturas"
    directorio = "C:/tmp/capturas/" + datetime.datetime.now().strftime(
        "%Y-%m-%d-%H-%M-%S"
    )
    # directorio = "/home/tu_usuario/mis_archivos"
    grabando = True

    os.makedirs(directorio_base, exist_ok=True)
    os.makedirs(directorio, exist_ok=True)

    ventana = tk.Tk()
    ventana.title("Capturador de pantalla")
    ventana.geometry("300x200")

    menu_bar = tk.Menu(ventana)
    menu_ayuda = tk.Menu(menu_bar, tearoff=0)
    menu_ayuda.add_command(label="Acerca de...", command=abrir_acerca_de)
    menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
    ventana.config(menu=menu_bar)

    dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    path = os.path.abspath(os.path.join(dir, "img/circulo-negro.ico"))
    ventana.after(201, lambda: ventana.iconbitmap(path))

    info = tk.Label(ventana, text="⚫ Inactivo", font=("Arial", 14), fg="black")
    info.pack(pady=15)

    boton1 = tk.Button(ventana, text="Grabar", command=funcion_1, width=20)
    boton2 = tk.Button(ventana, text="Detener", command=funcion_2, width=20)

    boton1.pack(pady=10)
    boton2.pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    main()

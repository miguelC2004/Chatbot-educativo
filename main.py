import random
import wikipediaapi
from sympy import *
import tkinter as tk
from tkinter import font, messagebox

# Inicializar la instancia de Wikipedia
wiki = wikipediaapi.Wikipedia('es')

# Lista de preguntas y respuestas predefinidas
preguntas = {
    "Hola": ["¡Hola!", "Hola, ¿cómo puedo ayudarte?"],
    "¿Cómo estás?": ["Estoy bien, gracias por preguntar.", "¡Estoy genial!", "Me siento fantástico."],
    "¿Cuál es tu nombre?": ["Puedes llamarme ChatBot.", "Mi nombre es ChatBot, ¿en qué puedo ayudarte?"],
    "Adiós": ["¡Hasta luego!", "¡Que tengas un buen día!"],
    "¿Qué tiempo hace hoy?": ["Hoy hace buen tiempo.", "Está soleado y agradable hoy."],
    "Cuéntame un chiste": ["¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.", "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"],
    "": ["Perdón, no entendí la pregunta. ¿Podrías reformularla?"]
}

# Función para obtener una respuesta a partir de una pregunta
def obtener_respuesta(pregunta):
    if pregunta in preguntas:
        return random.choice(preguntas[pregunta])
    elif es_ecuacion_valida(pregunta):
        return resolver_ecuacion(pregunta)
    else:
        return buscar_en_wikipedia(pregunta)

# Función para verificar si la entrada es una ecuación válida
def es_ecuacion_valida(ecuacion):
    try:
        parse_expr(ecuacion)
        return True
    except:
        return False

# Función para buscar información en Wikipedia
def buscar_en_wikipedia(consulta):
    page = wiki.page(consulta)
    if page.exists():
        return page.summary[:500] + "..."
    else:
        return "No encontré información sobre eso en Wikipedia."

# Función para resolver ecuaciones matemáticas
def resolver_ecuacion(ecuacion):
    x = symbols('x')
    try:
        soluciones = solve(parse_expr(ecuacion), x)
        resultado = ""
        for solucion in soluciones:
            resultado += "x = " + str(solucion) + "\n"
        return resultado
    except:
        return "No pude resolver la ecuación."

# Función para mostrar la respuesta completa del chatbot
def ver_respuesta_completa():
    respuesta_completa = salida.get("1.0", tk.END)
    messagebox.showinfo("Respuesta Completa", respuesta_completa)

# Función para manejar la entrada del usuario
def procesar_entrada():
    pregunta = entrada.get()
    respuesta = obtener_respuesta(pregunta)
    salida.config(state=tk.NORMAL)
    salida.insert(tk.END, "Tú: " + pregunta + "\n")
    salida.insert(tk.END, "ChatBot: " + respuesta + "\n\n")
    salida.config(state=tk.DISABLED)
    entrada.delete(0, tk.END)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("ChatBot")
ventana.geometry("500x400")
ventana.configure(bg="#F4F4F4")

# Crear fuente personalizada
font_style = font.Font(family="Helvetica", size=12)

# Crear elementos de la interfaz
frame_salida = tk.Frame(ventana, bg="#F4F4F4")
salida = tk.Text(frame_salida, width=60, height=15, font=font_style)
salida.config(state=tk.DISABLED)
salida.pack(side=tk.LEFT, fill=tk.BOTH)
frame_salida.pack(pady=20)

frame_entrada = tk.Frame(ventana, bg="#F4F4F4")
etiqueta = tk.Label(frame_entrada, text="Pregunta:", bg="#F4F4F4", font=font_style)
etiqueta.pack(side=tk.LEFT)
entrada = tk.Entry(frame_entrada, width=40, font=font_style)
entrada.bind("<Return>", lambda event: procesar_entrada())
entrada.pack(side=tk.LEFT)
frame_entrada.pack(pady=10)

frame_botones = tk.Frame(ventana, bg="#F4F4F4")
boton_enviar = tk.Button(frame_botones, text="Enviar", command=procesar_entrada, font=font_style, bg="#4CAF50", fg="white",
                         activebackground="#45A049", activeforeground="white")
boton_enviar.pack(side=tk.LEFT, padx=5)

boton_respuesta_completa = tk.Button(frame_botones, text="Respuesta Completa", command=ver_respuesta_completa,
                                    font=font_style, bg="#1976D2", fg="white", activebackground="#1565C0",
                                    activeforeground="white")
boton_respuesta_completa.pack(side=tk.LEFT, padx=5)

frame_botones.pack(pady=10)

# Loop principal de la ventana
ventana.mainloop()

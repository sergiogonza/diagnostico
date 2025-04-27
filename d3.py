import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO

# Función para enviar el PDF por email
def enviar_pdf_por_email(pdf_filename, email_contacto):
    from_email = "tu_correo@gmail.com"  # Reemplaza con tu correo
    to_email = email_contacto  # Correo del contacto al que se le enviará el PDF
    subject = "Diagnóstico Tecnológico Empresarial"  # Asunto del correo
    body = "Adjunto encontrarás el diagnóstico tecnológico de tu empresa en formato PDF."

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(body)

    # Abrir el archivo PDF y adjuntarlo al correo
    with open(pdf_filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={pdf_filename}")
        msg.attach(part)

    # Asegurarse de que el correo se envíe correctamente con codificación UTF-8
    try:
        # Conectar al servidor SMTP de Gmail (puedes cambiarlo si usas otro servicio)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, "tu_contraseña")  # Reemplaza con tu contraseña
        msg = msg.as_string().encode('utf-8')  # Asegurar que el mensaje está en UTF-8
        server.sendmail(from_email, to_email, msg)
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Fase 1: Recolección de respuestas y generación de gráfico
# Preguntas iniciales
sector_economico = st.selectbox("Sector Económico", [
    "Tecnología / Startups",
    "Servicios Financieros",
    "Comercio Minorista",
    "Manufactura / Industrial",
    "Salud y Bienestar",
    "Educación",
    "Gobierno / Sector Público",
    "Agroindustria",
    "Turismo y Hospitalidad"
])

eslabon_cadena = st.selectbox("Eslabón de la cadena", [
    "Productor de Materias Primas / Suministros",
    "Proveedor de Materias Primas/ Intermediarios",
    "Fabricante/ Transformador",
    "Comercializador / Intermediario",
    "Prestador de servicios Complementarios",
    "Prestador de servicios de soporte y apoyo a la industria"
])

num_empleados = st.selectbox("Número de empleados", ["10 o menos", "11 a 50", "51 a 200", "Más de 200"])
nombre_contacto = st.text_input("Nombre contacto que diligencia")
email_contacto = st.text_input("e-mail contacto que diligencia")
telefono_contacto = st.text_input("Teléfono de contacto (prefijo + número de teléfono)")

# Preguntas para la fase 1
preguntas = [
    "¿Cuentan con hardware y software actualizados y compatibles con sus procesos?",
    "¿Tienen procesos críticos automatizados con herramientas digitales?",
    "¿Centralizan, analizan y respaldan sus datos estratégicos de forma eficiente?",
    "¿Tienen sitio web activo, redes sociales, herramientas colaborativas, CRM u otros sistemas?",
    "¿Tienen políticas de seguridad, copias de respaldo y control de accesos?",
    "¿El equipo domina herramientas digitales necesarias para su rol?",
    "¿Usan dashboards, IA generativa, ERPs, BI u otras herramientas analíticas?",
    "¿Desarrollan o adaptan soluciones tecnológicas propias o personalizadas?"
]

# Recolección de respuestas de los usuarios
respuestas = []
for pregunta in preguntas:
    respuesta = st.slider(pregunta, min_value=1, max_value=5)  # Se obtiene una valoración de 1 a 5
    respuestas.append(respuesta)

# Generar estrategia y sugerencia estratégica para cada respuesta
estrategias = []
sugerencias = []

for respuesta in respuestas:
    if respuesta == 1:
        estrategias.append("Requiere atención urgente")
        sugerencias.append("Fomentar la capacitación y actualizar la infraestructura")
    elif respuesta == 2:
        estrategias.append("Nivel bajo, pero puede mejorar")
        sugerencias.append("Iniciar planes de optimización de procesos")
    elif respuesta == 3:
        estrategias.append("Nivel moderado de avance")
        sugerencias.append("Continuar con la integración de tecnología en el proceso")
    elif respuesta == 4:
        estrategias.append("Buena implementación tecnológica")
        sugerencias.append("Consolidar la infraestructura digital")
    else:
        estrategias.append("Excelente nivel tecnológico")
        sugerencias.append("Aprovechar para expandir y diversificar aún más la digitalización")

# Determinar el nivel actual de la empresa según las respuestas
nivel_actual = []
for respuesta in respuestas:
    if respuesta < 1:
        nivel_actual.append("Data Null")
    elif respuesta < 3:
        nivel_actual.append("Nivel Bajo (Alerta)")
    elif respuesta < 5:
        nivel_actual.append("Nivel Medio (Base Estable)")
    else:
        nivel_actual.append("Nivel Alto (Competitividad Digital)")

# Mostrar los resultados y las sugerencias en la app de Streamlit
for i, (pregunta, estrategia, sugerencia, nivel) in enumerate(zip(preguntas, estrategias, sugerencias, nivel_actual)):
    st.write(f"Pregunta {i+1}: {pregunta}")
    st.write(f"Estrategia: {estrategia}")
    st.write(f"Sugerencia: {sugerencia}")
    st.write(f"Nivel Actual: {nivel}")
    st.write("\n")

# Fase 2: Recolección de valoraciones por área evaluada
areas_evaluadas = [
    "Infraestructura Tecnológica",
    "Automatización de Procesos",
    "Gestión de Información y Datos",
    "Presencia y Herramientas Digitales",
    "Seguridad de la Información",
    "Capacidades Digitales del Equipo",
    "Uso de Inteligencia Artificial y Analítica",
    "Innovación Tecnológica Aplicada"
]

# Recolección de respuestas para cada área
valoraciones = []
for area in areas_evaluadas:
    impacto = st.slider(f"{area} - Impacto en Eficiencia y Competitividad", 1, 5)
    riesgo = st.slider(f"{area} - Riesgo Operativo Actual", 1, 5)
    facilidad = st.slider(f"{area} - Facilidad de Implementación", 1, 5)
    valoraciones.append((impacto, riesgo, facilidad))

# Calcular la prioridad recomendada y el significado estratégico
prioridades = []
estrategias_areas = []
for impacto, riesgo, facilidad, area in zip([v[0] for v in valoraciones], 
                                             [v[1] for v in valoraciones], 
                                             [v[2] for v in valoraciones], 
                                             areas_evaluadas):
    if impacto >= 4 and riesgo >= 4:
        prioridad = "Alta Prioridad"
        estrategia = "Área crítica: alto impacto y riesgo + posibilidad real de intervención"
    elif impacto >= 3 and riesgo >= 3:
        prioridad = "Media Prioridad"
        estrategia = "Área importante, pero puede esperar frente a otras más urgentes"
    else:
        prioridad = "Baja Prioridad"
        estrategia = "Área menos crítica, puede esperar intervenciones más urgentes"
    
    prioridades.append(prioridad)
    estrategias_areas.append(estrategia)

# Mostrar los resultados de la fase 2
for i, (area, (impacto, riesgo, facilidad), prioridad, estrategia) in enumerate(zip(areas_evaluadas, valoraciones, prioridades, estrategias_areas)):
    st.write(f"Área Evaluada {i+1}: {area}")
    st.write(f"Impacto en Eficiencia y Competitividad: {impacto}")
    st.write(f"Riesgo Operativo Actual: {riesgo}")
    st.write(f"Facilidad de Implementación: {facilidad}")
    st.write(f"Prioridad Recomendada: {prioridad}")
    st.write(f"Significado Estratégico: {estrategia}")
    st.write("\n")

# Generar el gráfico de 8 lados con conexiones basado en las valoraciones
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
angles = np.linspace(0, 2 * np.pi, 8, endpoint=False).tolist()
# Usamos la primera valoración del área evaluada para generar un gráfico
values = [v[0] for v in valoraciones]  # Usar el impacto como valor para cada área
values += values[:1]  # Cerrar el gráfico, añadiendo el primer valor al final de los valores

# Asegúrate de que 'angles' y 'values' tengan la misma longitud
angles += [angles[0]]  # Añadir el primer ángulo al final de los ángulos

ax.fill(angles, values, color='blue', alpha=0.25)
ax.plot(angles, values, color='blue', linewidth=2)

ax.set_yticklabels([])  # No mostrar las etiquetas en el eje Y
ax.set_xticks(angles[:-1])  # Marcar los ángulos
ax.set_xticklabels(areas_evaluadas, rotation=45, ha="right")

st.pyplot(fig)

# Generar un archivo PDF con los resultados de la fase 2
def generar_pdf_fase2(pdf_filename, valoraciones, prioridades, estrategias_areas):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    y_position = 750
    c.drawString(100, y_position, "Diagnóstico Tecnológico Empresarial - Fase 2")
    y_position -= 20
    for i, (area, (impacto, riesgo, facilidad), prioridad, estrategia) in enumerate(zip(areas_evaluadas, valoraciones, prioridades, estrategias_areas)):
        c.drawString(100, y_position, f"Área {i+1}: {area}")
        y_position -= 20
        c.drawString(100, y_position, f"Impacto: {impacto}, Riesgo: {riesgo}, Facilidad: {facilidad}")
        y_position -= 20
        c.drawString(100, y_position, f"Prioridad: {prioridad}")
        y_position -= 20
        c.drawString(100, y_position, f"Estrategia: {estrategia}")
        y_position -= 40
    c.save()

# Generar el PDF en memoria (sin guardarlo en disco)
def generar_pdf_memoria(valoraciones, prioridades, estrategias_areas):
    pdf_buffer = BytesIO()
    generar_pdf_fase2(pdf_buffer, valoraciones, prioridades, estrategias_areas)
    pdf_buffer.seek(0)
    return pdf_buffer

# Crear el botón de descarga en Streamlit
pdf_memoria = generar_pdf_memoria(valoraciones, prioridades, estrategias_areas)
st.download_button(
    label="Descargar PDF",
    data=pdf_memoria,
    file_name="diagnostico_estrategico.pdf",
    mime="application/pdf"
)

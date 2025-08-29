# inJobFinder 🔎💼

Automatiza la búsqueda de prácticas en LinkedIn y filtra las ofertas usando IA ⚡.
Este proyecto extrae ofertas de empleo, las guarda en un CSV y las evalúa con ChatGPT (GPT-3.5 Turbo) dándoles una nota del 1 al 5 según criterios predefinidos (reputación de empresa, rol, tecnologías, etc.).


## 🚀 ¿Qué hace?
	1.	Se loguea automáticamente en LinkedIn.
	2.	Navega a la sección de empleos y extrae las ofertas disponibles.
	3.	Procesa y guarda la información en un CSV.
	4.	Evalúa cada oferta con la API de OpenAI, asignando una puntuación del 1 al 5.
	5.	Devuelve un dataset donde es fácil identificar las mejores ofertas para aplicar.



## 🛠️ Tecnologías usadas
	•	Python 3
	•	Selenium → automatización web
	•	Pandas → gestión de datos
	•	OpenAI API → evaluación inteligente con GPT-3.5 Turbo
	•	dotenv → gestión de variables de entorno



## ⚙️ Configuración

### Clona el repositorio:

git clone https://github.com/saanchoo/inJobFinder.git
cd inJobFinder

### Instala las dependencias:

pip install -r requirements.txt



## 🔑 Variables de entorno

Crea un archivo .env en la raíz del proyecto con tus credenciales:

LINKEDIN_USER=tu_correo@ejemplo.com
LINKEDIN_PASS=tu_contraseña

OPENAI_API_KEY=tu_api_key

GPT_PROMPT=“Eres un asistente que ayuda a evaluar ofertas de prácticas de software. Evalúa del 1 al 5 cada oferta de trabajo (5 = mejor) en función de su encaje con un perfil junior, valorando reputación de la empresa, rol relacionado con software y tecnologías relevantes. Sé muy crítico: un 5 es difícil de conseguir.”



## ▶️ Ejecución

Lanza el script principal:

python main.py

Esto abrirá LinkedIn, extraerá las ofertas, las evaluará y guardará un archivo CSV con los resultados.



## 📂 Salida

Los resultados se guardan en jobs_data.csv, incluyendo:
	•	Título de la oferta
	•	Empresa
	•	Ubicación
	•	Link
	•	Descripción
	•	Nota (1-5)



## 🚧 Estado del proyecto

Este es un proyecto base y funcional, pero con mucho potencial para crecer.
En el futuro se podrían añadir:
	•	Notificaciones automáticas (ej. WhatsApp o email) con las mejores ofertas.
	•	Filtros más avanzados (por tecnologías, salario, tipo de contrato).
	•	Dashboard visual con gráficas.



## 🤝 Contribuciones

Si quieres mejorar el proyecto, ¡haz un fork y propón tus cambios! 🙌



## 📜 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo y modificarlo libremente.

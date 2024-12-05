# Discord-Inspector
Discord-Inspector es una herramienta de OSINT que permite recopilar información mediante el uso de la ID en Discord. Utilizando diferentes APIs, relacionados con perfiles, servidores, o aplicaciones (Bots) a partir de su ID. Esta herramienta puede ser utilizada para obtener detalles públicos, con fines de análisis o investigaciones.

## Funciones principales
Usuario (ID): Permite obtener diversos datos asociados a un usuario a través de su ID. Entre la información disponible se incluyen su nickname global, el color del banner/perfil, la fecha de creación de la cuenta, los emblemas y otros datos relacionados.

Servidor (ID): Permite obtener información sobre un servidor siempre que este tenga activado el widget del servidor. Si el widget no está habilitado, se mostrará un mensaje de error. Algunos de los datos disponibles son: nombre del servidor, fecha de creación, URL de invitación (si está disponible), usuarios activos, entre otros.

Aplicación/BOT (ID): Permite obtener datos sobre un bot en Discord. La información puede variar dependiendo del bot, pero generalmente incluye detalles como la monetización, verificación, visibilidad pública, entre otros. Además, se proporcionan los datos en formato raw (sin procesar) en un archivo JSON. También se incluye la búsqueda mediante la herramienta Discordlookup en la web.

## Instalacion

Clonar repositorio.
```
git clone https://github.com/Euronymou5/Discord-Inspector
```

Instalar dependencias.
```
pip install -r requirements.txt
```

Iniciar script.
```
python main.py
```

## Imagenes

|  Usuario |  Servidor | BOT  |
| ------------ | ------------ | ------------ |
| ![image](https://github.com/user-attachments/assets/4e19bd87-68d7-49a8-a95d-4d396b7e9dc3)  | ![image](https://github.com/user-attachments/assets/bad8a023-530d-41d9-81d4-5d82619e9329) | ![image](https://github.com/user-attachments/assets/7e1e93b0-35e4-4c96-b4a1-8d7189b9758b) |

## 🌐 Contacto 🌐
[![discord](https://img.shields.io/badge/Discord-euronymou5-a?style=plastic&logo=discord&logoColor=white&labelColor=black&color=7289DA)](https://discord.com/users/452720652500205579)

![email](https://img.shields.io/badge/ProtonMail-mr.euron%40proton.me-a?style=plastic&logo=protonmail&logoColor=white&labelColor=black&color=8B89CC)

[![X](https://img.shields.io/twitter/follow/Euronymou51?style=plastic&logo=X&label=%40Euronymou51&labelColor=%23000000&color=%23000000)](https://x.com/Euronymou51)

# -*- coding: utf-8 -*-
# Discord Inspector By: Euronymou5
# https://github.com/Euronymou5

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication
import sys
import requests
from tkinter import messagebox
from datetime import datetime
import threading
from bs4 import BeautifulSoup
import webbrowser

app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
MainWindow.setObjectName("MainWindow")
MainWindow.setWindowIcon(QIcon('icons/favicon.ico'))
MainWindow.resize(622, 368)
MainWindow.setMinimumSize(622, 368)
MainWindow.setMaximumSize(622, 368)
MainWindow.setStyleSheet("background-color: rgb(49, 51, 56);")

centralwidget = QtWidgets.QWidget(MainWindow)
centralwidget.setObjectName("centralwidget")

tabWidget = QtWidgets.QTabWidget(centralwidget)
tabWidget.setGeometry(QtCore.QRect(5, 92, 611, 271))
tabWidget.setObjectName("tabWidget")

tab = QtWidgets.QWidget()
tab.setEnabled(True)
tab.setObjectName("tab")

fondo_franem = QtWidgets.QFrame(tab)
fondo_franem.setGeometry(QtCore.QRect(0, 0, 611, 261))
fondo_franem.setStyleSheet("background-color: rgb(43, 45, 49);")
fondo_franem.setFrameShape(QtWidgets.QFrame.StyledPanel)
fondo_franem.setFrameShadow(QtWidgets.QFrame.Raised)
fondo_franem.setObjectName("fondo_franem")

id_label = QtWidgets.QLabel(fondo_franem)
id_label.setGeometry(QtCore.QRect(36, 20, 51, 20))
id_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 75 10pt \"Gill Sans MT\";")
id_label.setAlignment(QtCore.Qt.AlignCenter)
id_label.setObjectName("id_label")

lineEdit = QtWidgets.QLineEdit(fondo_franem)
lineEdit.setGeometry(QtCore.QRect(10, 40, 111, 21))
lineEdit.setStyleSheet("color: rgb(200, 200, 200);")
lineEdit.setClearButtonEnabled(True)
lineEdit.setObjectName("lineEdit")

def buscar_func():
    global datos
    id = lineEdit.text()
    jsondata_entry.clear()
    datos = []
    r = requests.get(f'https://discordlookup.mesalytic.moe/v1/user/{id}')
    var = r.json()

    if var.get('message') == 'Value is not a valid Discord snowflake':
       messagebox.showerror('Discord Inspector', 'Error: la id no es correcta.')
       # Quitar los demas widgets, si se ha hecho una busqueda antes del error.
       try:
        username_label.setText('')
        globalname.setText('')
        userid_label.setText('')
        banner_color_label.setText('')
        color_label.setText('')
        creadoen_label_2.setText('')
        creadoen_label.setVisible(False)
        copiar_btn.setVisible(False)
        userimage.setPixmap(QPixmap())
       except:
        pass
    else:
      username_label.setText(var["global_name"])
      globalname.setText(f'@{var["username"]}')
      userid_label.setText(var["id"])
      banner_color_label.setText(f'Banner: {var["raw"]["banner_color"]}')
      color_label.setText(f'Color de perfil: {var["banner"]["color"]}')

      fecha_dt = datetime.strptime(var["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
      fecha_n = fecha_dt.strftime("%d %B %Y, %H:%M:%S")

      # Agregar datos a la lista 'datos'
      datos.append('\n'.join([
        f'Nombre global: {var["global_name"]}',
        f'Nickname: {var["username"]}',
        f'ID: {var["id"]}',
        f'Color del banner: {var["raw"]["banner_color"]}',
        f'Color de perfil: {var["banner"]["color"]}',
        f'Fecha de creacion: {fecha_n}'
      ]))

      creadoen_label_2.setText(fecha_n)
      creadoen_label.setVisible(True)
      jsondata_entry.appendPlainText(str(var))
      copiar_btn.setVisible(True)

      # Descargar imagen del usuario
      response = requests.get(var["avatar"]["link"])
      if response.status_code == 200:
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        if not pixmap.isNull():
          userimage.setPixmap(pixmap)
          userimage.setScaledContents(True)

def hilo():
  th = threading.Thread(target=buscar_func)
  th.start()

buscaruser_btn = QtWidgets.QPushButton(fondo_franem)
buscaruser_btn.setGeometry(QtCore.QRect(10, 80, 121, 31))
buscaruser_btn.setObjectName("buscaruser_btn")
buscaruser_btn.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 11pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
buscaruser_btn.clicked.connect(hilo)

frame_2 = QtWidgets.QFrame(fondo_franem)
frame_2.setGeometry(QtCore.QRect(0, 130, 614, 3))
frame_2.setStyleSheet("background-color: rgb(63, 65, 71);")
frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
frame_2.setLineWidth(1)
frame_2.setMidLineWidth(0)
frame_2.setObjectName("frame_2")

userimage = QtWidgets.QLabel(fondo_franem)
userimage.setGeometry(QtCore.QRect(10, 140, 41, 41))
userimage.setObjectName("userimage")

username_label = QtWidgets.QLabel(fondo_franem)
username_label.setGeometry(QtCore.QRect(60, 140, 151, 16))
username_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 11pt \"Gill Sans MT\";")
username_label.setObjectName("username_label")

globalname = QtWidgets.QLabel(fondo_franem)
globalname.setGeometry(QtCore.QRect(60, 158, 101, 16))
globalname.setStyleSheet("color: rgb(255, 255, 255);\n""font: 9pt \"Gill Sans MT\";")
globalname.setObjectName("globalname")

def copiar_func():
  for data in datos:
    clipboard = QApplication.clipboard()
    clipboard.setText(data)
  messagebox.showinfo('Discord Inspector', 'Copiado al portapapeles.')

copiar_btn = QtWidgets.QPushButton(fondo_franem)
copiar_btn.setGeometry(QtCore.QRect(10, 205, 171, 31))
copiar_btn.setObjectName("copiar_btn")
copiar_btn.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 11pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
copiar_btn.setText("Copiar datos")
copiar_btn.setVisible(False)
copiar_btn.clicked.connect(copiar_func)
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icons/clip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
copiar_btn.setIcon(icon)
copiar_btn.setIconSize(QtCore.QSize(22, 22))

userid_label = QtWidgets.QLabel(fondo_franem)
userid_label.setGeometry(QtCore.QRect(60, 175, 111, 16))
userid_label.setStyleSheet("color: rgb(181, 181, 181);\n"
"font: 9pt \"Gill Sans MT\";")
userid_label.setObjectName("userid_label")

jsondata_entry = QtWidgets.QPlainTextEdit(fondo_franem)
jsondata_entry.setGeometry(QtCore.QRect(390, 10, 212, 231))
jsondata_entry.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 8pt \"Arial\";")
jsondata_entry.setReadOnly(True)
jsondata_entry.setObjectName("jsondata_entry")
jsondata_label = QtWidgets.QLabel(fondo_franem)
jsondata_label.setGeometry(QtCore.QRect(230, 30, 141, 71))
jsondata_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Gill Sans MT\";")
jsondata_label.setAlignment(QtCore.Qt.AlignCenter)
jsondata_label.setObjectName("jsondata_label")

creadoen_label = QtWidgets.QLabel(fondo_franem)
creadoen_label.setGeometry(QtCore.QRect(195, 185, 51, 21))
creadoen_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Gill Sans MT\";")
creadoen_label.setObjectName("creadoen_label")
creadoen_label.setVisible(False)

creadoen_label_2 = QtWidgets.QLabel(fondo_franem)
creadoen_label_2.setObjectName(u"creadoen_label_2")
creadoen_label_2.setGeometry(QtCore.QRect(250, 186, 131, 21))
creadoen_label_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 7pt \"Arial\";")

bot_label = QtWidgets.QLabel(fondo_franem)
bot_label.setGeometry(QtCore.QRect(220, 215, 121, 16))
bot_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Gill Sans MT\";")
bot_label.setObjectName("bot_label")

banner_color_label = QtWidgets.QLabel(fondo_franem)
banner_color_label.setGeometry(QtCore.QRect(195, 140, 161, 16))
banner_color_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Gill Sans MT\";")
banner_color_label.setObjectName("banner_color_label")

color_label = QtWidgets.QLabel(fondo_franem)
color_label.setGeometry(QtCore.QRect(195, 164, 161, 16))
color_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Gill Sans MT\";")
color_label.setObjectName("color_label")

tabWidget.addTab(tab, "")
tab_3 = QtWidgets.QWidget()
tab_3.setObjectName("tab_3")

def buscar_sv_func():
    global datos_sv
    global sv_id

    sv_id = entry_server_id.text()
    jsondata_entry_2.clear()
    datos_sv = []

    # Peticion a api externa de discord
    r = requests.get(f'https://discordlookup.mesalytic.moe/v1/guild/{sv_id}')
    var = r.json()

    # Peticion a discordlookup
    ss = requests.get(f'https://discordlookup.com/guild/{sv_id}')
    texto = ss.content
    soup = BeautifulSoup(texto, 'html.parser')

    # Peticion a canary.discord.com/api
    inf = requests.get(f'https://canary.discord.com/api/v10/guilds/{sv_id}/widget.json')
    ll = inf.json()

    if var.get('message') == 'Value is not a valid Discord snowflake':
       messagebox.showerror('Discord Inspector', 'Error: la id no es correcta.')
       # Quitar los demas widgets, si se ha hecho una busqueda antes del error.
       try:
        nombre_label.setVisible(False)
        codigo_inv_label.setVisible(False)
        busqueda_btn.setVisible(False)
        users_online_label.setVisible(False)
        fechacreacion_label.setVisible(False)
        copiar_inf_sv_btn.setVisible(False)
       except:
        pass
    elif var.get('error') == 'The guild is either non-existant, unavailable, or has Server Widget/Discovery disabled.':
       messagebox.showerror('Discord Inspector', 'Error: El servidor no existe, no está disponible o tiene el widget del servidor deshabilitado.')
       # Quitar los demas widgets, si se ha hecho una busqueda antes del error.
       try:
        nombre_label.setVisible(False)
        codigo_inv_label.setVisible(False)
        busqueda_btn.setVisible(False)
        users_online_label.setVisible(False)
        fechacreacion_label.setVisible(False)
        copiar_inf_sv_btn.setVisible(False)
       except:
        pass
    # Busqueda
    else:
      busqueda_btn.setVisible(True)
      copiar_inf_sv_btn.setVisible(True)
      
      nombre_label.setText(f'Nombre: {var["name"]}')
      codigo_inv_label.setText(f'URL de invitacion: {var["instant_invite"]}')
      users_online_label.setText(f"Usuarios activos: " + str(var['presence_count']))
      jsondata_entry_2.appendPlainText(str(var))
      jsondata_entry_2.appendPlainText(f'\n*Informacion de discord.com/api*\n\n' + str(ll))

      etiquetas_p = soup.find_all('p')
      for p in etiquetas_p:
        link = p.find('a', href=lambda href: href and "timestamp" in href)
        if link:
          ey = link.text
          fechacreacion_label.setText(f"Fecha de creacion: {ey.strip()}")

      # Agregar datos a la lista 'datos_sv'
      datos_sv.append('\n'.join([
        f'Nombre del servidor: {var["name"]}',
        f'URL de invitacion: {var["instant_invite"]}',
        f'Usuarios activos: {var["presence_count"]}',
        f'Fecha de creacion: {ey.strip()}',
      ]))

def copiar_func_sv():
  for data in datos_sv:
    clipboard = QApplication.clipboard()
    clipboard.setText(data)
  messagebox.showinfo('Discord Inspector', 'Copiado al portapapeles.')

fondo_franem_2 = QtWidgets.QFrame(tab_3)
fondo_franem_2.setGeometry(QtCore.QRect(0, 0, 611, 261))
fondo_franem_2.setStyleSheet("background-color: rgb(43, 45, 49);")
fondo_franem_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
fondo_franem_2.setFrameShadow(QtWidgets.QFrame.Raised)
fondo_franem_2.setObjectName("fondo_franem_2")

tabWidget.addTab(tab_3, "")
tab_2 = QtWidgets.QWidget()
tab_2.setObjectName("tab_2")

fondo_franem_3 = QtWidgets.QFrame(tab_2)
fondo_franem_3.setGeometry(QtCore.QRect(0, 0, 611, 261))
fondo_franem_3.setStyleSheet("background-color: rgb(43, 45, 49);")
fondo_franem_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
fondo_franem_3.setFrameShadow(QtWidgets.QFrame.Raised)
fondo_franem_3.setObjectName("fondo_franem_3")
tabWidget.addTab(tab_2, "")

titulo_label = QtWidgets.QLabel(centralwidget)
titulo_label.setGeometry(QtCore.QRect(145, 0, 331, 61))
titulo_label.setStyleSheet("color: rgb(88, 101, 242);\n"
"font: 20pt \"Impact\";")
titulo_label.setAlignment(QtCore.Qt.AlignCenter)
titulo_label.setObjectName("titulo_label")

frame = QtWidgets.QFrame(centralwidget)
frame.setGeometry(QtCore.QRect(0, 80, 641, 3))
frame.setStyleSheet("background-color: rgb(63, 65, 71);")
frame.setFrameShape(QtWidgets.QFrame.NoFrame)
frame.setFrameShadow(QtWidgets.QFrame.Plain)
frame.setLineWidth(1)
frame.setMidLineWidth(0)
frame.setObjectName("frame")

titulo_label_2 = QtWidgets.QLabel(centralwidget)
titulo_label_2.setGeometry(QtCore.QRect(250, 48, 111, 20))
titulo_label_2.setStyleSheet("color: rgb(219, 222, 225);\n"
"font: 10pt \"Impact\";")
titulo_label_2.setAlignment(QtCore.Qt.AlignCenter)
titulo_label_2.setObjectName("titulo_label_2")
MainWindow.setCentralWidget(centralwidget)

nota_label = QtWidgets.QLabel(fondo_franem_2)
nota_label.setGeometry(QtCore.QRect(6, 10, 341, 20))
nota_label.setStyleSheet("color: rgb(179, 179, 179);\n""font: 75 10pt \"Gill Sans MT\";")
nota_label.setAlignment(QtCore.Qt.AlignCenter)
nota_label.setObjectName("nota_label")
nota_label.setText("Nota: el servidor debe tener habilitado el widget de servidor.")

server_id_label = QtWidgets.QLabel(fondo_franem_2)
server_id_label.setGeometry(QtCore.QRect(36, 40, 51, 20))
server_id_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 75 10pt \"Gill Sans MT\";")
server_id_label.setAlignment(QtCore.Qt.AlignCenter)
server_id_label.setObjectName("server_id_label")
server_id_label.setText("ID")

entry_server_id = QtWidgets.QLineEdit(fondo_franem_2)
entry_server_id.setGeometry(QtCore.QRect(10, 60, 111, 21))
entry_server_id.setStyleSheet("color: rgb(200, 200, 200);")
entry_server_id.setClearButtonEnabled(True)
entry_server_id.setObjectName("entry_server_id")

def buscar_sv_hilo():
  th = threading.Thread(target=buscar_sv_func)
  th.start()

buscar_sv_btn = QtWidgets.QPushButton(fondo_franem_2)
buscar_sv_btn.setGeometry(QtCore.QRect(10, 95, 121, 31))
buscar_sv_btn.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 11pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
buscar_sv_btn.setObjectName("buscar_sv_btn")
buscar_sv_btn.setText("Buscar")
buscar_sv_btn.clicked.connect(buscar_sv_hilo)

nombre_label = QtWidgets.QLabel(fondo_franem_2)
nombre_label.setGeometry(QtCore.QRect(7, 155, 361, 16))
nombre_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 11pt \"Gill Sans MT\";")
nombre_label.setObjectName("nombre_label")

jsondata_label_2 = QtWidgets.QLabel(fondo_franem_2)
jsondata_label_2.setGeometry(QtCore.QRect(430, 0, 141, 31))
jsondata_label_2.setStyleSheet("color: rgb(255, 255, 255);\n""font: 75 12pt \"Gill Sans MT\";")
jsondata_label_2.setAlignment(QtCore.Qt.AlignCenter)
jsondata_label_2.setObjectName("jsondata_label_2")
jsondata_label_2.setText("Informacion de la API:")

jsondata_entry_2 = QtWidgets.QPlainTextEdit(fondo_franem_2)
jsondata_entry_2.setGeometry(QtCore.QRect(400, 30, 201, 111))
jsondata_entry_2.setStyleSheet("color: rgb(255, 255, 255);\n""font: 8pt \"Arial\";")
jsondata_entry_2.setReadOnly(True)
jsondata_entry_2.setObjectName("jsondata_entry_2")

frame_3 = QtWidgets.QFrame(fondo_franem_2)
frame_3.setGeometry(QtCore.QRect(0, 145, 605, 3))
frame_3.setStyleSheet("background-color: rgb(63, 65, 71);")
frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
frame_3.setLineWidth(1)
frame_3.setMidLineWidth(0)
frame_3.setObjectName("frame_3")

fechacreacion_label = QtWidgets.QLabel(fondo_franem_2)
fechacreacion_label.setGeometry(QtCore.QRect(7, 175, 331, 16))
fechacreacion_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 11pt \"Gill Sans MT\";")
fechacreacion_label.setObjectName("fechacreacion_label")

codigo_inv_label = QtWidgets.QLabel(fondo_franem_2)
codigo_inv_label.setGeometry(QtCore.QRect(7, 195, 411, 16))
codigo_inv_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 11pt \"Gill Sans MT\";")
codigo_inv_label.setObjectName("codigo_inv_label")

users_online_label = QtWidgets.QLabel(fondo_franem_2)
users_online_label.setGeometry(QtCore.QRect(7, 215, 351, 16))
users_online_label.setStyleSheet("color: rgb(255, 255, 255);\n""font: 11pt \"Gill Sans MT\";")
users_online_label.setObjectName("users_online_label")

busqueda_btn = QtWidgets.QPushButton(fondo_franem_2)
busqueda_btn.setGeometry(QtCore.QRect(410, 204, 191, 31))
busqueda_btn.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 10pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icons/lup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
busqueda_btn.setIcon(icon)
busqueda_btn.setIconSize(QtCore.QSize(22, 22))
busqueda_btn.setObjectName("busqueda_btn")
busqueda_btn.setText("Busqueda con discordlookup")
busqueda_btn.clicked.connect(lambda: webbrowser.open(f'https://discordlookup.com/guild/{sv_id}'))
busqueda_btn.setVisible(False)

copiar_inf_sv_btn = QtWidgets.QPushButton(fondo_franem_2)
copiar_inf_sv_btn.setGeometry(QtCore.QRect(410, 168, 191, 31))
copiar_inf_sv_btn.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 10pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icons/clip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
copiar_inf_sv_btn.setIcon(icon)
copiar_inf_sv_btn.setIconSize(QtCore.QSize(22, 22))
copiar_inf_sv_btn.setObjectName("copiar_inf_sv_btn")
copiar_inf_sv_btn.setText("Copiar Datos")
copiar_inf_sv_btn.clicked.connect(copiar_func_sv)
copiar_inf_sv_btn.setVisible(False)

# BOT ID WIDGETS

def bot_info_func():
    global datos_bot
    global bot_id

    bot_id = entry_bot_id.text()
    descripcion_entry.clear()
    jsondata_entry_3.clear()
    datos_bot = []

    # Peticion a api externa de discord
    r = requests.get(f'https://discordlookup.mesalytic.moe/v1/application/{bot_id}')
    var = r.json()

    if var.get('message') == 'Value is not a valid Discord snowflake':
       messagebox.showerror('Discord Inspector', 'Error: la id no es correcta.')
       # Quitar los demas widgets, si se ha hecho una busqueda antes del error.
       try:
        username_bot_label.setVisible(False)
        monetizacion_label.setVisible(False)
        verify_label.setVisible(False)
        public_label.setVisible(False)
        botimage.setVisible(False)
        descripcion_entry.setVisible(False)
        descripcion_label.setVisible(False)
        copiarinf_btn_bot.setVisible(False)
        busqueda_btn_bot.setVisible(False)
       except:
        pass
    else:
      busqueda_btn_bot.setVisible(True)
      copiarinf_btn_bot.setVisible(True)
      descripcion_entry.setVisible(True)
      descripcion_label.setVisible(True)

      username_bot_label.setText(var["name"])
      if var["is_monetized"] == True:
        monetizacion_label.setText('Monetizacion: Si')
      else:
        monetizacion_label.setText('Monetizacion: No')
      if var["is_verified"] == True:
        verify_label.setText("Verificado: Si")
      else:
        verify_label.setText("Verificado: No")
      if var["bot_public"] == True:
        public_label.setText("Publico: Si")
      else:
        public_label.setText("Publico: No")

      descripcion_entry.appendPlainText(str(var["description"]))
      jsondata_entry_3.appendPlainText(str(var))

      # Descargar imagen
      response = requests.get(var["icon"])
      if response.status_code == 200:
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        if not pixmap.isNull():
          botimage.setPixmap(pixmap)
          botimage.setScaledContents(True)

      # Agregar datos a la lista 'datos_bot'
      datos_bot.append('\n'.join([
        f'{var["name"]}',
        f'Monetizacion: {var["is_monetized"]}',
        f'Verificado: {var["is_verified"]}',
        f'Publico: {var["bot_public"]}',
      ]))

def copiar_func_bot():
  for data in datos_bot:
    clipboard = QApplication.clipboard()
    clipboard.setText(data)
  messagebox.showinfo('Discord Inspector', 'Copiado al portapapeles.')

id_label_bot = QtWidgets.QLabel(fondo_franem_3)
id_label_bot.setGeometry(QtCore.QRect(36, 20, 51, 20))
id_label_bot.setStyleSheet("color: rgb(255, 255, 255);\n""font: 75 10pt \"Gill Sans MT\";")
id_label_bot.setAlignment(QtCore.Qt.AlignCenter)
id_label_bot.setObjectName("id_label_bot")
id_label_bot.setText("ID")

entry_bot_id = QtWidgets.QLineEdit(fondo_franem_3)
entry_bot_id.setGeometry(QtCore.QRect(10, 40, 111, 21))
entry_bot_id.setStyleSheet("color: rgb(200, 200, 200);")
entry_bot_id.setClearButtonEnabled(True)
entry_bot_id.setObjectName("lineEdit")

def hilo_bot():
  th = threading.Thread(target=bot_info_func)
  th.start()

buscaruser_btn_2 = QtWidgets.QPushButton(fondo_franem_3)
buscaruser_btn_2.setGeometry(QtCore.QRect(10, 80, 121, 31))
buscaruser_btn_2.setObjectName("buscaruser_btn_2")
buscaruser_btn_2.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 11pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
buscaruser_btn_2.setText("Buscar")
buscaruser_btn_2.clicked.connect(hilo_bot)

frame_4 = QtWidgets.QFrame(fondo_franem_3)
frame_4.setGeometry(QtCore.QRect(0, 130, 614, 3))
frame_4.setStyleSheet("background-color: rgb(63, 65, 71);")
frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
frame_4.setLineWidth(1)
frame_4.setMidLineWidth(0)
frame_4.setObjectName("frame_4")

botimage = QtWidgets.QLabel(fondo_franem_3)
botimage.setGeometry(QtCore.QRect(10, 140, 41, 41))
botimage.setObjectName("userimage")

username_bot_label = QtWidgets.QLabel(fondo_franem_3)
username_bot_label.setGeometry(QtCore.QRect(60, 140, 281, 16))
username_bot_label.setStyleSheet("color: rgb(255, 255, 255);\n""background-color: rgb(43, 45, 49);\n""font: 11pt \"Gill Sans MT\";")
username_bot_label.setObjectName("username_bot_label")

monetizacion_label = QtWidgets.QLabel(fondo_franem_3)
monetizacion_label.setGeometry(QtCore.QRect(60, 157, 191, 16))
monetizacion_label.setStyleSheet("color: rgb(255, 255, 255);\n""background-color: rgb(43, 45, 49);\n""font: 11pt \"Gill Sans MT\";")
monetizacion_label.setObjectName("monetizacion_label")

verify_label = QtWidgets.QLabel(fondo_franem_3)
verify_label.setGeometry(QtCore.QRect(60, 175, 191, 16))
verify_label.setStyleSheet("color: rgb(255, 255, 255);\n""background-color: rgb(43, 45, 49);\n""font: 11pt \"Gill Sans MT\";")
verify_label.setObjectName("verify_label")

public_label = QtWidgets.QLabel(fondo_franem_3)
public_label.setGeometry(QtCore.QRect(60, 192, 191, 16))
public_label.setStyleSheet("color: rgb(255, 255, 255);\n""background-color: rgb(43, 45, 49);\n""font: 11pt \"Gill Sans MT\";")
public_label.setObjectName("public_label")

descripcion_entry = QtWidgets.QPlainTextEdit(fondo_franem_3)
descripcion_entry.setGeometry(QtCore.QRect(190, 60, 151, 61))
descripcion_entry.setStyleSheet("color: rgb(255, 255, 255);\n""font: 8pt \"Arial\";")
descripcion_entry.setReadOnly(True)
descripcion_entry.setVisible(False)
descripcion_entry.setObjectName("descripcion_entry")

descripcion_label = QtWidgets.QLabel(fondo_franem_3)
descripcion_label.setGeometry(QtCore.QRect(220, 30, 81, 16))
descripcion_label.setStyleSheet("color: rgb(255, 255, 255);\n""background-color: rgb(43, 45, 49);\n""font: 11pt \"Gill Sans MT\";")
descripcion_label.setObjectName("descripcion_label")
descripcion_label.setVisible(False)
descripcion_label.setText("Descripcion:")

jsondata_entry_3 = QtWidgets.QPlainTextEdit(fondo_franem_3)
jsondata_entry_3.setGeometry(QtCore.QRect(390, 20, 212, 221))
jsondata_entry_3.setStyleSheet("color: rgb(255, 255, 255);\n""font: 8pt \"Arial\";")
jsondata_entry_3.setReadOnly(True)
jsondata_entry_3.setObjectName("jsondata_entry_3")

jsondata_label_3 = QtWidgets.QLabel(fondo_franem_3)
jsondata_label_3.setGeometry(QtCore.QRect(426, 1, 141, 16))
jsondata_label_3.setStyleSheet("color: rgb(255, 255, 255);\n""font: 75 12pt \"Gill Sans MT\";")
jsondata_label_3.setAlignment(QtCore.Qt.AlignCenter)
jsondata_label_3.setObjectName("jsondata_label_3")
jsondata_label_3.setText("Informacion de la API:")

copiarinf_btn_bot = QtWidgets.QPushButton(fondo_franem_3)
copiarinf_btn_bot.setGeometry(QtCore.QRect(190, 165, 191, 31))
copiarinf_btn_bot.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 10pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
copiarinf_btn_bot.setIcon(icon)
copiarinf_btn_bot.setIconSize(QtCore.QSize(22, 22))
copiarinf_btn_bot.setObjectName("copiarinf_btn_bot")
copiarinf_btn_bot.setVisible(False)
copiarinf_btn_bot.clicked.connect(copiar_func_bot)
copiarinf_btn_bot.setText("Copiar Datos")

busqueda_btn_bot = QtWidgets.QPushButton(fondo_franem_3)
busqueda_btn_bot.setGeometry(QtCore.QRect(190, 200, 191, 31))
busqueda_btn_bot.setStyleSheet("QPushButton {\n"
"                color: rgb(255, 255, 255);"
"                font: 10pt \"Gill Sans MT\";"
"                background-color: rgb(67, 68, 75);\n"
"                border-radius: 2px;\n"
"                padding: 5px;\n"
"}\n"
"            \n"
"QPushButton:hover {\n"
"                background-color: #484951\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"                background-color: #3c3d44\n"
"}")
icond = QtGui.QIcon()
icond.addPixmap(QtGui.QPixmap("icons/lup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
busqueda_btn_bot.setIcon(icond)
busqueda_btn_bot.setIconSize(QtCore.QSize(22, 22))
busqueda_btn_bot.setObjectName("busqueda_btn_bot")
busqueda_btn_bot.setVisible(False)
busqueda_btn_bot.clicked.connect(lambda: webbrowser.open(f'https://discordlookup.com/application/{bot_id}'))
busqueda_btn_bot.setText('Busqueda con discordlookup')

tabWidget.setCurrentIndex(0)
QtCore.QMetaObject.connectSlotsByName(MainWindow)

def retranslateUi(MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate("MainWindow", "Discord Inspector"))
    id_label.setText(_translate("MainWindow", "ID"))
    buscaruser_btn.setText(_translate("MainWindow", "Buscar"))
    jsondata_label.setText(_translate("MainWindow", "Informacion de la API:"))
    creadoen_label.setText(_translate("MainWindow", "Creado:"))
    tabWidget.setTabText(tabWidget.indexOf(tab), _translate("MainWindow", "Usuario (ID)"))
    tabWidget.setTabText(tabWidget.indexOf(tab_3), _translate("MainWindow", "Servidor (ID)"))
    tabWidget.setTabText(tabWidget.indexOf(tab_2), _translate("MainWindow", "Aplicacion (BOT ID)"))
    titulo_label.setText(_translate("MainWindow", "Discord Inspector"))
    titulo_label_2.setText(_translate("MainWindow", "By: Euronymou5"))

retranslateUi(MainWindow)

if __name__ == "__main__":
    MainWindow.show()
    sys.exit(app.exec_())
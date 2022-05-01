# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:34:56 2022

@author: hien2
"""

import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QMainWindow, QWidget, QLabel, QTextEdit, QRadioButton,
                             QFormLayout, QGridLayout, QToolTip, QMessageBox)
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from paramiko import client
#from fenetre_de_dossier import MVCViewDossier
#from fenetre_d_historique_ECUE235_DTTH import MVCViewHistorique
import datetime


hote_path = ('patients_hote.csv') #hote #thay doi ten cua file
vm_path = ('patients_vm.csv') #vm #thay doi ten cua file

class MVCView(QWidget):

    def __init__(self, ctrl):
        super().__init__()

        self.myCtrl = ctrl

        #logo
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('sante_logo.png'))
        self.logo.setStyleSheet("margin: 0px")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        #nom de plateforme
        self.nom_pe = QLabel("ParaSanté") 
        self.nom_pe.setStyleSheet("font-family: 'Roboto', sans-serif; font-size: 20pt; font-weight: bold; margin: 0px 50px")
        self.nom_pe.setAlignment(QtCore.Qt.AlignCenter)
        
        #Message de bienvenue
        self.mess = QLabel("Bienvenue à notre application!")
        self.mess.setStyleSheet("font-family: 'Roboto', sans-serif; font-size: 12pt; margin: 0px 50px")
        self.mess.setAlignment(QtCore.Qt.AlignCenter)
        
        #bouton "Créer un dossier"
        self.btn_creer = QPushButton('Créer un dossier')
        self.btn_creer.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 0px 80px 5px")

        #bouton "Importer un dossier"
        self.btn_import = QPushButton('Importer un dossier')
        self.btn_import.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 0px 80px 20px")


        self.init_ui()

        self.show()

    def init_ui(self):
        v_box = QVBoxLayout()
        v_box.addWidget(self.logo)
        v_box.addWidget(self.nom_pe)
        v_box.addWidget(self.mess)
        v_box.addWidget(self.btn_creer)
        v_box.addWidget(self.btn_import)

        self.setLayout(v_box)
        self.setWindowTitle("Fenêtre d'accueil")
        self.setFixedSize(335, 380)
        #self.move(300, 50)
        self.setStyleSheet("background-color: #f0ecec; border-radius: 5px")
        self.setWindowIcon(QIcon('sante_logo.png'))

        self.btn_creer.clicked.connect(self.btn_creer_click)
        #self.btn_import.clicked.connect(self.btn_import_click)

    @pyqtSlot()
    def btn_creer_click(self):
        self.trans = MVCViewDossier(self.myCtrl)
        self.close()

    """"@pyqtSlot()
    def bouton_ouvrirDossier_click(self):
        self.trans = MVCViewImporter(self.myCtrl)
        self.close()"""


class MVCViewDossier(QWidget):
    fermeturequelclient = QtCore.pyqtSignal(str)
    def __init__(self, ctrl, nom_e=None, prenom_e=None, age_e=None, sexe_e=None, sym_e=None, ordo_e=None):
        super().__init__()
        self.myCtrl = ctrl

        # nom
        self.nom_label = QLabel("Nom")
        self.nom_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin: 10px 0px 5px 15px")
        self.nom_text = QLineEdit(nom_e)
        self.nom_text.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; background-color: #fff; margin: 10px 0px 5px 5px")

        # prenom
        self.prenom_label = QLabel("Prénom")
        self.prenom_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-bottom: 5px")
        self.prenom_text = QLineEdit(prenom_e)
        self.prenom_text.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; background-color: #fff; margin-bottom: 5px")

        # age
        self.age_label = QLabel("Âge")
        self.age_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-bottom: 5px")
        self.age_text = QLineEdit(age_e)
        self.age_text.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; background-color: #fff; margin-bottom: 5px")

        # sexe
        self.sexe_label = QLabel("Sexe")
        self.sexe_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px")
        self.sexe_m = QRadioButton("M", self)
        self.sexe_f = QRadioButton("F", self)
        self.sexe_m.setChecked(True) if sexe_e == "M" else None
        self.sexe_f.setChecked(True) if sexe_e == "F" else None

        # button
        self.btn_h = QPushButton('Historique')
        self.btn_h.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 0px 20px 5px 50px")
        self.btn_e = QPushButton("Enregistrer")
        self.btn_e.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 20px")
        self.btn_f = QPushButton("Fermer")
        self.btn_f.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 10px; margin: 20px")

        # zone de text
        self.sym_label = QLabel("Symptômes")
        self.sym_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-top: 15px")
        self.sym = QTextEdit(sym_e)
        self.sym.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; background-color: #fff; padding: 10px; margin: 0px 20px 5px 15px")
        self.sym.textChanged.connect(self.propo_connect)

        self.ordo_label = QLabel("Ordonnances")
        self.ordo_label.setStyleSheet("font-family: 'Roboto', sans-serif; margin-left: 15px; margin-top: 5px")
        self.ordo = QTextEdit(ordo_e)
        self.ordo.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; background-color: #fff; padding: 10px; margin: 0px 20px 5px 15px")
        self.propo = QTextEdit("")
        self.propo.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; padding: 10px; margin: 20px 20px 5px")

        self.list_medica = {"Doliprane": ["Douleur", "Fievre", "Nausee"],
                           "Dafalgan": ["Douleur", "Fievre", "Sudation", "Naussee"],
                           "Efferalgant": ["Douleur", "Fievre"],
                           "Kardegic": ["Hypertension", "Douleur", "Depression"],
                           "Spasfon": ["Douleur", "Digestif"],
                           "Gaviscon": ["Estomac", "Brulures"],
                           "Dexeryl": ["Douleur", "Irritation", "Urticaire"],
                           "Meteospasmyl": ["Ballonement", "Digestif"],
                           "Biseptine": ["Infectées", "Infection"],
                           "Eludril": ["Infecion", "Bouche"]}

        self.init_ui()

        self.show()

    def init_ui(self):
        QToolTip.setFont(QFont('Roboto', 14))
        self.btn_f.setToolTip('Cliquez ici pour retourner à la fenêtre de accueil')
        self.btn_e.setToolTip('Cliquez ici pour enregistrer les informations dans la fiche du patient')
        self.btn_h.setToolTip('Cliquez ici pour enregistrer les informations dans la fiche du patient')
        h_box = QHBoxLayout()
        f_box = QFormLayout()
        f_box.addRow(self.nom_label, self.nom_text)
        f_box.addRow(self.prenom_label, self.prenom_text)
        f_box.addRow(self.age_label, self.age_text)
        h_box.addWidget(self.sexe_label)
        h_box.addWidget(self.sexe_m)
        h_box.addWidget(self.sexe_f)
        f_box.addRow(h_box)

        k_box = QVBoxLayout()
        k_box.addWidget(self.sym_label)
        k_box.addWidget(self.sym)
        k_box.addWidget(self.ordo_label)
        k_box.addWidget(self.ordo)

        layout = QGridLayout()
        layout.addLayout(f_box, 0, 0)
        layout.addWidget(self.btn_h, 0, 1)
        layout.addLayout(k_box, 1, 0)
        layout.addWidget(self.propo, 1, 1)
        layout.addWidget(self.btn_e, 2, 0)
        layout.addWidget(self.btn_f, 2, 1)

        self.setLayout(layout)
        self.setWindowTitle("Fenêtre de doissier")
        # self.move(250, 50)
        self.setFixedSize(450, 450)
        self.setStyleSheet("background-color: #f0ecec")
        self.setWindowIcon(QIcon('sante_logo.png'))

        self.propo.setDisabled(True)
        self.btn_f.clicked.connect(self.btn_f_click)
        self.btn_e.clicked.connect(self.btn_e_click)
        self.btn_h.clicked.connect(self.btn_h_click)
        self.sexe_m.toggled.connect(self.radiobtn_sexe_click)
        self.sexe_f.toggled.connect(self.radiobtn_sexe_click)

    @pyqtSlot()
    def btn_f_click(self):
        self.trans = MVCView(self.myCtrl)
        self.close()

    def radiobtn_sexe_click(self):
        if self.sexe_m.isChecked():
            return self.sexe_m.text()
        if self.sexe_f.isChecked():
            return self.sexe_f.text()

    def btn_e_click(self):
        nom_e = self.nom_text.text().upper()
        nom_e = " ".join(nom_e.split())
        prenom_e = self.prenom_text.text().title()
        prenom_e = " ".join(prenom_e.split())
        age_e = self.age_text.text()
        age_e = " ".join(age_e.split())
        sexe_e = self.radiobtn_sexe_click()
        sym_e = self.sym.toPlainText().title()
        sym_e = " ".join(sym_e.split())
        ordo_e = self.ordo.toPlainText().title()
        ordo_e = " ".join(ordo_e.split())

        if (nom_e == '' or prenom_e == '' or age_e == '' or sexe_e == '' or sym_e == '' or ordo_e == ''):
            self.btn_e.setToolTip("Veuillez remplir tous les champs avant de cliquer ce bouton")
        else:
            self.myCtrl.save(nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e)
            self.nom_text.setText("")
            self.prenom_text.setText("")
            self.age_text.setText("")
            self.sym.setText("")
            self.ordo.setText("")

    @pyqtSlot()
    def btn_h_click(self):
        try:
            self.aux = self.myCtrl.show()
            nom_h = list(list(self.aux.values())[0].values())
            nom_e = self.nom_text.text().upper()
            nom_e = " ".join(nom_e.split())
            for i in range(len(nom_h)):
                if (nom_e == nom_h[i]):
                    self.nom_txt_h = nom_h[i]

            prenom_h = list(list(self.aux.values())[1].values())
            prenom_e = self.prenom_text.text().title()
            prenom_e = " ".join(prenom_e.split())
            for i in range(len(prenom_h)):
                if (prenom_e == prenom_h[i]):
                    self.prenom_txt_h = prenom_h[i]

            age_h = list(list(self.aux.values())[2].values())
            age_e = self.age_text.text()
            age_e = " ".join(age_e.split())
            for i in range(len(age_h)):
                age_h[i] = str(age_h[i])
                if (age_e == age_h[i]):
                    self.age_txt_h = str(age_h[i])

            sexe_h = list(list(self.aux.values())[3].values())
            sexe_e = self.radiobtn_sexe_click()
            for i in range(len(sexe_h)):
                if (sexe_e == sexe_h[i]):
                    self.sexe_txt_h = sexe_h[i]

            sym_h = list(list(self.aux.values())[4].values())
            sym_e = self.sym.toPlainText().title()
            sym_e = " ".join(sym_e.split())
            for i in range(len(sym_h)):
                if (sym_e == sym_h[i]):
                    self.sym_txt_h = str(sym_h[i])

            ordo_h = list(list(self.aux.values())[5].values())
            ordo_e = self.ordo.toPlainText().title()
            ordo_e = " ".join(ordo_e.split())
            for i in range(len(ordo_h)):
                if (ordo_e == ordo_h[i]):
                    self.ordo_txt_h = ordo_h[i]

            if (nom_e == '' or prenom_e == '' or age_e == '' or sexe_e == '' or sym_e == '' or ordo_e == ''):
                self.btn_h.setToolTip("Veuillez remplir tous les champs avant de cliquer ce bouton")
            else:
                self.trans = MVCViewHistorique(self.myCtrl, self.nom_txt_h, self.prenom_txt_h, self.age_txt_h, self.sexe_txt_h, self.sym_txt_h, self.ordo_txt_h)
                self.close()
        except:
            QMessageBox.about(self, "Erreur", "Veuillez vérifier toutes les informations du patient que vous voulez chercher!!!")

    def propo_connect(self):
        self.propo.clear()
        self.sym_connect = self.sym.toPlainText().split('\n')
        self.sym_list = [] #liste des symptomes saisies

        for i in self.sym_connect:
            self.sym_ligne = i.split(" ") #Après une espace, c'est un symptome
            for j in self.sym_ligne:
                self.sym_list.append(j)  #Ajoute chaque symptome dans la liste

        self.ordo_list = []
        for l in range(len(self.sym_list)): #l chaque symptome dans la liste des symptomes
            for m in self.list_medica.keys(): #m chaque médicament
                for n in self.list_medica[m]: #n liste des symptomes liée à chaque médicament
                    if self.sym_list[l] == n:     #On cherche symptome saisie dans n la liste des symptome
                        self.ordo_list.append(m) #on ajoute m médicement dans l'ordonnance

        self.ordo_list = list(set(self.ordo_list)) #convertir "list" en "set" pour éviter l'affichage des médicaments plusieurs fois, puis, revenir la list en "list"

        self.ordo_string = "\n".join(self.ordo_list) #convertir "list" en "str"

        self.propo.setText(self.ordo_string) #l'affichage des propositions des médicaments liés à ses symptomes

class MVCViewHistorique(QWidget):

    def __init__(self, ctrl, nom_txt_h="", prenom_txt_h="", age_txt_h="", sexe_txt_h="", sym_txt_h="", ordo_txt_h=""):
        super().__init__()

        self.myCtrl = ctrl
        #nom
        self.nom_label_h = QLabel("Nom")
        self.nom_label_h.setStyleSheet("font-family: 'Roboto'; margin: 10px 0px 5px 15px")
        self.nom_text_h = QLineEdit(nom_txt_h)
        self.nom_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin: 10px 0px 5px 5px; margin-right: 220px")

        #prenom
        self.prenom_label_h = QLabel("Prénom")
        self.prenom_label_h.setStyleSheet("font-family: 'Roboto'; margin-left: 15px; margin-bottom: 5px")
        self.prenom_text_h = QLineEdit(prenom_txt_h)
        self.prenom_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; margin-bottom: 5px; margin-right: 220px")

        #age
        self.age_label_h = QLabel("Âge")
        self.age_label_h.setStyleSheet("font-family: 'Roboto'; margin-left: 15px; margin-bottom: 5px")
        self.age_text_h = QLineEdit(age_txt_h)
        self.age_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; margin-bottom: 5px; margin-right: 220px")

        #sexe
        self.sexe_label_h = QLabel("Sexe")
        self.sexe_label_h.setStyleSheet("font-family: 'Roboto'; margin-left: 15px; margin-bottom: 5px")
        self.sexe_text_h = QLineEdit(sexe_txt_h)
        self.sexe_text_h.setStyleSheet("border-radius: 5px; border: 1px solid #01579b; margin-left: 5px; margin-bottom: 5px; margin-right: 220px")

        #button
        self.btn_f_h = QPushButton("Fermer")
        self.btn_f_h.setStyleSheet("font-size: 8pt; background-color: #01579b; color: #fff; text-align: center; border-radius: 5px; padding: 5px; margin: 10px 150px")

        #zone de text
        self.sym_label_h = QLabel("Symptômes")
        self.sym_label_h.setStyleSheet("font-family: 'Roboto'; margin: 10px 0px 5px 15px")
        self.sym_h = QTextEdit(sym_txt_h)
        self.sym_h.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; padding: 5px; margin: 0px 10px 5px")

        self.ordo_label_h = QLabel("Ordonnances")
        self.ordo_label_h.setStyleSheet("font-family: 'Roboto'; margin: 10px 0px 5px 15px")
        self.ordo_h = QTextEdit(ordo_txt_h)
        self.ordo_h.setStyleSheet("border: 1px solid #01579b; border-radius: 10px; padding: 5px; margin: 0px 10px 5px")

        self.init_ui()

        self.show()

    def init_ui(self):
        QToolTip.setFont(QFont('Roboto', 14))
        self.btn_f_h.setToolTip('Cliquez ici pour retourner à la fenêtre de dossier')
        f_box = QFormLayout()
        f_box.addRow(self.nom_label_h, self.nom_text_h)
        f_box.addRow(self.prenom_label_h, self.prenom_text_h)
        f_box.addRow(self.age_label_h, self.age_text_h)
        f_box.addRow(self.sexe_label_h, self.sexe_text_h)

        v_box = QVBoxLayout()
        v_box.addLayout(f_box)
        v_box.addWidget(self.sym_label_h)
        v_box.addWidget(self.sym_h)
        v_box.addWidget(self.ordo_label_h)
        v_box.addWidget(self.ordo_h)
        v_box.addWidget(self.btn_f_h)

        self.setLayout(v_box)
        self.setWindowTitle("Fenêtre d'historique")
        #self.move(250, 50)
        self.setFixedSize(450, 500)
        self.setStyleSheet("background-color: #f0ecec")
        self.setWindowIcon(QIcon('sante_logo.png'))

        self.nom_text_h.setDisabled(True)
        self.prenom_text_h.setDisabled(True)
        self.age_text_h.setDisabled(True)
        self.sexe_text_h.setDisabled(True)
        self.sym_h.setDisabled(True)
        self.ordo_h.setDisabled(True)
        self.btn_f_h.clicked.connect(self.btn_f_h_click)

    @pyqtSlot()
    def btn_f_h_click(self):
        self.trans = MVCViewDossier(self.myCtrl)
        self.close()

# %%
class MVCController:

    def __init__(self, model):
        self.myModel = model

    def save(self, nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e):
        return self.myModel.savePatient(nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e)

    def show(self):
        self.aux = self.myModel.showPatient()
        return self.aux

# %%
class MVCModel:

    def __init__(self, ssh):
        self.ssh = ssh
        self.file = pd.DataFrame({'Nom': [], 'Prenom': [], 'Age': [], 'Sexe': [], 'Symptomes': [], 'Ordonnances': []})
        self.file = self.rcp()

    def savePatient(self, nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e):
        self.file.loc[len(self.file.index)] = [nom_e, prenom_e, age_e, sexe_e, sym_e, ordo_e]
        self.file.to_csv(hote_path, index=False)
        self.ssh.envoi_fichier()

    def showPatient(self):
        self.aux = self.file.to_dict()
        return self.aux

    def rcp(self):
        self.ssh.rcp_fichier()
        try:
            data = pd.read_csv(hote_path)
            return data
        except:
            print("Error!!!!!!! Le fichier est vide")
            return self.file

# %%
class ssh:
    client = None

    def __init__(self, hostname, port, username, password):
        try:
            print("Connecting to server.")
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username, password=password)
            self.sftp = self.client.open_sftp()
        except:
            print("Exception raised!")

    def envoi_fichier(self):
        self.sftp.put(hote_path, vm_path)

    def rcp_fichier(self):
        open(hote_path, 'a').close()
        try:
            print(self.sftp.stat(vm_path))
            print("File already exists.")
            self.sftp.get(vm_path, hote_path)
        except:
            print("Copying file.")
            self.sftp.put(hote_path, vm_path)


print(__name__)

hostname = "192.168.1.38"  # votre destination
username = "etudiant"
password = "vitrygtr"
port = 22

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ssh = ssh(hostname, port, username, password)
    model = MVCModel(ssh)
    ctrl = MVCController(model)
    window_a = MVCView(ctrl)
    sys.exit(app.exec_())

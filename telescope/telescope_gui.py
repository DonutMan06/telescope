#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:58:30 2021

@author: pierre
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from numpy import pi, sqrt, floor, log10
import sys

from matplotlib import pyplot as plt

from enum import Enum

from .astroids import read_sources, kua, body



sources_file = './telescope/sources.json'

astroids = read_sources(sources_file)

init_index = 0 # The GUI is initialized with astroids[init_value]

# Init index for telescope parameters
i_diam = 1
i_F = 2
i_f = 2

label_width = 100 # QLabel length

# Telescope properties
D_list = [150, 200, 250, 300] # Diamètre en mm
F_list = [500, 750, 1000, 1250, 1500, 1750] # Focale du primaire en mm
f_list = [1, 2, 5, 10, 15, 20, 25, 30, 35] # Focale de l'objectif en mm


class color_text(Enum):
    ENABLED  = '#000000'
    DISABLED = '#808080'
    WRONG    = '#FF0000'

class mainwin(QWidget):
    def __init__(self):
        
        
        # ------- WINDOWS CONSTRUCTION -------------- #
        super().__init__()

        self.setWindowTitle('Telescope simulator')
        
        d = QGridLayout()
        self.setLayout(d)
        
        ## Groupe entrées
        
        g1 = QGroupBox('Entrées')
        
        d1 = QFormLayout()
        
        # Entrée 1 : Cible
        
        self.target = QComboBox()
        self.target.addItems([x.name for x in astroids])
        self.target.setCurrentIndex(init_index)
        
        d1.addRow(QLabel('Cible'), self.target)
        
        
        # Entrée 2 : Distance
        
        self.distance = QSlider(Qt.Horizontal)
        self.distance.setMinimum(0)
        self.distance.setMaximum(101)
        self.distance.setSingleStep(1)
        self.distance.setValue(25)
        self.distance.setTickPosition(QSlider.TicksBelow)
        
        d1.addRow(QLabel('Distance'), self.distance)

        
        # Entrée 3 : Diamètre
        
        self.diametre = QComboBox()
        self.diametre.addItems([str(x)+' mm' for x in D_list])
        self.diametre.setCurrentIndex(i_diam)
        
        d1.addRow(QLabel('Diamètre objectif'), self.diametre)
        
        
        # Entrée 4 : Focale primaire
        
        self.F = QComboBox()
        self.F.addItems([str(x)+' mm' for x in F_list])
        self.F.setCurrentIndex(i_F)
        
        d1.addRow(QLabel('Focale primaire'), self.F)    
        
        
        # Entrée 5 : Focale secondaire
        
        self.f = QComboBox()
        self.f.addItems([str(x)+' mm' for x in f_list])
        self.f.setCurrentIndex(i_f)
        
        d1.addRow(QLabel('Focale oculaire'), self.f)
        
        
        # Entrée 6 : Champ apparent
        
        self.champ = QSlider(Qt.Horizontal)
        self.champ.setMinimum(29)
        self.champ.setMaximum(71)
        self.champ.setSingleStep(1)
        self.champ.setValue(50)
        self.champ.setTickPosition(QSlider.TicksBelow)
        
        d1.addRow(QLabel('Champ apparent'), self.champ)
        
        # Ajout des boutons Quitter et Plotter
        
        self.quit_button = QPushButton('&Quitter')
        self.plot_button = QPushButton('&Plot')
        d1.addRow(self.quit_button, self.plot_button)
        
        
        g1.setLayout(d1)
        
        d.addWidget(g1, 0, 0)
        
        
        ## Groupe sortie planete
        
        g2 = QGroupBox('Planete / Satellite')
        
        d2 = QFormLayout()
 
        self.aphelie_label = QLabel('Aphélie (ua)')
        self.aphelie = QLabel('0')
        self.aphelie.setAlignment(Qt.AlignRight)
        self.aphelie.setMinimumSize(label_width, 13)
        d2.addRow(self.aphelie_label, self.aphelie)   
        
        self.perihelie_label = QLabel('Périhélie (ua)')
        self.perihelie = QLabel('0')
        self.perihelie.setAlignment(Qt.AlignRight)
        self.perihelie.setMinimumSize(label_width, 13)
        d2.addRow(self.perihelie_label, self.perihelie)
        
        
        self.apogee_label = QLabel('Apogée (km)')
        self.apogee = QLabel('0')
        self.apogee.setAlignment(Qt.AlignRight)
        self.apogee.setMinimumSize(label_width, 13)
        d2.addRow(self.apogee_label, self.apogee)        
 
        self.perigee_label = QLabel('Périgée (ua)')
        self.perigee = QLabel('0')
        self.perigee.setAlignment(Qt.AlignRight)
        self.perigee.setMinimumSize(label_width, 13)
        
        d2.addRow(self.perigee_label, self.perigee)
        
    
        
        self.d_mean = QLabel('0')
        self.d_mean.setAlignment(Qt.AlignRight)
        self.d_mean.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Distance Soleil (ua)'), self.d_mean)  
        
        self.radius = QLabel('0')
        self.radius.setAlignment(Qt.AlignRight)
        self.radius.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Rayon moyen (km)'), self.radius)
        
        self.d_earth = QLabel('0')
        self.d_earth.setAlignment(Qt.AlignRight)
        self.d_earth.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Distance Terre (ua)'), self.d_earth)
        
        self.alpha_in = QLabel('0')
        self.alpha_in.setAlignment(Qt.AlignRight)
        self.alpha_in.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Angle apparent'), self.alpha_in)

        self.albedo = QLabel('0')
        self.albedo.setAlignment(Qt.AlignRight)
        self.albedo.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Albedo de bond'), self.albedo)       

        self.pout = QLabel('0')
        self.pout.setAlignment(Qt.AlignRight)
        self.pout.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Puissance lumineuse (W)'), self.pout)  

        self.psurf= QLabel('0')
        self.psurf.setAlignment(Qt.AlignRight)
        self.psurf.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Puissance surfacique sur Terre (W/m2)'), self.psurf)  

        self.mag_in = QLabel('0')
        self.mag_in.setAlignment(Qt.AlignRight)
        self.mag_in.setMinimumSize(label_width, 13)
        d2.addRow(QLabel('Magnitude apparente'), self.mag_in)       
   
        g2.setLayout(d2)
        
        d.addWidget(g2, 0, 1)
        
        
        
        ## Groupe sortie instrument
        
        g3 = QGroupBox('Instrument')
        
        d3 = QFormLayout()
        
        self.Ge = QLabel('0')
        d3.addRow(QLabel('Grossissement équipupillaire'), self.Ge)
        self.Ge.setAlignment(Qt.AlignRight)
        self.Ge.setMinimumSize(label_width, 13)
        
        self.G = QLabel('0')
        d3.addRow(QLabel('Grossissement'), self.G)
        self.G.setAlignment(Qt.AlignRight)
        self.G.setMinimumSize(label_width, 13)
        
        self.Gmax = QLabel('0')
        d3.addRow(QLabel('Grossissement max'), self.Gmax)
        self.Gmax.setAlignment(Qt.AlignRight)
        self.Gmax.setMinimumSize(label_width, 13)
        
        self.Ca = QLabel('0')
        d3.addRow(QLabel('Champ apparent'), self.Ca)
        self.Ca.setAlignment(Qt.AlignRight)
        self.Ca.setMinimumSize(label_width, 13)
        
        self.Cr = QLabel('0')
        d3.addRow(QLabel('Champ réel'), self.Cr)
        self.Cr.setAlignment(Qt.AlignRight)
        self.Cr.setMinimumSize(label_width, 13)
        
        self.doc = QLabel('0')
        d3.addRow(QLabel('Diamètre disque oculaire (mm)'), self.doc)
        self.doc.setAlignment(Qt.AlignRight)
        self.doc.setMinimumSize(label_width, 13)

        self.taille = QLabel('0')
        d3.addRow(QLabel('Taille au foyer (mm)'), self.taille)
        self.taille.setAlignment(Qt.AlignRight)
        self.taille.setMinimumSize(label_width, 13)          

        self.E = QLabel('0')
        d3.addRow(QLabel('Eclairement au foyer (W/m2)'), self.E)
        self.E.setAlignment(Qt.AlignRight)
        self.E.setMinimumSize(label_width, 13)

        self.mag_out = QLabel('0')
        d3.addRow(QLabel('Magnitude apparente'), self.mag_out)
        self.mag_out.setAlignment(Qt.AlignRight)
        self.mag_out.setMinimumSize(label_width, 13)

        self.alpha_out = QLabel('0')
        d3.addRow(QLabel('Angle apparent (minutes d\'arc)'), self.alpha_out)
        self.alpha_out.setAlignment(Qt.AlignRight)
        self.alpha_out.setMinimumSize(label_width, 13)
        
        
        self.dt = QLabel('0')
        d3.addRow(QLabel('Temps observation (minutes)'), self.dt)
        self.dt.setAlignment(Qt.AlignRight)
        self.dt.setMinimumSize(label_width, 13)
        
        g3.setLayout(d3)
        
        d.addWidget(g3, 0, 2)       
        
        self.show()
        
        
    # ------------- METHODS --------------------- #
    
    def get_astroid_index(self):
        # Retourne l'index de l'objet actuellement sélectionné
        return self.target.currentIndex()
    
    def get_astroid(self):
        itarget = self.get_astroid_index()
        return astroids[itarget]
    
    def get_aphelie_perihelie_str(self):
        # Retourne l'aphélie et le perihélie en ua
        p = self.get_astroid()

        if p.bodytype == body.PLANET:
            aphelie =  '{:5.2f}'.format(p.aphelie/kua)
            perihelie = '{:5.2f}'.format(p.perihelie/kua)
        else:
            aphelie = 'NA'
            perihelie = 'NA'
        
        return (aphelie, perihelie)

    def get_apogee_perigee_str(self):
        # Retourne l'aogee et le perigee en km
        p = self.get_astroid()
        
        if p.bodytype == body.SATELLITE:
            apogee =  '{:5.2f}'.format(p.apogee)
            perigee = '{:5.2f}'.format(p.perigee)
        else:
            apogee = 'NA'
            perigee = 'NA'
        
        return (apogee, perigee)
    
    def get_sun_distance(self):
        # Retourne la distance moyenne au Soleil en ua
        p = self.get_astroid()
        
        return p.d/kua
    
    
    def get_sun_distance_str(self):
        # Retourne la distance moyenne au Soleil en ua
        return '{:5.2f}'.format(self.get_sun_distance())
    
    def get_radius(self):
        # Retourne le rayon moyen de l'astre en km
        p = self.get_astroid()
        
        return p.radius
    
    
    def get_radius_str(self):
        # Retourne le rayon moyen de l'astre en km

        return '{:7.1f}'.format(self.get_radius())
    
    
    def get_earth_distance(self):
        # Retourne la distance à la Terre actuelle en km
        p = self.get_astroid()
        
        kf = self.distance.value()/100 # between 0 and 1...
        
        d_earth = kf*(p.d_earth_max - p.d_earth_min) + p.d_earth_min
        return d_earth
    
    def get_earth_distance_str(self):
        # Retourne la distance à la Terre actuelle en ua
        d_earth = self.get_earth_distance()/kua
        return '{:5.2f}'.format(d_earth) 
    
    
    def get_apparent_angle(self):
        # Retourne l'angle apparent en radians
        alpha_in_rad = 2*self.get_radius()/self.get_earth_distance()
        return alpha_in_rad
    
    def get_apparent_angle_str(self):
        # Retourne l'angle apparent en radians
        alpha_in_rad = self.get_apparent_angle()
        alpha_in_min = (alpha_in_rad*180/pi)*60
        alpha_in_sec = (alpha_in_min-floor(alpha_in_min))*60
        
        
        alpha_in = '%02d\' %02d\"' % (floor(alpha_in_min), floor(alpha_in_sec))  
        
        return alpha_in
        
    def get_albedo(self):
        p = self.get_astroid()
        return p.albedo
    
    def get_albedo_str(self):
        albedo = self.get_albedo()
        albedo_str = '%05.3f' % albedo
        return albedo_str
    
    def get_power(self):
        p = self.get_astroid()
        return p.Pout
    
    def get_power_str(self):
        P = self.get_power()
        return '%3.2e' % P # Puissance totale émise par la surface de la planète
    
    def get_surf_power(self):
        P = self.get_power()
        d_earth_km = self.get_earth_distance()
        return P/(4*pi*d_earth_km*d_earth_km*1e6) # W/m^2
    
    def get_surf_power_str(self):
        P = self.get_surf_power()
        return '%3.2e' % P
    
    def get_apparent_magnitude(self):
        
        P_sol = 3.826*1e26 # Puissance Solaire en W
        d = 150e6 # km
        E_sol = P_sol/(4*pi*d*d*1e6) # W/m2
        M_sol = -26.7

        # Determination of the C constant
        C = M_sol+ 2.5*log10(E_sol)
        
        p = self.get_astroid()
        P = p.Pout # W
        d = self.get_earth_distance() # km
        E = P/(4*pi*d*d*1e6)
        
        return -2.5*log10(E)+C
    
    def get_apparent_magnitude_str(self):
        M = self.get_apparent_magnitude()
        return '%+05.2f' % M
    
    
    def get_D(self):
         # Renvoie le diamètre de l'objectif en mm
        itarget = self.diametre.currentIndex()
        return D_list[itarget]   
    
    
    def get_F(self):
        # Renvoie la focale primaire en mm
        itarget = self.F.currentIndex()
        return F_list[itarget]
        
    def get_f(self):
        # Renvoie la focale secondaire en mm
        itarget = self.f.currentIndex()
        return f_list[itarget]
    
    def get_field(self):
        # Renvoie le champ apparent en degrés
        return self.champ.value()
    
    def get_field_str(self):
        champ = self.get_field()
        return '%6.2f °' % champ
    
    def get_Ge(self):
        D = self.get_D()
        return D/6

    def get_Ge_str(self):
        Ge = self.get_Ge()
        return '%d' % floor(Ge)
    
    def get_G(self):
        return self.get_F()/self.get_f()

    def get_G_str(self):
        G = self.get_G()
        return '%d' % floor(G)
    
    def get_Gm(self):
        return 2*self.get_D()

    def get_Gm_str(self):
        Gm = self.get_Gm()
        return '%d' % floor(Gm)   
    
    def get_real_field(self):
        # Renvoie le champ réel en degrés
        return self.champ.value()/self.get_G()
    
    def get_real_field_str(self):
        # Renvoie le champ réel en degrés
        champ = self.get_real_field()
        return '%6.2f °' % champ
    
    def get_doc(self):
        # Renvoie le diamètre du disque oculaire en mm
        f = self.get_f()
        F = self.get_F()
        D = self.get_D()
        return (f/F)*D

    def get_doc_str(self):
        doc = self.get_doc()
        return '%5.2f' % doc
    
    def get_taille(self):
        # Renvoie la taille de l'image au foyer en mm
        alpha = self.get_apparent_angle() # rad
        F = self.get_F() # mm
        return alpha*F
    
    def get_taille_str(self):
        taille = self.get_taille()
        return '%3.2e' % taille     
    
    def get_E(self):
        # Renvoie l'éclairement au foyer en W/m^2
        p = self.get_astroid()
        
        phi = p.Pout # W
        D = self.get_D()*1e-3 # m
        F = self.get_F()*1e-3 # m
        delta = 2*p.radius*1e3 # m
        E = (phi/(4*pi))*D/(F*delta)*D/(F*delta) # W/m^2
        return E
    
    def get_E_str(self):
        E = self.get_E()
        return '%3.2e' % E       
    
    def get_apparent_angle_out(self):
        # Retourne l'angle apparent en sortie en radians
        alpha_in = self.get_apparent_angle()
        F = self.get_F()
        f = self.get_f()
        
        return alpha_in*F/f
    
    def get_apparent_angle_out_str(self):
        # Retourne l'angle apparent en sortie
        alpha_in_rad = self.get_apparent_angle_out()
        alpha_in_min = (alpha_in_rad*180/pi)*60
        alpha_in_sec = (alpha_in_min-floor(alpha_in_min))*60
        
        
        alpha_in = '%02d\' %02d\"' % (floor(alpha_in_min), floor(alpha_in_sec))  
        
        return alpha_in
    
    def get_dt(self):
        # Renvoie le temps d'observation de la cible en minutes
        alpha = 0.5*self.get_real_field()*pi/180 # Radians
        T = 24*60 # Période de rotation terrestre en minutes
        
        return (alpha/(2*pi))*T
    
    def get_dt_str(self):
        dt = self.get_dt()
        dt_min = floor(dt)
        dt_sec = floor((dt-dt_min)*60)
        return '%02d\' %02d\"' % (dt_min, dt_sec)       
    
class controleur():
    def __init__(self, modele, vue):
        self._plot_view = modele
        self._vue = vue
        self.connectionSignaux()
        self.update()
        
    def connectionSignaux(self):
        
        self._vue.target.currentIndexChanged.connect(self.update)
        self._vue.distance.sliderMoved.connect(self.update)
        self._vue.diametre.currentIndexChanged.connect(self.update)
        self._vue.F.currentIndexChanged.connect(self.update)
        self._vue.f.currentIndexChanged.connect(self.update)
        self._vue.champ.sliderMoved.connect(self.update)
        
        self._vue.quit_button.clicked.connect(self.quitter)
        self._vue.plot_button.clicked.connect(self.tracer)

    def quitter(self):
        print('Exiting the program...')
        sys.exit()
        
    def tracer(self):
        # Ici on prépare tout ce qu'il faut pour tracer et on appele ensuite
        # le modèle...
        
        p = self._vue.get_astroid()
        #alpha = self._vue.get_apparent_angle() # rad
        #alpha_max = self._vue.get_real_field()*pi/180 # rad
        
        alpha = self._vue.get_apparent_angle_out()*180/pi # degrés
        alpha_max = self._vue.get_field() # degrés
        
        self._plot_view(p, alpha, alpha_max)
        
        
        
    def update(self):
        
        p = self._vue.get_astroid()
        
        # Panneau Planete/Satellite
        
        if p.bodytype == body.SATELLITE: # Aphélie et Périhélie sont NA
            self._vue.aphelie_label.setStyleSheet('color: ' + color_text.DISABLED.value)
            self._vue.perihelie_label.setStyleSheet('color: ' + color_text.DISABLED.value)
            self._vue.aphelie.setStyleSheet('color: ' + color_text.DISABLED.value)
            self._vue.perihelie.setStyleSheet('color: ' + color_text.DISABLED.value)
            
            self._vue.apogee_label.setStyleSheet('color: ' + color_text.ENABLED.value)
            self._vue.perigee_label.setStyleSheet('color: ' + color_text.ENABLED.value)
            self._vue.apogee.setStyleSheet('color: ' + color_text.ENABLED.value)
            self._vue.perigee.setStyleSheet('color: ' + color_text.ENABLED.value)
        else:
            self._vue.aphelie_label.setStyleSheet('color: ' + color_text.ENABLED.value)
            self._vue.perihelie_label.setStyleSheet('color: ' + color_text.ENABLED.value)
            self._vue.aphelie.setStyleSheet('color: ' + color_text.ENABLED.value)
            self._vue.perihelie.setStyleSheet('color: ' + color_text.ENABLED.value)
            
            self._vue.apogee_label.setStyleSheet('color: ' + color_text.DISABLED.value)
            self._vue.perigee_label.setStyleSheet('color: ' + color_text.DISABLED.value)            
            self._vue.apogee.setStyleSheet('color: ' + color_text.DISABLED.value)
            self._vue.perigee.setStyleSheet('color: ' + color_text.DISABLED.value)
            
        (aphelie, perihelie) = self._vue.get_aphelie_perihelie_str()
        self._vue.aphelie.setText(aphelie)
        self._vue.perihelie.setText(perihelie)
        
        (apogee, perigee) = self._vue.get_apogee_perigee_str()
        self._vue.apogee.setText(apogee)
        self._vue.perigee.setText(perigee)       
        
        self._vue.d_mean.setText(self._vue.get_sun_distance_str())
        self._vue.radius.setText(self._vue.get_radius_str())
        
        self._vue.d_earth.setText(self._vue.get_earth_distance_str())
        self._vue.alpha_in.setText(self._vue.get_apparent_angle_str())
        self._vue.albedo.setText(self._vue.get_albedo_str())
        self._vue.pout.setText(self._vue.get_power_str())
        self._vue.psurf.setText(self._vue.get_surf_power_str())
        
        self._vue.mag_in.setText(self._vue.get_apparent_magnitude_str())
        
        # Panneau Instrument
        
        self._vue.Ge.setText(self._vue.get_Ge_str())
        self._vue.G.setText(self._vue.get_G_str())
        self._vue.Gmax.setText(self._vue.get_Gm_str())
        
        if (self._vue.get_G()<self._vue.get_Ge()) or (self._vue.get_G()>self._vue.get_Gm()):
            # Nous sommes en dessous de Ge, on perd en luminosité
            # Nous sommes au dessus de Gm, on ne gagne rien
            self._vue.G.setStyleSheet('color: ' + color_text.WRONG.value)
        else:
            self._vue.G.setStyleSheet('color: ' + color_text.ENABLED.value)
            
        self._vue.Ca.setText(self._vue.get_field_str())  
        self._vue.Cr.setText(self._vue.get_real_field_str())
        
        self._vue.doc.setText(self._vue.get_doc_str())
        self._vue.taille.setText(self._vue.get_taille_str())
        self._vue.E.setText(self._vue.get_E_str())
        
        self._vue.alpha_out.setText(self._vue.get_apparent_angle_out_str())
        self._vue.dt.setText(self._vue.get_dt_str())
        
def plot_view(astroid, alpha, alpha_max):

    fig = plt.figure(figsize=(6, 6))
    ax = fig.gca()
    
    c1 = plt.Circle((0,0), 80, color=[0.8,0.8,0.8])
    ax.add_patch(c1)
    
    if alpha<alpha_max: # la cible ne déborde pas...
        c2 = plt.Circle((0,0), alpha_max, color=[0,0,0])
        c3 = plt.Circle((0,0), alpha, color=astroid.color)
        ax.add_patch(c2)
        ax.add_patch(c3)
        
    else:
        c2 = plt.Circle((0,0), alpha_max, color=astroid.color)
        ax.add_patch(c2)
    
    ax.set_xlim((-90,90))
    ax.set_ylim((-90,90))
    plt.axis('off')
    
    fig.show()
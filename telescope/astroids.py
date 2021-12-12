#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 09:21:44 2021

@author: pierre
"""

from numpy import pi, sqrt

from enum import Enum
import json

# Global scope variables

d_earth = 150e6 # Distance moyenne Terre-Soleil en km
P_sol = 3.826*1e26 # Flux énergétique du Soleil en Watt

kua = 150e6 # Conversion factor : 1 ua = kua * 1 km

## CLASSES
    
class body(Enum):
    PLANET = 1
    SATELLITE = 2

class astroid:
    def __init__(self, name, bodytype, radius, ring_radius, albedo, color):
        self.name = name
        self.bodytype = bodytype
        self.radius = radius # km
        self.ring_radius = ring_radius
        self.albedo = albedo
        self.color = color
        
    def __repr__(self):
        return 'Object \'%s\'' % self.name
    
    def __str__(self):
        self.__repr__()


class planet(astroid):
    """ Planet class, derived from astroid class
    name : name of the planet, [str]
    aphelie : aphelie in km, [float]
    perihelie : perihelie in km, [float]
    radius : radius of the planet in km, [float]
    ring_radius : radius of the planet's ring in km (set to 0 if no ring), [float]
    albedo : albedo de bond, sans unité, [float]
    color : color of the planet, [tbd]
    """


    def __init__(self, name, aphelie, perihelie, radius, ring_radius, albedo, color):
        
        super().__init__(name, body.PLANET, radius, ring_radius, albedo, color)
        
        (a, b, e) = get_orbit_parameters(aphelie, perihelie)
        self.a = a
        self.b = b
        self.e = e
            
        self.d = (a+b)/2 # Distance Soleil-planete, approximation orbite circulaire pour simplifier...
        
        if self.d > d_earth: # La planète est plus éloignée de la Terre que le Soleil
            self.d_earth_min =self.d - d_earth # Distance Terre-planete minimale (km)
            self.d_earth_max = self.d + d_earth # Distance Terre-planete maximale (km)
        else:
            self.d_earth_min = d_earth - self.d
            self.d_earth_max = self.d + d_earth
            
        self.d_earth_mean = (self.d_earth_min+self.d_earth_max)/2 # Distance Terre-planete moyenne (km)
        
        self.aphelie = aphelie
        self.perihelie = perihelie
        
        self.perigee = 0 # Not applicable
        self.apogee = 0 # Not applicable
        
        # Photometrie
        self.Pin = P_sol/(4*pi*self.d*self.d*1e6) # Puissance reçue du Soleil sur la planète en W/m^2
        self.Pout = self.Pin*pi*radius*radius*albedo*1e6 # Puissance émise en W par le disque de la planete
        

class satellite(astroid):
    """ Satellite class, derived from astroid class
    name : name of the satellite, [str]
    apogee : apogee in km, [float]
    perigee : perigee in km, [float]
    radius : radius of the satellite in km, [float]
    ring_radius : radius of the satellite's ring in km (set to 0 if no ring), [float]
    albedo : albedo de bond, sans unité, [float]
    color : color of the satellite, [tbd]
    """


    def __init__(self, name, apogee, perigee, radius, ring_radius, albedo, color):
        
        super().__init__(name, body.SATELLITE, radius, ring_radius, albedo, color)
        
        (a, b, e) = get_orbit_parameters(apogee, perigee)
        self.a = a
        self.b = b
        self.e = e
            
        self.d = kua # Distance Soleil-satellite, égale à 1 ua...
        
        self.d_earth_min = perigee # Fixed
        self.d_earth_max = apogee # Fixed
        self.d_earth_mean = (a+b)/2 # Fixed
        
 
        self.aphelie = 0 # Not applicable
        self.perihelie = 0 # Not applicable
        
        self.perigee = perigee
        self.apogee = apogee
        
        # Photometrie
        self.Pin = P_sol/(4*pi*d_earth*d_earth*1e6) # Puissance reçue du Soleil sur le satellite en W/m^2
        self.Pout = self.Pin*pi*radius*radius*albedo*1e6 # Puissance émise en W par le disque de la planete



## FUNCTIONS

def get_orbit_parameters(apoapside, periapside):
    """
    This function returns the main elliptic parameters from apoapside (in km)
    and periapside (in km)
    It is basic geometry properties and the names follow the standards.
    This function can be used both with aphelie/perihelie (for planets)
    and apogee/perigee (for satellites)
    """
    
    a = (apoapside+periapside)/2 # Semi-major axis (in km)
    e = (apoapside-periapside)/(apoapside+periapside) # Eccentricity
    
    b = a * sqrt(1-e*e) # Semi-minor axis (in km)
    
    return (a, b, e)


def read_sources(filename):
    with open(filename, 'r') as f:
        d = json.load(f)
    
    astroid_list = []

    for p in d['planet_list']:
        x = planet( name=p['name'], aphelie=p['aphelie'], perihelie=p['perihelie'],\
               radius=p['radius'], ring_radius=p['ring_radius'], albedo=p['albedo'],color=p['color'])
        astroid_list.append(x)
    
    for p in d['satellite_list']:
        x = satellite( name=p['name'], apogee=p['apogee'], perigee=p['perigee'],\
               radius=p['radius'], ring_radius=p['ring_radius'], albedo=p['albedo'],color=p['color'])
        astroid_list.append(x)
    
    return astroid_list
    

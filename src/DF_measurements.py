# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 20:44:51 2025

@author: sh2065
"""

import nplab.datafile as df
from nplab.instrument.camera.lumenera import LumeneraCamera
from nplab.instrument.stage.prior import ProScan
from nplab.instrument.spectrometer.seabreeze import OceanOpticsSpectrometer
# from nplab.instrument.light_sources.cube_laser import CubeLaser
from nplab.instrument.spectrometer.spectrometer_aligner import SpectrometerAligner
from nplab.instrument.camera.camera_with_location import CameraWithLocation
from nplab.instrument.shutter.BX51_uniblitz import Uniblitz
from nplab.utils.array_with_attrs import ArrayWithAttrs
from particle_tracking_app.particle_tracking_wizard import InfiniteTrackingWizard as TrackingWizard
import numpy as np
import time


stage = ProScan("COM3", hardware_version = 2)

# shutter = Uniblitz('COM6')#6
cam = LumeneraCamera(1)
# cam = LumeneraCamera(1)
# cam.show_gui()
spec = OceanOpticsSpectrometer(0)
spec.set_tec_temperature(-20)

CWL = CameraWithLocation(cam,stage)
CWL.show_gui(blocking =False)
stage.show_gui(blocking = False) 
spec.show_gui(blocking = False)
alinger = SpectrometerAligner(spec,stage)
equipment_dict = {'spectrometer':spec,
                  'alinger':alinger}


wizard = TrackingWizard(CWL,equipment_dict,task_list = ['z_scan'])
wizard.data_file.show_gui(blocking = False)
wizard.show()

def PL_measurement(exp=1,scan=10,laser=447, power=1):
    current_file= df.data_file
    
    shutter.close_shutter()
    time.sleep(0.5)
    laserOn(laserPower=power,laser=laser)
    time.sleep(1)
    spe=[]
    group=df.create_group('Particle_%')
    for i in range(scan):
        spe.append(spec.read_spectrum())
    attrs = spec.metadata
    group.create_dataset(name = 'kinetic_laserOff_%d',data = spe,attrs = attrs)
    laserOff()
    shutter.open_shutter()


def laserOn(laserPower=1, laser= 447):
    if laser == 447:
        cube = CubeLaser('COM5')
        cube.set_power(laserPower)
    else:
        cube = CubeLaser('COM7')
        cube.mode_switch(pulsed=0)
        time.sleep(0.5)
        cube.set_power(laserPower)

def laserOff(laser= 447):
    if laser == 447:
        cube = CubeLaser('COM5')
        cube.set_power(0)
    else:
        cube = CubeLaser('COM7')
        cube.mode_switch(pulsed=1)


data_file = df.current()
def irradiate(time = 1000.0,laser_power = 2,number_of_spec = 20,scans=10):
    
    spec.integration_time = time
    Particles=data_file.create_group(name = 'Particle_Au@Pd-BPT_%d')
    for i in range(scans):
        if i<1:
            spectrum_list_0 = []
            for j in range(number_of_spec):
                laserOff()
                spectrum_list_0.append(spec.read_spectrum())
            #laserOff()
            attrs = spec.metadata
            attrs['Laser_power'] = laser_power
            Particles.create_dataset(name = 'kinetic_laserOff_%d',data = spectrum_list_0,attrs = attrs)
        if i>scans-2:
            spectrum_list_1 = []
            laserOff()
            for j in range(number_of_spec):
                laserOff()
                spectrum_list_1.append(spec.read_spectrum())
            #laserOff()
            attrs = spec.metadata
            attrs['Laser_power'] = laser_power
            Particles.create_dataset(name = 'kinetic_laserOff_%d',data = spectrum_list_1,attrs = attrs)        
        else:
            spectrum_list_2 = []
            for z in range(number_of_spec):
                laserOn(laser_power)
                spectrum_list_2.append(spec.read_spectrum())
            #laserOff()
            attrs = spec.metadata
            attrs['Laser_power'] = laser_power
            Particles.create_dataset(name = 'kinetic_laserOn_%d',data = spectrum_list_2,attrs = attrs)
    laserOff()

def Track_PL(exposure = 1000.0,laser_power = 1,number_of_spec = 20, scan=1, laser=447, name='Particle_%d',Tracking=False,autofocus=False, name_1='kinetic_laserOn_%d',new_group=True,save_img=False):

    if new_group and Tracking == False:
        Particle=data_file.create_group(name=name)
    elif Tracking == False:
        Particle=data_file.require_group(name=name)
    img=CWL.thumb_image()
    for i in range(scan):
        CWL.move_to_feature(img, ignore_z_pos = True)
        if autofocus:
            CWL.autofocus()
        shutter.close_shutter()  
        time.sleep(1)
        spec.integration_time = exposure
        spectrum_list_2 = []
        laserOn(laser_power, laser=laser)
        for z in range(number_of_spec):
            spectrum_list_2.append(spec.read_spectrum())
        laserOff(laser=laser)
        attrs = spec.metadata
        attrs['Laser_power'] = laser_power
        shutter.open_shutter()
        if Tracking:
            wizard.particle_group.create_dataset(name = name_1,data = spectrum_list_2,attrs = attrs)
            if save_img:
                wizard.particle_group.create_dataset(name ='CWL.thumb_image_%d',data = img)
        else:
            Particle.create_dataset(name = name_1,data = spectrum_list_2,attrs = attrs)
            if save_img:
                Particle.particle_group.create_dataset(name ='CWL.thumb_image_%d',data = img)


def save_irradiate(h5filename = 'KineticScan'):
    data = irradiate()
    data_file.create_dataset(name = h5filename,data = data)

def z_scan(dz = np.arange(-3,3,0.35),exposure=1000,settling_time=0.1,save_img=False, name='Particle_%d',Tracking=True,new_group=True,data_name='z_scan_%d',save_data=True):
    
    if new_group and Tracking == False:
        Particle=data_file.create_group(name=name)
    elif Tracking == False:
        Particle=data_file.require_group(name=name)

    spectra = []
    here = stage.position
    spec.integration_time = exposure
    time.sleep(0.5)

    spec.read_spectrum() #reads spectrum trice to clear cached junk before taking measurement
    spec.read_spectrum()
    for z in dz:
        stage.move(np.array([0,0,z])+here)
        time.sleep(settling_time)
        spectra.append(spec.read_spectrum())
    attrs = spec.metadata
    time.sleep(0.5)
    stage.move(here)
    if Tracking and save_data:
        wizard.particle_group.create_dataset(name =data_name,data = spectra,attrs = attrs)
        if save_img:
            img=CWL.thumb_image()
            wizard.particle_group.create_dataset(name ='CWL.thumb_image_%d',data = img)
    elif save_data:
        Particle.create_dataset(name =data_name,data = spectra,attrs = attrs)
        if save_img:
            img=CWL.thumb_image()
            Particle.create_dataset(name ='CWL.thumb_image_%d',data = img)
    else:
        pass


def DF_power_series(power=[1,2,3,4,5,6],settle_time=10,exp_PL=1000):

    for i,j in enumerate(power):
        z_scan(Tracking=True)
        Track_PL(exposure = exp_PL,laser_power = j,number_of_spec = 10,Tracking=True,name_1='kinetic_laserOn_%d',new_group=True)
    z_scan()
    



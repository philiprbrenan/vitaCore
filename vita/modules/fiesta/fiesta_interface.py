#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:53:55 2019

@author: jmbols
"""
from matplotlib import pyplot as plt
import numpy as np
import scipy.io as sio
# Other imports
from vita.core import MagneticField
from vita.modules.utils import intersection


class Fiesta():
    '''
    Class for tracing the magnetic field lines given a FIESTA equlibrium

    :param str filename: the path to the FIESTA MATLAB save file.

    :ivar VectorFunction3D b_field: A 3D vector function of the magnetic field .

    member functions:
    '''
    def __init__(self, filename):
        self.filename = filename
        self.read_fiesta_model()

    @property
    def b_field(self):
        '''
        Function for getting the magnetic a 3D vector function of the magnetic field
        '''
        return MagneticField(self.r_vec, self.z_vec,
                             np.swapaxes(self.b_r, 0, 1), np.swapaxes(self.b_z, 0, 1),
                             np.swapaxes(self.b_phi, 0, 1))

    def read_fiesta_model(self):
        '''
        Function for reading the FIESTA equilibrium data from a .mat file

        input: self, a reference the object itself

        output: self.r_limiter, a numpy array with the radial coordinates of the vessel limits
                self.z_limiter, a numpy array with the vertical coordinates of the vessel limits
                self.r_vec,     a numpy array with the radial grid coordinates
                self.z_vec,     a numpy array with the vertical grid coordinates
                self.psi_n,
                self.b_r,       a numpy array with the radial magnetic field component
                self.b_z        a numpy array with the poloidal field component
                self.i_rod      a float with the current in the rod
        '''
        # Read data from .mat file
        mat = sio.loadmat(self.filename, mat_dtype=True, squeeze_me=True)

        # Get vessel limits
        self.r_limiter = mat['R_limits']
        self.z_limiter = mat['Z_limits']

        # Get grid data
        self.r_vec = mat['r']
        self.z_vec = mat['z']

        # Get magnetic data
        self.psi_n = mat['psi_n']
        self.b_r = mat['Br']
        self.b_z = mat['Bz']
        self.b_phi = mat['Bphi']
        self.i_rod = mat['irod']

    def get_midplane_lcfs(self, psi_p=1.0):
        '''
        Function for getting the inner and outer radial position of the LCFS at the midplane

        input: self, a reference to the object itself

        return: Rcross, a list with the outer and inner radial position of the mid-plane LCFS
        '''

        r_vec, z_vec = np.meshgrid(self.r_vec, self.z_vec)
        # Get contour
        cont = plt.contour(r_vec, z_vec, self.psi_n, [psi_p])
        cont = cont.allsegs[0]

        # Loop over the contours
        for c_i in cont:
            is_core = any(c_i[:, 1] > 0)*any(c_i[:, 1] < 0)
            if is_core:
                func1 = np.array((c_i[:, 0], c_i[:, 1]))
                func2 = np.array((np.array([0., 1.]), np.array([0., 0.])))
                r_lcfs, _ = intersection(func1, func2)

        plt.close() # plt.contour opens a plot, close it

        return r_lcfs

if __name__ == '__main__':
    FILEPATH = '/home/jmbols/Postdoc/ST40/Programme 1/Equilibrium/eq001_limited.mat'
    FIESTA_EQUIL = Fiesta(FILEPATH)
    print(FIESTA_EQUIL.get_midplane_lcfs())
    print(type(FIESTA_EQUIL.r_limiter))

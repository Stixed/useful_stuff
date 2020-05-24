import numpy as np
from scipy import interpolate

class Mode(object):
    
    def get_fields(self, comp):
        fields = np.zeros((len(self.x[:,0]), len(self.x[0,:]), len(self.eigenEnergies[:,1])), dtype=complex)
        for i in range(len(fields[0, 0, :])):
            if i<=len(fields[0, 0, :])/2:
                fname_real = '{f}_{f}/{f}/{s}_r.txt'.format(self.eigenEnergies[i,0], self.eigenEnergies[i,1], self.eigenEnergies[i,3], comp)
                fname_imag = '{f}_{f}/{f}/{s}_i.txt'.format(self.eigenEnergies[i,0], self.eigenEnergies[i,1], self.eigenEnergies[i,3], comp)
                realPart = np.loadtxt(fname_real, dtype=float, delimiter=' ')
                imagPart = np.loadtxt(fname_imag, dtype=float, delimiter=' ')
                fields[:,:,i] = realPart + 1j * imagPart
            else:
                fname_real = '{f}_{f}/{f}/{s}_r.txt'.format(self.eigenEnergies[i,1], self.eigenEnergies[i,0], self.eigenEnergies[i,3], comp)
                fname_imag = '{f}_{f}/{f}/{s}_i.txt'.format(self.eigenEnergies[i,1], self.eigenEnergies[i,0], self.eigenEnergies[i,3], comp)
                realPart = np.loadtxt(fname_real, dtype=float, delimiter=' ')
                imagPart = np.loadtxt(fname_imag, dtype=float, delimiter=' ')
                fields[:,:,i] = np.transpose(realPart) + 1j * np.transpose(imagPart)                
        return fields

    def __init__(self, fname):
        self.x = np.loadtxt('x.txt', dtype=float, delimiter=' ')
        self.y = np.loadtxt('y.txt', dtype=float, delimiter=' ')
        self.data_txt = np.loadtxt(fname, dtype = None, delimiter=',')
        self.data_txt[:,0]*=2*np.pi
        self.data_txt[:,1]*=2*np.pi
        self.data2 = np.array(self.data_txt)
        self.data2[:,[0,1]] = self.data_txt[:,[1,0]]
        self.eigenEnergies = np.append(self.data_txt, self.data2, axis=0)
        self.Ex = self.get_fields('Ex')
        self.Ey = self.get_fields('Ey')
        self.Ez = self.get_fields('Ez')
        self.Hx = self.get_fields('Hx')
        self.Hy = self.get_fields('Hy')
        self.Hz = self.get_fields('Hz')

        self.kx_grid, self.ky_grid = np.mgrid[0:np.pi:200j, 0:np.pi:200j]
        self.bandstructure = interpolate.griddata(self.eigenEnergies[:,0:2], self.eigenEnergies[:,2], (self.kx_grid, self.ky_grid), method='cubic') + 1j*interpolate.griddata(self.eigenEnergies[:,0:2], self.eigenEnergies[:,3], (self.kx_grid, self.ky_grid), method='cubic')
    
    def calc_fieldE(self, kx, ky):
        E_field = np.zeros((len(self.x[:,0]), len(self.x[0,:]), 3), dtype=complex)
        xi = (kx, ky)
        for i in range(len(self.x[:,0])):
            for j in range(len(self.y[0,:])):
                E_field[i, j, 0] = interpolate.griddata(self.eigenEnergies[:,0:2], self.Ex[i, j, :], xi, method='cubic')
                E_field[i, j, 1] = interpolate.griddata(self.eigenEnergies[:,0:2], self.Ey[i, j, :], xi, method='cubic')
                E_field[i, j, 2] = interpolate.griddata(self.eigenEnergies[:,0:2], self.Ez[i, j, :], xi, method='cubic')
        return E_field
    
    def calc_fieldH(self, kx, ky):
        H_field = np.zeros((len(self.x[:,0]), len(self.x[0,:]), 3), dtype=complex)
        xi = (kx, ky)
        for i in range(len(self.x[:,0])):
            for j in range(len(self.y[0,:])):
                H_field[i, j, 0] = interpolate.griddata(self.eigenEnergies[:,0:2], self.Hx[i, j, :], xi, method='cubic')
                H_field[i, j, 1] = interpolate.griddata(self.eigenEnergies[:,0:2], self.Hy[i, j, :], xi, method='cubic')
                H_field[i, j, 2] = interpolate.griddata(self.eigenEnergies[:,0:2], self.Hz[i, j, :], xi, method='cubic')
        return H_field

    def calc_energy(self, kx, ky):
        xi = (kx, ky)
        energy = interpolate.griddata(self.eigenEnergies[:,0:2], self.eigenEnergies[:,2], xi, method='cubic') + 1j*interpolate.griddata(self.eigenEnergies[:,0:2], self.eigenEnergies[:,3], xi, method='cubic')
        return energy

    # def calc_range(self, ):
    #     kxx, kyy, En0, gap_l = band(0.3, 0.3, 0)
    #     kxx, kyy, En1, gap_u = band(0.3, 0.3, 1)
    #     xmask = (np.logical_and(np.real(En0)<gap_u, np.real(En1)>gap_l)).all(axis=1)
    #     ymask = (np.logical_and(np.real(En0)<gap_u, np.real(En1)>gap_l)).all(axis=0)
    #     return kxx[:,ymask], kyy[:,ymask], En0[:,ymask], En1[:,ymask]
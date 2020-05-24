import numpy as np
from scipy import interpolate
from chern import Mode
from scipy.integrate import simps

def calc_range(bstruct0, bstruct1, kxx, kyy, gap_b, gap_u):
    xmask = (np.logical_and(np.real(bstruct0)<gap_u, np.real(bstruct1)>gap_b)).all(axis=1)
    ymask = (np.logical_and(np.real(bstruct0)<gap_u, np.real(bstruct1)>gap_b)).all(axis=0)
    return kxx[:,ymask], kyy[:,ymask], bstruct0[:,ymask], bstruct1[:,ymask]


if __name__ == "__main__":

    mode0 = Mode('TE_low.txt')
    mode1 = Mode('TE_up.txt')
    gap_b = mode0.calc_energy(0.5, 0)
    gap_u = mode1.calc_energy(0.5, 0)
    kx_mesh, ky_mesh, E0, E1 = calc_range(mode0.bandstructure, mode1.bandstructure, mode0.kx_grid, mode0.ky_grid, gap_b, gap_u)
    kx = np.linspace(np.min(kx_mesh), np.max(kx_mesh), 18)
    ky = np.linspace(np.min(ky_mesh), np.max(ky_mesh), 18)
    kxx, kyy = np.meshgrid(kx, ky)
    U12 = 0
    U23 = 0
    U34 = 0
    U41 = 0
    Berry = np.zeros((17,17), dtype=complex)
    dx = 1e-6
    dy = 1e-6
    for i in range(len(kx)-1):
        for j in range(len(ky)-1):
            ### U12 calc###
            temp1 = mode0.calc_fieldH(kx[i], ky[j])
            temp2 = mode0.calc_fieldH(kx[i+1], ky[j])
            exp1 = np.exp(kx[i]*mode0.x + ky[j]*mode0.y)
            exp2 = np.exp(kx[i+1]*mode0.x + ky[j]*mode0.y)
            temp1 = np.conj(exp1*temp1)
            temp2 = exp2*temp2
            temp3 = temp1[:,:,0]*temp2[:,:,0] + temp1[:,:,1]*temp2[:,:,1] + temp1[:,:,2]*temp2[:,:,2]
            U12 = simps(simps(temp3, mode0.x[0,:]*dx), mode0.y[:,0]*dy)
            ### U23 calc###
            temp1 = mode0.calc_fieldH(kx[i+1], ky[j])
            temp2 = mode0.calc_fieldH(kx[i+1], ky[j+1])
            exp1 = np.exp(kx[i+1]*mode0.x + ky[j]*mode0.y)
            exp2 = np.exp(kx[i+1]*mode0.x + ky[j+1]*mode0.y)
            temp1 = np.conj(exp1*temp1)
            temp2 = exp2*temp2
            temp3 = temp1[:,:,0]*temp2[:,:,0] + temp1[:,:,1]*temp2[:,:,1] + temp1[:,:,2]*temp2[:,:,2]
            U23 = simps(simps(temp3, mode0.x[0,:]*dx), mode0.y[:,0]*dy)
            ### U34 calc###
            temp1 = mode0.calc_fieldH(kx[i+1], ky[j+1])
            temp2 = mode0.calc_fieldH(kx[i], ky[j+1])
            exp1 = np.exp(kx[i+1]*mode0.x + ky[j+1]*mode0.y)
            exp2 = np.exp(kx[i]*mode0.x + ky[j+1]*mode0.y)
            temp1 = np.conj(exp1*temp1)
            temp2 = exp2*temp2
            temp3 = temp1[:,:,0]*temp2[:,:,0] + temp1[:,:,1]*temp2[:,:,1] + temp1[:,:,2]*temp2[:,:,2]
            U34 = simps(simps(temp3, mode0.x[0,:]*dx), mode0.y[:,0]*dy)
            ### U41 calc### 
            temp1 = mode0.calc_fieldH(kx[i], ky[j+1])
            temp2 = mode0.calc_fieldH(kx[i], ky[j])
            exp1 = np.exp(kx[i]*mode0.x + ky[j+1]*mode0.y)
            exp2 = np.exp(kx[i]*mode0.x + ky[j]*mode0.y)
            temp1 = np.conj(exp1*temp1)
            temp2 = exp2*temp2
            temp3 = temp1[:,:,0]*temp2[:,:,0] + temp1[:,:,1]*temp2[:,:,1] + temp1[:,:,2]*temp2[:,:,2]
            U41 = simps(simps(temp3, mode0.x[0,:]*dx), mode0.y[:,0]*dy)

            Berry[i, j] = U12*U23*U34*U41/(np.abs(U12)*np.abs(U23)*np.abs(U34)*np.abs(41))
    



    ### Chern Number calc ####

    ChernN = np.sum(np.imag(np.log(Berry)))
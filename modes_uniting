import numpy as np
def reading(name):
    mass=np.loadtxt(name, delimiter = ',')

    return mass

def main():
    modes = np.zeros((1,4),dtype=float)
    for rl in range(20,121,1):
        name='si_r_0_modes_%s.dat' % rl
        mass=reading(name)
        #print(mass)
        if mass.shape[0]==0:
            continue
        b=np.zeros((int(mass.size/3),1), dtype=mass.dtype)
        #print(np.shape(b))
        #print('------------')
        mass1=np.reshape(mass,((int(mass.size/3),3)))
        #print(np.shape(mass1))
        a=np.hstack((b,mass1))
        a[:,0]=rl/100
        modes=np.vstack((modes,a))
        print(modes)
    return modes
main()

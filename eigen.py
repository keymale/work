import numpy as np
import numpy.linalg as LA

a = np.array([[1,5],[3,7]])
b = np.array([[1,5,4],[3,7,2],[17,4,2]])

aeig_val, aeig_vec = LA.eig(a)
beig_val, beig_vec = LA.eig(b)

if __name__ == '__main__':
    print(aeig_val)
    print(aeig_vec)
    print(beig_val)
    print(beig_vec)
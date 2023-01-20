import numpy as np
import matplotlib.pyplot as plt



class P():
    def __init__(self, coord):
        self.T = lambda t: np.array([[t**3, t**2, t, 1]])
        self.B = np.array([[-1, 3, -3, 1],
                           [3, -6, 3, 0],
                           [-3, 0, 3, 0],
                           [1, 4, 1, 0]])/6
        self.R = P.iterate(coord)

    # @classmethod
    def iterate(list):
        def a(i):
            return [list[i-1], list[i], list[i+1], list[i+2]]
        return a


    def __call__(self,k,t_num=30):
        L = []
        for i in np.linspace(0,1, num=t_num):
            temp = list((self.T(i)@self.B).flatten())
            L.append(sum([temp[i]*np.array(self.R(k)[i]) for i in range(4)]))
        # print(self.R, L)
        return np.array(L)

    def tangent(self, k, t_num=30):
        T = lambda t: np.array([[t**2, t, 1]])
        B = np.array([[-1, 3, -3, 1],
                      [2, -4, 2, 0],
                      [-1, 0, 1, 0]])/2
        L = []
        for i in np.linspace(0,1, num=t_num):
            temp = list((T(i)@B).flatten())
            L.append(sum([temp[i]*np.array(self.R(k)[i]) for i in range(4)]))
        # print(self.R, L)
        return np.array(L)



if __name__ == "__main__":
    coord = [[0, 0],
            [1, 1.5],
            [1.5, 2.5,],
            [3, 3],
            [4, 1.5],
            [5, 2.3],
            [4.7, 3.3]]
    coord = ((-3/5, 0, 0),( -2/5.0, 4/5.0, 0), (2/5.0, -4/5.0, 0), (4/5.0, 4/5.0, 0))

    pi = P(coord)





    # print(B.shape, R(1).shape)
    # print(B@R(1))
    plt.plot(np.array(coord)[:,0], np.array(coord)[:,1], 'ro',label="original")
    plt.plot(np.array(coord)[:,0], np.array(coord)[:,1], label="original")
    def plot_pi(k):
        # x = np.linspace(k, k+3, 11)
        pk = pi(k)
        tan = pi.tangent(k, 10)
        # print(pk.shape)
        print(tan)
        plt.plot(pk[:,0], pk[:,1], 'b', label="linear interpolation")
        plt.plot(tan[:,0], tan[:,1], 'r', label="linear interpolation")

    # plot_pi(2)
    for i in [1]:
        plot_pi(i)
    plt.show()
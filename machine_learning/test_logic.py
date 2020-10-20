import numpy as np
import math
import matplotlib.pyplot as plt


def cross_entropy(y, t):
    N = len(y)
    L = (1 / N) * np.sum(-t * np.log(y) - (1 - t)*np.log(1 - y))
    return L


class neuron():
    '''
    u_s_j:s番目の入力ベクトルx‗sに対する、隠れ層j番目のニューロン活性
    y_s_j:s番目の入力ベクトルx‗sに対する、隠れ層j番目のニューロン出力
    w_j_i:入力層i番目のニューロンから隠れ層j番目のニューロンへのシナプスの重み
    sigma_s = y_s - t_s
    '''
    def __init__(self, w, t, eta = 0.001, alpha = 0.001, beta1 = 0.9, beta2 = 0.999, epsilon = 1e-8):
        self.w = w
        self.t = t
        self.eta = eta
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.cnt = 0
        self.m = 0
        self.v = 0
        self.N = len(t)
        self.b = np.random.randn(1)[0]

    def sigmoid(self):
        return 1/(1 + math.e**(-self.u))

    def dLdw(self):
        return (1 / self.N) * np.dot((self.y - self.t), self.x)

    def dLdb(self):
        return (1 / self.N)*np.sum(self.y - self.t)
    
    def spark(self, x):
        self.x = x
        self.u = np.dot(self.x, self.w) + self.b
        self.y = self.sigmoid()
        return self.y

    def adam(self, dLdw):
        self.m = self.beta1 * self.m + (1 - self.beta1) * (dLdw + self.alpha * self.w)
        self.v = self.beta2 * self.v + (1 - self.beta2) * (dLdw + self.alpha * self.w) ** 2
        mb = self.m / (1 - self.beta1 ** (self.cnt + 1))
        vb = self.v / (1 - self.beta2 ** (self.cnt + 1))
        self.w = self.w - self.eta * mb / (np.sqrt(vb) + self.epsilon)
        self.cnt += 1

    def rev_wb(self):
        #self.w = (1 - self.eta * alpha) * self.w - (self.eta * self.dLdw())
        self.adam(self.dLdw())
        self.b = self.b - (self.eta * self.dLdb())        


class hidden_neuron(neuron):
    def ReLU(self):
        return np.where(self.u <= 0, 0, self.u)

    def dReLU(self):
        return np.where(self.u <= 0, 0, 1)

    def dLdw(self, wj):
        sigma_s = self.y - self.t
        return (1 / self.N) * np.dot(sigma_s * wj * self.dReLU(),x)

    def dLdb(self, wj):
        sigma_s = self.y - self.t
        return (1 / self.N)*np.sum(sigma_s * wj * self.dReLU())

    def spark(self, x):
        self.x = x
        self.u = np.dot(self.x, self.w) + self.b
        self.y = self.ReLU()
        return self.y

    def rev_wb(self, wj):
        #self.w = (1 - eta * alpha) * self.w - (eta * self.dLdw(wj))
        self.adam(self.dLdw(wj))
        self.b = self.b - (eta * self.dLdb(wj))



if __name__ == "__main__":
    eta = 0.001
    epoc = 10000
    hidden_num = 16
    x = np.array(((0, 0),
         (0, 1),
         (1, 0),
         (1, 1)))
    t = np.array((0, 1, 1, 0))
    neuron_hid = [[] for _ in range(hidden_num)]
    y = [[] for _ in range(hidden_num)]    
    ans  = [[], [], [], []]
    for i in range(hidden_num):
        neuron_hid[i] = hidden_neuron(np.random.randn(2), t)
    neuron_out = neuron(np.random.randn(hidden_num), t)

    for i in range(epoc):
        for j in range(hidden_num):
            y[j] = neuron_hid[j].spark(x)
        yo = neuron_out.spark(np.stack([y[j]for j in range(hidden_num)], 1))
        for j in range(hidden_num):
            neuron_hid[j].rev_wb(neuron_out.w[j])
        neuron_out.rev_wb()
        for i in range(4):
            ans[i].append(yo[i])
    cnt = list(range(epoc))
    plt.plot(cnt,ans[0],label = "0")
    plt.plot(cnt,ans[1],label = "1")
    plt.plot(cnt,ans[2],label = "2")
    plt.plot(cnt,ans[3],label = "3") 
    plt.legend()       
    plt.show()
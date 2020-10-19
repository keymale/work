import numpy as np
import math
import matplotlib.pyplot as plt

def sigmoid(u):
    return 1/(1 + math.e**(-u))


def cross_entropy(y, t):
    N = len(y)
    L = (1 / N) * np.sum(-t * np.log(y) - (1 - t)*np.log(1 - y))
    return L


def ReLU(u):
    return np.where(u <= 0, 0, u)


def dReLU(u):
    return np.where(u <= 0, 0, 1)


def dLdw(y, t, x):
    N = len(t)
    nn = len(x[0])
    ans = []
    for i in range(nn):
        ans.append(np.sum((y - t) * x[:,i]))
    ans = (1 / N) * np.array(ans)
    return ans

def dLdw_hidden(y, t, x, wj, u):
    '''
    u_s_j:s番目の入力ベクトルx‗sに対する、隠れ層j番目のニューロン活性
    y_s_j:s番目の入力ベクトルx‗sに対する、隠れ層j番目のニューロン出力
    w_j_i:入力層i番目のニューロンから隠れ層j番目のニューロンへのシナプスの重み
    sigma_s = y_s - t_s
    
    '''
    N = len(t)
    nn = len(x[0])
    ans = []
    sigma_s = y - t
    for i in range(nn):
        ans.append(np.sum(sigma_s * wj * dReLU(u) * x[:,i]))
    ans = (1 / N) * np.array(ans)
    return ans


def dLdb(y, t):
    N = len(t)
    return (1 / N)*np.sum(y - t)


def dLdb_hidden(y, t, wj, u):
    N = len(t)
    sigma_s = y - t
    return (1 / N)*np.sum(sigma_s * wj * dReLU(u))


class neuron():
    def __init__(self, w):
        self.w = w
        self.b = 1
    
    def spark(self, x):
        self.x = x
        self.u = []
        for xx in self.x:
            self.u.append(np.dot(xx, self.w) + self.b)
        self.u = np.array(self.u)
        
        return self.u

    def spark_output(self, u):
        self.y = sigmoid(self.u)
        return self.y

    def rev_wb(self, t, eta, alpha = 0.0001):
        self.t = t
        self.w = (1 - eta * alpha) * self.w - (eta * dLdw(y = self.y, t = self.t, x = self.x))
        self.b = self.b - (eta * dLdb(y = self.y, t = self.t))        

class hidden_neuron(neuron):
    def spark_output(self, u):
        self.y = ReLU(self.u)
        return self.y

    def rev_wb(self, t, eta, wj, alpha = 0.0001):
        self.t = t
        self.w = (1 - eta * alpha) * self.w - (eta * dLdw_hidden(self.y, self.t, self.x, wj, self.u))
        self.b = self.b - (eta * dLdb_hidden(self.y, self.t, wj, self.u))



if __name__ == "__main__":
    x = np.array(((0, 0),
         (0, 1),
         (1, 0),
         (1, 1)))
    t = np.array((0, 1, 1, 0))
    hidden_num =12
    neuron_hid = [[] for _ in range(hidden_num)]
    u = [[] for _ in range(hidden_num)]
    y = [[] for _ in range(hidden_num)]
    eta = 0.001
    for i in range(hidden_num):
        neuron_hid[i] = hidden_neuron(np.random.randn(2))
    neuron_out = neuron(np.random.randn(hidden_num))

    ans  = [[], [], [], []]
    ans_u  = [[], [], [], []]
    epoc = 20000
    for i in range(epoc):
        for j in range(hidden_num):
            u[j] = neuron_hid[j].spark(x)
            y[j] = neuron_hid[j].spark_output(u[j])
        uo = neuron_out.spark(np.stack([y[j]for j in range(hidden_num)], 1))
        yo = neuron_out.spark_output(uo)
        for j in range(hidden_num):
            neuron_hid[j].rev_wb(t, eta, neuron_out.w[j])
        neuron_out.rev_wb(t, eta)
        for i in range(4):
            ans[i].append(yo[i])
            ans_u[i].append(uo[i])
    cnt = list(range(epoc))
    plt.plot(cnt,ans[0],label = "0")
    plt.plot(cnt,ans[1],label = "1")
    plt.plot(cnt,ans[2],label = "2")
    plt.plot(cnt,ans[3],label = "3") 
    plt.legend()       
    plt.show()
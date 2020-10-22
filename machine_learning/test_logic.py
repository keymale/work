import numpy as np
import math
import matplotlib.pyplot as plt


def cross_entropy(y, t):
    N = len(y)
    L = (1 / N) * np.sum(-t * np.log(y) - (1 - t)*np.log(1 - y))
    return L


class Neuron():
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

    def activation(self):
        return 1/(1 + math.e**(-self.u))

    def dLdw(self):
        return (1 / self.N) * np.dot((self.y - self.t), self.x)

    def dLdb(self):
        return (1 / self.N)*np.sum(self.y - self.t)
    
    def spark(self, x):
        self.x = x
        self.u = np.dot(self.x, self.w) + self.b
        self.y = self.activation()
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


class HiddenNeuron(Neuron):
    def activation(self):
        return np.where(self.u <= 0, 0, self.u)

    def dReLU(self):
        return np.where(self.u <= 0, 0, 1)

    def dLdw(self, wj):
        sigma_s = self.y - self.t
        return (1 / self.N) * np.dot(sigma_s * wj * self.dReLU(),x)

    def dLdb(self, wj):
        sigma_s = self.y - self.t
        return (1 / self.N)*np.sum(sigma_s * wj * self.dReLU())

    def rev_wb(self, wj):
        #self.w = (1 - eta * alpha) * self.w - (eta * self.dLdw(wj))
        self.adam(self.dLdw(wj))
        self.b = self.b - (self.eta * self.dLdb(wj))


class NeuronMulti(Neuron):
    def activation(self):
        return math.e**(self.x) / (np.sum(math.e**(self.x))

    def dLdw(self):
        self.sigma_sk = self.y - self.t
        return (1 / self.N) * np.dot(self.sigma_sk, self.y)

    def dLdb(self):
        return (1 / self.N)*np.sum(self.sigma_sk))


class HiddenNeuronMulti(HiddenNeuron):
    def dLdw(self, wj):
        sigma_s = self.y - self.t
        return (1 / self.N) * np.dot(sigma_s * wj * self.dReLU(),x)

    def dLdb(self, wj):
        sigma_s = self.y - self.t
        return (1 / self.N)*np.sum(sigma_s * wj * self.dReLU())


class NN1Output():
    def __init__(self, x, t, epoc, hidden_num = 16):
        self.hidden_num = hidden_num
        self.neuron_hid = [[] for _ in range(self.hidden_num)]
        self.x = x
        self.y = [[] for _ in range(self.hidden_num)]    
        self.t = t
        self.epoc = epoc
        self.ans_len = len(self.x)
        self.x_len = len(self.x[0])
        self.loss = []
        self.ans  = [[]for _ in range(self.ans_len)]
        for i in range(self.hidden_num):
            self.neuron_hid[i] = HiddenNeuron(np.random.randn(self.x_len), self.t)
        self.neuron_out = Neuron(np.random.randn(self.hidden_num), t)

    def study(self):
        fig, ax = plt.subplots(1, 1)
        
        for i in range(self.epoc):
            for j in range(self.hidden_num):
                self.y[j] = self.neuron_hid[j].spark(self.x)
            self.yo = self.neuron_out.spark(np.stack([self.y[j]for j in range(self.hidden_num)], 1))
            for j in range(self.hidden_num):
                self.neuron_hid[j].rev_wb(self.neuron_out.w[j])
            self.neuron_out.rev_wb()
            for k in range(self.ans_len):
                self.ans[k].append(self.yo[k])
            self.loss.append(np.sum(np.abs(self.yo - self.t)))
            if i % 100 == 0:
                line, = ax.plot(list(range(i+1)), self.loss,color = "blue")
                plt.pause(1e-9)
                line.remove()
        plt.plot(list(range(i+1)), self.loss,color = "blue")
        plt.show()
            


if __name__ == "__main__":
    x = np.array(((0, 0),
         (0, 1),
         (1, 0),
         (1, 1)))
    t = np.array((0, 1, 1, 0))
    epoc = 10000
    hidden_num = 16
    nn1out = NN1Output(x, t, epoc, hidden_num = 16)
    nn1out.study()
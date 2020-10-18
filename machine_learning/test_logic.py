import numpy as np
import math
import matplotlib.pyplot as plt

def sigmoid(u):
    return 1/(1 + math.e**(-u))


def cross_entropy(y, t):
    N = len(y)
    L = (1 / N) * np.sum(-t * np.log(y) - (1 - t)*np.log(1 - y))
    return L

def dLdw(y, t, x):
    N = len(t)
    nn = len(x[0])
    ans = []
    for i in range(nn):
        ans.append(np.sum((y - t) * x[:,i]))
    ans = (1 / N) * np.array(ans)
    return ans


def dLdb(y, t):
    N = len(t)
    return (1 / N)*np.sum(y - t)


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
        self.y = sigmoid(self.u)

        return self.y

    def rev_wb(self, t, eta):
        self.t = t
        self.w = self.w - (eta * dLdw(y = self.y, t = self.t, x = self.x))
        self.b = self.b - (eta * dLdb(y = self.y, t = self.t))        

if __name__ == "__main__":
    x = np.array(((0, 0),
         (0, 1),
         (1, 0),
         (1, 1)))
    t = np.array((0, 0, 1, 1))
    w = np.array((0.5, 0.5))
    eta = 0.1
    neuron1 = neuron(w)
    ans  = [[], [], [], []]
    epoc = 1000
    for i in range(epoc):
        y = neuron1.spark(x)
        neuron1.rev_wb(t, eta)
        for i in range(4):
            ans[i].append(y[i])
    cnt = list(range(epoc))
    plt.plot(cnt,ans[0],label = "0")
    plt.plot(cnt,ans[1],label = "1")
    plt.plot(cnt,ans[2],label = "2")
    plt.plot(cnt,ans[3],label = "3") 
    plt.legend()       
    plt.show()
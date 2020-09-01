import time
from functools import lru_cache

def fibonacci0(n):
    if n < 2:
        return n
    return fibonacci0(n - 1) + fibonacci0(n - 2)

memo = {0: 0, 1:1}
def fibonacci1(n):
    if n not in memo:
        memo[n] = fibonacci1(n - 1) + fibonacci1(n - 2)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci2(n):
    if n < 2:
        return n
    return fibonacci2(n - 1)+ fibonacci2(n - 2)


def fibonacci3(n):
    if n == 0:
        return n
    last = 0
    next = 1
    for _ in range(n-1):
        last, next = next, last + next
    return next
 

def fibonacci4(n):
    yield 0
    if n > 0: yield 1
    last = 0
    next = 1
    for _ in range(n-1):
        last, next = next, last + next
        yield next

def time_count(func,k):
    start = time.time()
    func(n=30)
    elapsed_time = time.time() - start
    print ("fibonacci"+str(k)+" elapsed_time:{0}".format(elapsed_time) + "[sec]")

if __name__=="__main__":
    time_count(fibonacci0,k=0)
    time_count(fibonacci1,k=1)
    time_count(fibonacci2,k=2)
    time_count(fibonacci3,k=3)
    for i in fibonacci4(10):
        print(i)
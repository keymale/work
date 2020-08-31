from typing import Dict
from functools import lru_cache
memo: Dict[int,int] = {0: 0, 1:1}# 基底部
def fib(n):
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)#memoliize
    return memo[n]

@lru_cache(maxsize=None)
def fib0(n):
    if n < 2:
        return n
    return fib0(n - 1)+ fib0(n - 2)


if __name__=="__main__":
    for i in range(10):
        print(fib0(i))
from typing import Dict
memo: Dict[int,int] = {0: 0, 1:1}# 基底部
def fib(n):
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)#memoliize
    return memo[n]

if __name__=="__main__":
    for i in range(10):
        print(fib(i))
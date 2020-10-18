n = int(input())
S = list(map(int,input().split()))
q = int(input())
T = list(map(int,input().split()))

ans = 0


for i in T:
    m = (len(S)-1)//2 
    mi = 0
    ma = len(S)-1
    while True:
        if mi > ma:
            break
        elif i == S[m]:
            ans += 1
            break
        elif i < S[m]:
            mi = mi
            ma = m -1
            m = (ma + mi)//2
        else:
            ma = ma
            mi = m + 1
            m = (ma + mi)//2
print(ans)

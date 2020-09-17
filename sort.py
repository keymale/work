def bubbleSort(A,N):
    flag = 1
    cnt = 0
    while flag:
        flag = 0
        for j in range(N-1,0,-1):
            if A[j] < A[j-1]:
                A[j], A[j-1] = A[j-1], A[j]
                cnt += 1
                flag = 1
    return A, cnt
                

def selectionSort(A, N):
    cnt = 0
    for i in range(N):
        minj = i
        for j in range(i, N):
            if A[j] < A[minj]:
                minj = j
        A[i], A[minj] = A[minj], A[i]
        if i != minj:
            cnt += 1
    return A, cnt


if __name__ == "__main__":
    N = int(input())
    A = list(map(int, input().split()))
    ans, cnt = selectionSort(A, N)
    print(' '.join(map(str, ans)))
    print(cnt)
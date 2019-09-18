from sys import stdin

rf = stdin
# rf = open('in.txt', mode='r')


if __name__ == '__main__':
    N = int(rf.readline())
    A = [int(j) for j in rf.readline().split()]
    l_max = [0]*N
    r_max = [0]*N

    l_max[0] = A[0]
    r_max[N-1] = A[N-1]

    for i in range(1, N):
        l_max[i] = max(l_max[i-1], A[i])
    for i in range(N-2, -1, -1):
        r_max[i] = max(r_max[i+1], A[i])

    for i in range(N):
        if i == 0 or i == N-1:
            print(i+1, end=' ')
        else:
            if min(l_max[i-1], A[i], r_max[i+1]) != A[i]:
                print(i+1, end=' ')

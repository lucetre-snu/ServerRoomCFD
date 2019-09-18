from sys import stdin
rf = stdin
# rf = open('in.txt', mode='r')

if __name__ == '__main__':
    N = int(rf.readline())
    arr = [int(j) for j in rf.readline().split()]
    pos = {}
    for i in range(N):
        pos[arr[i]] = i
    K = int(rf.readline())
    print(pos[K])

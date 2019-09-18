from sys import stdin
import math

rf = stdin
rf = open('in.txt', mode='r')


def monk_sort(arr, ind):
    h_mod = 10**(5*(ind+1))
    l_mod = 10**(5*ind)
    chunk = [(k, (k % h_mod)//l_mod) for k in arr]
    chunk.sort(key=lambda x: x[1])
    arr = [x[0] for x in chunk]
    return arr


if __name__ == '__main__':
    N = int(rf.readline())
    A = [int(j) for j in rf.readline().split()]
    for i in range(int(math.log10(max(A))/5+1)):
        A = monk_sort(A, i)
        for k in A:
            print(k, end=' ')
        print()

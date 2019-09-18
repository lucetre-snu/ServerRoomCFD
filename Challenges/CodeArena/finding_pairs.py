from sys import stdin

rf = stdin
# rf = open('in.txt', mode='r')


if __name__ == '__main__':
    T = int(rf.readline())
    for _ in range(T):
        N = int(rf.readline())
        A = [int(j) for j in rf.readline().split()]
        freq = {}
        for i in A:
            if i in freq.keys():
                freq[i] += 1
            else:
                freq[i] = 1

        result = 0
        for (k, v) in freq.items():
            result += (v*(v-1)) // 2
        print(result + N)

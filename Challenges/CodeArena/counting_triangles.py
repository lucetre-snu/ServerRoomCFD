from sys import stdin

rf = stdin
# rf = open('in.txt', mode='r')


if __name__ == '__main__':
    n = int(rf.readline())
    triangles = {}
    for _ in range(n):
        sides = [int(j) for j in rf.readline().split()]
        sides = tuple(sorted(sides))
        if sides in triangles.keys():
            triangles[sides] += 1
        else:
            triangles[sides] = 1
    result = 0
    for (k, v) in triangles.items():
        if v == 1:
            result += 1
    print(result)

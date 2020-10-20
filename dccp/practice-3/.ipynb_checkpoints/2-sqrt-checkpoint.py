a = float(input())
x = float(input())
eps = float(input())

while (x*x-a)/a <= -eps or (x*x-a)/a >= eps:
    print(format(x, '.12f'))
    x = 1/2 *(x + a/x)
print(format(x, '.12f'), end='')
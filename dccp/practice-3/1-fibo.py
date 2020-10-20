f_prev = 0
f_curr = 0
f_next = 1

n = int(input())
for i in range(n):
    f_prev = f_curr
    f_curr = f_next
    f_next = f_prev + f_curr

print(f_curr)

N = int(input("Number to be factored: "))
g = int(input("guess: "))
r = 1
rem = 0
while True:
    rem = (g**r)%N

    if rem == 1:
        break
    else:
       r = r + 1


a = (g**(r/2)+1)
b = (g**(r/2)-1)

x = N
while True:
    remain = a%x

    if remain == 0:
        break
    else:
       a = x
       x = remain

p = int(x)
q = int(N/x)
print("Factors are", p, q)

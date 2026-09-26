 

n=int(input("Enter the Number"))
def collatz(n):
    steps=0
    while n!=1:
        if n%2==0:
         n=n//2
        else:
           n = 3 * n + 1 
        steps+=1
    return steps

print(collatz(n)) 

    
max_steps = 0
number = 0

for i in range(1, 10000):
    steps = collatz(i)

    if steps > max_steps:
        max_steps = steps
        number = i

print("Starting number:", number)
print("Collatz steps:", max_steps)
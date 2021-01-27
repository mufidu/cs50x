from cs50 import get_float

dollar = get_float("Change owed: ")

while dollar <= 0:
    print("Sorry, invalid.")
    dollar = get_float("Change owed: ")
    
cents = round(dollar*100, 0)

n = 0

if cents >= 25:
    n += cents // 25
    cents = cents % 25

if cents < 25 and cents >= 10:
    n += cents // 10
    cents = cents % 10
    
if cents < 10 and cents >= 5:
    n += cents // 5
    cents = cents % 5
    
if cents < 5 and cents >= 1:
    n += cents

print(f"{int(n)}")
    
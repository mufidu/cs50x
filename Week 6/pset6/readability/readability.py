from cs50 import get_string

text = get_string("Text: \n")

letters = 0
words = 0
sentences = 0

for letter in text:
    if 90 >= ord(letter) >= 65 or 122 >= ord(letter) >= 97:
        letters += 1
        
for letter in text:
    if ord(letter) == 32:
        words += 1
        
for letter in text:
    if ord(letter) == 33 or ord(letter) == 46 or ord(letter) == 63:
        sentences += 1

l = letters * 100 / words
s = sentences * 100 / words

# Coleman-Liau index
index = round(0.0588 * l - 0.296 * s - 15.8)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
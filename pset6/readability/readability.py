from cs50 import get_string
s = get_string("Text: ")
letters = 0
words = 1
sentences = 0
for c in s:
    if c.islower():
        letters += 1
    if c.isupper():
        letters += 1
    if c.isspace():
        words += 1
    if c == '.' or c == '!' or c == '?':
        sentences += 1

L = float(letters * 100) / float(words)
S = float(sentences * 100) / float(words)
index = 0.000
index = (0.0588 * float(L)) - (0.296 * float(S)) - 15.8
if index >= 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(index)}")

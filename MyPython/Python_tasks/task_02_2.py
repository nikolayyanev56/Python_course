def number_of_vowels(string):
    vowels = "aeiou"
    num = 0
    for char in string.lower():
        if char in vowels:
            num += 1
    return num

print(number_of_vowels("grrrrgh!") == 0)
print(number_of_vowels("The quick brown fox jumps over the lazy dog.") == 11)
print(number_of_vowels("MONTHY PYTHON") == 2)
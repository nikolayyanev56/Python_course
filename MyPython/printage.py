#printing is done in several ways:

# % formatting like C
print('I dont %s this %s' % ("like","way"))

# str.format() for Python 2.7+
print("Here is a number: {}, and a tupple: {} formatted".format(56,(4,5,7)))

# with the new f-string since Python 3.6
name = "Nick"
print(f"My name is {name}")

#you can do this if you want to print the name and value of a variable
print(f"{name = }")
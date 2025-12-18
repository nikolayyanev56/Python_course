#here's a comment

#integer
num = 1
print(f"var {num = } is a {type(num)}")

#string
word = "hello"
print(f"var {word = } is a {type(word)}")

#float
oiler = 2.7127182818284
print(f"var {oiler = } is a {type(oiler)}")

#complex (fancy!)
imaginary_num = 3 + 4j
print(f"var {imaginary_num = } is a {type(imaginary_num)}")

#bytes 
little_byte = b'weeeeee'
print(f"var {little_byte = } is a {type(little_byte)}")

#boolean , 
false_bool = True
print(f"var {false_bool = } is a {type(false_bool)}")

# tuple - ordered collection, allows duplicates, immutable
some_tupple = (2,3,5,7,12)
print(f"var {some_tupple = } is a {type(some_tupple)}")

# list - ordered collection, allows duplicates, mutable
random_list = [6,4,2,8,9]
print(f"var {random_list = } is a {type(random_list)}")

# set - collection of unique items (does't have duplicates!), mutable
here_be_a_set = {5,4,2,7,7,7,0}
print(f"var {here_be_a_set = } is a {type(here_be_a_set)}")

# dictionary - associate keys to values, mutable
smol_dict = {"item1": "first item","item2": "second item","item3": "third item"}
print(f"var {smol_dict = } is a {type(smol_dict)}")

# Technically all types are objects/classes
print(f"even type has a type : {type(type)}")

# also there's a NoneType
nothing = None
print(f"var {nothing = } is a {type(nothing)}")
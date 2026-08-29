# Python Articles

---

# Article 1: Python Variables and Data Types

## Introduction

When you start learning Python, one of the very first things you need to understand is how the language stores information. This is done through **variables**. A variable is simply a name that points to a value stored in the computer's memory. Along with variables, Python has several built-in **data types** that describe what kind of value is being stored, such as numbers, text, or collections of items. Understanding variables and data types is the foundation for everything else you will learn in Python, including strings, lists, tuples, and dictionaries, which are covered in later articles in this series.

## Main Concepts

In Python, you do not need to declare the type of a variable before using it. Python figures out the type automatically based on the value you assign. This is called **dynamic typing**. For example, if you write `age = 25`, Python knows that `age` is an integer without you having to say so explicitly.

Python has several core built-in data types:

- **int**: whole numbers, like `10` or `-3`
- **float**: decimal numbers, like `3.14` or `-0.5`
- **str**: text, called a string, like `"hello"`
- **bool**: `True` or `False` values
- **list**: an ordered, changeable collection of items
- **tuple**: an ordered, unchangeable collection of items
- **dict**: a collection of key-value pairs

A very important concept connected to data types is **mutability**. A mutable object can be changed after it is created, while an immutable object cannot. Numbers, strings, and tuples are immutable in Python. Lists and dictionaries are mutable, meaning you can add, remove, or change their contents after creation. This distinction becomes very important once you start working with more complex data structures.

## Examples

Here is a simple example that shows different variable types being created:

```python
name = "Alice"          # str
age = 30                 # int
height = 1.65            # float
is_student = False       # bool
fruits = ["apple", "banana", "cherry"]   # list
coordinates = (10, 20)   # tuple
person = {"name": "Alice", "age": 30}    # dict

print(type(name))
print(type(fruits))
```

You can check the type of any variable using the built-in `type()` function, as shown above. This is useful when you are not sure what kind of data you are working with, especially when debugging.

Variables can also be reassigned to new values, even of a different type:

```python
value = 10
print(value)       # 10
value = "now I'm a string"
print(value)       # now I'm a string
```

This flexibility is part of what makes Python beginner-friendly, but it can also lead to confusion if you are not careful about what type of data your variable currently holds.

## Common Operations

Some common operations you will perform with variables include assignment, reassignment, and type conversion. Type conversion, also called **type casting**, lets you convert one data type into another using functions like `int()`, `float()`, `str()`, and `list()`.

```python
age_str = "25"
age_int = int(age_str)     # converts string to integer
price = 19.99
price_str = str(price)     # converts float to string
```

You can also perform basic arithmetic on numeric types, and concatenation or repetition on strings, which behaves similarly to how it works on lists and tuples, since strings are also ordered sequences.

## Comparison With Related Python Concepts

Variables themselves are not a data structure, but they are the containers that hold every data structure you will learn about. A string is a sequence of characters, a list is a mutable ordered collection, a tuple is an immutable ordered collection, and a dictionary maps keys to values. All of these are objects with a type, and understanding the difference between mutable and immutable types will help you avoid many common bugs later, especially when you start passing lists or dictionaries into functions and unexpectedly modifying them.

## Common Mistakes

A very common mistake beginners make is assuming that all data types behave the same way when copied or modified. For example, copying a list does not always create a fully independent copy:

```python
list_a = [1, 2, 3]
list_b = list_a
list_b.append(4)
print(list_a)   # [1, 2, 3, 4] - list_a changed too!
```

This happens because `list_a` and `list_b` point to the same mutable object in memory. Immutable types like integers, strings, and tuples do not have this problem, because any "change" actually creates a brand new object instead of modifying the original.

Another common mistake is trying to combine incompatible types, such as adding a string and an integer directly, which raises a `TypeError`.

## Practical Use Cases

Variables and data types are used in literally every Python program. Numbers are used for calculations, strings for storing names and messages, booleans for decision-making, lists for grouping related items, tuples for fixed collections of values like coordinates, and dictionaries for structured records like user profiles. Choosing the correct data type for your data is one of the most important decisions you make when designing a program, because it affects both performance and how easily you can update your data later.

## Conclusion

Variables and data types form the building blocks of every Python program. Understanding how Python assigns types automatically, and knowing the difference between mutable types like lists and dictionaries versus immutable types like strings and tuples, will prepare you well for the more detailed articles ahead. In the next articles, we will explore strings, lists, tuples, and dictionaries in much greater depth.

---

# Article 2: Python Strings

## Introduction

Strings are one of the most commonly used data types in Python. A string is simply a sequence of characters used to represent text, such as a name, a sentence, or even a whole paragraph. Because strings are so central to programming, Python provides a rich set of tools for creating, modifying, and analyzing them. In this article, we will explore what strings are, how they behave as sequences, why they are immutable, and how they compare to another ordered collection type: lists.

## Main Concepts

In Python, a string is created by wrapping text in either single quotes or double quotes:

```python
greeting = "Hello, world!"
name = 'Alice'
```

A key concept to understand is that strings are **sequences**, just like lists and tuples. This means each character in a string has a position, called an index, starting at 0. You can access individual characters using indexing, and you can access a range of characters using slicing.

Another essential concept is that strings are **immutable**. Once a string is created, its contents cannot be changed. Any operation that appears to modify a string actually creates a brand-new string object instead.

## Examples

Here is how indexing and slicing work with strings:

```python
word = "Python"
print(word[0])      # P
print(word[-1])     # n
print(word[0:3])    # Pyt
print(word[::-1])   # nohtyP (reversed string)
```

Because strings are immutable, trying to change a single character directly will raise an error:

```python
word = "Python"
word[0] = "J"   # This raises a TypeError
```

Instead, to "change" a string, you must create a new one:

```python
word = "Python"
new_word = "J" + word[1:]
print(new_word)   # Jython
```

Strings also support many built-in methods for common text processing tasks:

```python
text = "  Hello, World!  "
print(text.strip())        # "Hello, World!"
print(text.lower())        # "  hello, world!  "
print(text.replace("World", "Python"))
print(text.split(","))     # ['  Hello', ' World!  ']
```

## Common Operations

Common string operations include concatenation (joining strings together with `+`), repetition (`"ab" * 3` produces `"ababab"`), and membership testing using the `in` keyword. You can also loop through a string character by character, just as you would loop through a list:

```python
for char in "cat":
    print(char)
```

The `len()` function works on strings the same way it works on lists and tuples, returning the number of characters:

```python
print(len("hello"))   # 5
```

Formatting strings is another very common operation, often done using f-strings:

```python
name = "Alice"
age = 30
message = f"{name} is {age} years old."
print(message)
```

## Comparison With Related Python Concepts

Strings and lists share a lot of similarities because they are both ordered sequences that support indexing, slicing, and iteration. However, there is a critical difference: strings are immutable, while lists are mutable. This means you can change individual elements of a list in place, but you cannot do the same with a string.

```python
my_list = ["c", "a", "t"]
my_list[0] = "b"       # works fine, list becomes ["b", "a", "t"]

my_string = "cat"
my_string[0] = "b"     # raises TypeError, strings can't be changed
```

Another difference is what they typically store: strings hold only characters (text), while lists can hold any type of object, including numbers, other lists, or even dictionaries. You can convert between the two using `list("cat")`, which produces `['c', 'a', 't']`, and `"".join(["c", "a", "t"])`, which produces `"cat"`.

## Common Mistakes

A very common beginner mistake is trying to modify a string in place, forgetting that strings are immutable. Another common mistake is confusing single characters with one-character strings, since Python does not have a separate character type—a single character is just a string of length 1. Beginners also sometimes forget that string indexing starts at 0, leading to off-by-one errors, and they may forget that slicing with `word[0:3]` does not include the character at index 3.

## Practical Use Cases

Strings are used everywhere in real-world programming: reading user input, processing text files, building messages for users, parsing data from web APIs, and validating input formats like email addresses. Any time your program deals with human-readable text, you are working with strings.

## Conclusion

Strings are immutable sequences of characters that share many behaviors with lists, such as indexing, slicing, and iteration, but cannot be modified in place. Understanding the sequence nature of strings, along with their immutability, will help you avoid common bugs and prepares you for understanding lists, which behave similarly but allow modification, covered in detail in the next article.

---

# Article 3: Python Lists

## Introduction

Lists are one of the most flexible and widely used data structures in Python. A list is an ordered collection of items that can be changed after it is created, which makes it very different from immutable sequences like strings and tuples. In this article, we will look at how lists work, how to perform common operations on them, and how they compare to tuples, which are their immutable counterpart.

## Main Concepts

A list in Python is created using square brackets, with items separated by commas:

```python
fruits = ["apple", "banana", "cherry"]
```

Lists are **ordered**, meaning the items keep the position you place them in, and each item can be accessed using an index, just like with strings. Lists are also **mutable**, meaning you can change, add, or remove items after the list has been created. This is one of the biggest differences between lists and both strings and tuples, which cannot be changed once created.

A single list can hold items of different data types, including other lists, which are called nested lists:

```python
mixed = [1, "two", 3.0, [4, 5]]
```

## Examples

Here are some basic list operations:

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])        # apple
print(fruits[-1])       # cherry

fruits.append("orange")     # add an item to the end
fruits.remove("banana")     # remove a specific item
fruits[0] = "kiwi"          # change an item in place

print(fruits)   # ['kiwi', 'cherry', 'orange']
```

You can also slice a list to get a sub-list, using the same syntax as strings:

```python
numbers = [10, 20, 30, 40, 50]
print(numbers[1:4])   # [20, 30, 40]
```

Looping through a list is a very common pattern:

```python
for fruit in fruits:
    print(fruit)
```

## Common Operations

Common list operations include appending items with `.append()`, inserting at a specific position with `.insert()`, removing items with `.remove()` or `.pop()`, sorting with `.sort()`, and reversing with `.reverse()`. The `len()` function returns the number of items, just as it does for strings and tuples.

```python
numbers = [5, 3, 1, 4, 2]
numbers.sort()
print(numbers)    # [1, 2, 3, 4, 5]

numbers.append(6)
numbers.pop(0)
print(numbers)    # [2, 3, 4, 5, 6]
```

List comprehensions are a powerful and very "Pythonic" way to build new lists:

```python
squares = [x * x for x in range(5)]
print(squares)   # [0, 1, 4, 9, 16]
```

## Comparison With Related Python Concepts

Lists and tuples are extremely similar in that they are both ordered sequences that can store items of any type, including mixed types. The key difference is **mutability**: lists can be changed after creation, while tuples cannot.

```python
my_list = [1, 2, 3]
my_list[0] = 100      # allowed

my_tuple = (1, 2, 3)
my_tuple[0] = 100      # raises TypeError, tuples are immutable
```

Because lists are mutable, they are generally used when you expect the collection of items to change over time, such as a shopping cart or a list of active users. Tuples, on the other hand, are often used for fixed collections of related values, such as coordinates or RGB color values, where you do not want the data to accidentally change.

Lists also differ from dictionaries: a list stores items in order and accesses them by numeric index, while a dictionary stores items as key-value pairs and accesses them by key rather than position.

## Common Mistakes

One common mistake is confusing list copying with list referencing, as shown in the earlier article on variables—assigning one list to another variable does not create an independent copy. To make a true copy, you should use `.copy()` or the `list()` constructor.

```python
original = [1, 2, 3]
copy_of_list = original.copy()
copy_of_list.append(4)
print(original)   # [1, 2, 3] - unaffected
```

Another common mistake is trying to modify a list while iterating over it, which can produce unexpected results. Beginners also sometimes confuse `.remove()`, which removes a value, with `.pop()`, which removes an item by index.

## Practical Use Cases

Lists are used constantly in real Python programs: storing collections of user input, holding results from a database query, managing to-do items, and building up data before processing it further. Because lists are mutable and flexible, they are often the default choice when you need a collection of items that might grow, shrink, or change over the life of a program.

## Conclusion

Lists are ordered, mutable collections that can hold items of any type, including other lists. Their flexibility makes them one of the most commonly used data structures in Python, but that same mutability requires care when copying or sharing lists between variables. In the next article, we will look closely at tuples, the immutable sibling of lists, and explore when you should choose one over the other.

---

# Article 4: Python Tuples

## Introduction

Tuples are another fundamental ordered data structure in Python, closely related to lists but with one major difference: tuples are **immutable**. Once a tuple is created, its contents cannot be changed. This article explains how tuples work, when to use them, and how they compare to lists, which were covered in the previous article.

## Main Concepts

A tuple is created using parentheses, with items separated by commas:

```python
coordinates = (10, 20)
colors = ("red", "green", "blue")
```

Like lists, tuples are **ordered**, meaning each item has a fixed position that can be accessed using an index. Unlike lists, tuples are **immutable**, so once you create a tuple, you cannot add, remove, or change its items. This makes tuples useful for representing data that should not change during the life of a program, such as fixed coordinates or configuration values.

Interestingly, a tuple can contain mutable objects, such as lists, inside it. The tuple itself cannot be changed, but a mutable object stored inside the tuple can still be modified:

```python
data = (1, 2, [3, 4])
data[2].append(5)
print(data)   # (1, 2, [3, 4, 5])
```

This is an important and often surprising detail: immutability of a tuple only means the tuple cannot be reassigned to point to different objects—it does not freeze the mutable objects stored inside it.

## Examples

Basic tuple access works just like it does with lists and strings:

```python
point = (3, 7)
print(point[0])    # 3
print(point[1])    # 7
```

Trying to change a tuple's contents directly raises an error:

```python
point = (3, 7)
point[0] = 100   # raises TypeError
```

Tuples are often used for **unpacking**, a very common and convenient Python pattern:

```python
point = (3, 7)
x, y = point
print(x)   # 3
print(y)   # 7
```

You can also create a tuple with a single item, but you must include a trailing comma:

```python
single = (5,)     # this is a tuple
not_a_tuple = (5)  # this is just an integer in parentheses
```

## Common Operations

Because tuples are immutable, they support fewer operations than lists. You can still use `len()` to get the number of items, use indexing and slicing to access items, use `in` to check membership, and loop through a tuple with a `for` loop:

```python
sizes = ("small", "medium", "large")
print(len(sizes))          # 3
print("medium" in sizes)   # True

for size in sizes:
    print(size)
```

Tuples also support counting and finding the index of an item, using `.count()` and `.index()`, similar to lists.

## Comparison With Related Python Concepts

The most important comparison is between tuples and lists. Both are ordered sequences, and both can hold mixed data types. The core difference is that tuples cannot be modified after creation, while lists can. Because of this, tuples are generally faster and use slightly less memory than lists, and they are considered safer to use when you want to guarantee that data will not accidentally change.

```python
# Good use of a tuple: fixed coordinate that shouldn't change
location = (12.9716, 77.5946)

# Good use of a list: a collection that will grow over time
visited_cities = ["Bengaluru", "Mumbai"]
visited_cities.append("Delhi")
```

Tuples are also commonly used as dictionary keys, because dictionary keys must be immutable. Lists cannot be used as dictionary keys for this exact reason, but tuples can, as long as everything inside the tuple is also immutable.

## Common Mistakes

A common mistake is forgetting the trailing comma when creating a single-item tuple, which results in a regular value rather than a tuple. Another common mistake is assuming that a tuple is completely unchangeable, forgetting that mutable objects stored inside a tuple, like a nested list, can still be modified. Beginners also sometimes try to use list methods like `.append()` or `.remove()` on tuples, which do not exist because tuples do not support in-place modification.

## Practical Use Cases

Tuples are commonly used to represent fixed collections of related values, such as geographic coordinates, RGB colors, or database records returned from a query. They are also frequently used for function return values when a function needs to return multiple pieces of data at once, and as immutable keys in dictionaries when you need to map a combination of values to a single result.

## Conclusion

Tuples are ordered, immutable sequences that are closely related to lists but cannot be changed after creation. This immutability makes them a safer choice for fixed data and allows them to be used as dictionary keys, something lists cannot do. In the final article of this series, we will look at dictionaries, which use keys—often tuples or strings—to map to values.

---

# Article 5: Python Dictionaries

## Introduction

Dictionaries are one of the most powerful and widely used data structures in Python. Unlike lists and tuples, which store items in a simple order accessed by numeric index, a dictionary stores data as **key-value pairs**, where each unique key maps to a specific value. This article explains how dictionaries work, how they compare to lists and tuples, and when you should choose a dictionary over other data structures.

## Main Concepts

A dictionary is created using curly braces, with each key and value separated by a colon:

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "Bengaluru"
}
```

Dictionaries are **mutable**, meaning you can add, remove, or change key-value pairs after the dictionary is created. Unlike lists, dictionaries do not use numeric positions to access items—instead, you use the key itself.

An important rule in Python is that dictionary keys must be **immutable** types, such as strings, numbers, or tuples. This is because keys are stored using a mechanism called hashing, which requires the key's value to never change. Lists cannot be used as dictionary keys because they are mutable, but tuples can be used as keys, as long as every item inside the tuple is also immutable.

```python
locations = {
    (12.97, 77.59): "Bengaluru",
    (19.07, 72.87): "Mumbai"
}
```

## Examples

Here is how you access, add, and update values in a dictionary:

```python
person = {"name": "Alice", "age": 30}

print(person["name"])     # Alice
person["age"] = 31        # update an existing value
person["city"] = "Bengaluru"   # add a new key-value pair

print(person)
```

Trying to access a key that does not exist raises an error, so it is common to use the `.get()` method, which returns `None` or a default value instead of crashing:

```python
print(person.get("country"))              # None
print(person.get("country", "Unknown"))   # Unknown
```

You can loop through a dictionary's keys, values, or both:

```python
for key, value in person.items():
    print(key, "->", value)
```

## Common Operations

Common dictionary operations include adding or updating a key with square-bracket assignment, removing a key with `.pop()` or the `del` keyword, checking whether a key exists using `in`, and getting all keys or values using `.keys()` and `.values()`.

```python
person = {"name": "Alice", "age": 30}

print("name" in person)     # True
person.pop("age")
print(person)                # {'name': 'Alice'}

print(list(person.keys()))     # ['name']
print(list(person.values()))   # ['Alice']
```

Dictionary comprehensions, similar to list comprehensions, let you build dictionaries concisely:

```python
squares = {x: x * x for x in range(5)}
print(squares)   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## Comparison With Related Python Concepts

Dictionaries differ from lists and tuples in a fundamental way: lists and tuples are accessed by numeric position, while dictionaries are accessed by key. This makes dictionaries the better choice when you need to look up values by a meaningful label rather than by their position in a sequence.

```python
# List: access by position
scores_list = [90, 85, 78]
print(scores_list[0])    # 90, but you must remember what index 0 means

# Dictionary: access by meaningful key
scores_dict = {"Alice": 90, "Bob": 85, "Charlie": 78}
print(scores_dict["Alice"])   # 90, clearly labeled
```

Like lists, dictionaries are mutable, so you can change their contents after creation. Like tuples, dictionary keys must be immutable, which is why strings, numbers, and tuples are valid keys but lists are not. In terms of structure, a dictionary can be thought of as a more descriptive alternative to a list of tuples, where each tuple would have been a key-value pair.

## Common Mistakes

A common mistake is trying to use a mutable object, like a list, as a dictionary key, which raises a `TypeError` because lists are unhashable. Another common mistake is accessing a key directly with square brackets without checking whether it exists first, which raises a `KeyError` if the key is missing—using `.get()` avoids this problem. Beginners sometimes also confuse dictionary values, which can be duplicated, with dictionary keys, which must always be unique within a single dictionary.

## Practical Use Cases

Dictionaries are extremely common in real-world Python programs. They are used to represent structured records, such as a user profile with fields like name, age, and email. They are used to count occurrences of items, such as counting how many times each word appears in a document. They are also commonly used to store configuration settings, and to represent data received from web APIs, which is very often formatted as key-value pairs similar to a Python dictionary.

## Conclusion

Dictionaries are mutable collections that map unique, immutable keys to values, making them ideal for structured, labeled data. Unlike lists and tuples, which rely on numeric position, dictionaries let you access data by meaningful keys, and their requirement that keys be immutable connects directly back to the concepts of mutability and immutability introduced throughout this series. Together, these five articles—covering variables and data types, strings, lists, tuples, and dictionaries—provide a solid foundation for understanding how Python stores and organizes data.

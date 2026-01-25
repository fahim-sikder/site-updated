---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Julia Tutorial Part 1: Installations & Basics"
subtitle: ""
summary: ""
authors: ["Md Fahim Sikder"]
tags: ["Julia", "Tutorial","Installations", "Basics"]
categories: ["Tutorial","Julia Tutorial"]
date: 2020-07-08T14:24:00+06:00
lastmod: 2020-07-08T14:24:00+06:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: "Image Source: Google"
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---
## Introduction, Installations, and Basics

`Julia` is a open source programming language. It was designed from the beginning for high [performance](https://julialang.org/benchmarks/). Julia programs compile to efficient native code for multiple platforms via LLVM. To install it we need to download it's binary from [here](https://julialang.org/downloads/). We are going to use `Jupyter Notebook` as the code editor. But to do that we need to link the `Jupyter Notebook` with `Julia`. After installing `Julia`, open the Julia Command prompt with administration rights. Then type the following code:

```julia

using Pkg
Pkg.add("IJulia")


```

These will integrate `Julia` environment with `Jupyter Notebbok`.

N.B: We are assuming that your system has already Jupyter notebook installed.


`Julia` file has `.jl` extensions. It's time to write our first program. We will print `Hello Julia!`. The print function in `julia` is `println`.

##### _input_
```julia
println("Hello Julia!")
```
##### _output_
    Hello Julia!
    

Congratulations! We have just run your first program in `Julia`. 

### Variables & Data Types

`Julia` support 5 basic data types. 

1. Integer
2. Float
3. String
4. Character
5. Boolean

We can easily declare a variable just assigining the value in it. We don't need to give the datatype when declaring a variable. Also we can see what is the datatype of a variable by using `typeof` function. Lets see an example.

##### _input_
```julia
first = 1

println(typeof(first))

second = 22.0

println(typeof(second))

third = true
println(typeof(third))

fourth = "Hello World!"
println(typeof(fourth))

fifth = 'L'
println(typeof(fifth))
```
##### _output_
    Int64
    Float64
    Bool
    String
    Char
    

`String` needs to be in double quotes or triple quotes. If we put `String` in single quote, it will show error. Only `Character` will be in single quote.

##### _input_
```julia
#This is an intenional error

strr = 'Hello world'
println(strr)
```
##### _output_

    syntax: invalid character literal

    


### Constant

To declare a constant we need to use `const` keyword. After defining a constant we can redefine it, but it will give us a warning. We only can redefine in the same datatype. Suppose: we created a constant with integer datatype with a value, so we can redefine it with another integer value though it will give a warning, but we can not redefine with another datatype. It will give an error.

##### _input_
```julia
const var1 = 2
println(var1)
var1 = 3
println(var1)

#this will give error
var1 = 4.9
println(var1)
```
##### _output_
    2
    3
    

    WARNING: redefining constant var1
    


    invalid redefinition of constant var1

    

    Stacktrace:

     [1] top-level scope at In[4]:5


### Strings

As we have mentioned earlier, `String` needs to be in double or triple quotes.

```julia
mystr = "Hey this is a string"

mystr2 = """
    this is a multiple line string
    this string has 2 lines
    """

```

We can see the length of a string using the `length` function.

##### _input_
```julia
mystr = "Hey this is a string"

println(length(mystr))
```
##### _output_
    20
    

#### Taking seperate characters from string

We can access seperate characters from the string using index. Here we need to keep in mind that, unlike other programming language, `Julia` access its first character from a string using index 1. Suppose in `mystr` we want access the first character `H` , so we need to access it using `mystr[1]`. Now, if we want to access the last character of a string we need to use the `end` keyword. So, in `mystr` the last character is `g` and we can access it by using `mystr[end]`.

##### _input_
```julia
println(mystr[1])
println(mystr[end])
```
##### _output_
    H
    g
    

#### Substring

We also can get a substring from a string by slicing it. To do that we need to use `:` this. Suppose we want `this` as substring from `mystr` string. So, `this` started from index number `5` and ended in index number `8`. Then we need to access it using `mystr[5:8]`.

##### _input_
```julia
println(mystr[5:8])
```
##### _output_
    this
    

#### String Concatenation

To concatenate one string with another we need to use `*` keyword. Suppose we have two strings. `str1 = "Hello"` and `str2 = "World"`. We can merge them like this:

##### _input_
```julia
str1 = "Hello"
str2 = "World"

println(str1 * ", " * str2)
```
##### _output_
    Hello, World
    

Thats it for this tutorial.

Good Luck, and May the Julia be with you!

-------------------------------------------------------------------------------------------

**Other posts in this series:**

1. [Julia Tutorial Part 2: Data Structures]({{< ref "/post/Julia-Tutorial-Part-2-Data-Structures/index.md" >}})
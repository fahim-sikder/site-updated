---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Julia Tutorial Part 2: Data Structures"
subtitle: ""
summary: ""
authors: ["Md Fahim Sikder"]
tags: ["Julia", "Tutorial","Data", "Structures"]
categories: ["Tutorial","Julia Tutorial"]
date: 2020-07-30T10:50:26+06:00
lastmod: 2020-07-30T10:50:26+06:00
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
## Data Structures

In this tutorial, we will see `Julia's` data structure. Namely,

1. Tuple,
2. Array,
3. Dictionary, and
4. Set


### Tuple

Lets first discuss about `Tuple`. Tuple and Array can hold a list of elements. But the basic difference between them is, `Tuple` is immutable. It means that, we can't change the value of a tuple once it's created. We can create a tuple by giving some ordered elements into a paranthesis `( )`. The syntax of a tuple is as follows:

```julia
(item1, item2, itme3, ...)
```

Let's see an example. Suppose we want to create a tuple consists of some mixed values. We just give those values within a paranthesis `( )` or just without the parenthesis. Both will work just fine. Then we can print the type of the tuple by using the `typeof()` method. To access the elements of a tuple, we can use the index values of tuple, but keep in mind in `Julia`, index starts from 1. So, in order to access the first element of tuple, we need to follow this syntax:

```julia

tuple_name[1]

```

#### _input_
```julia
tup1 = (1, 2, 4.5, "Hello")

println(tup1)

#this also works

tup2 = 'c', 11, 0.5, "World"

print(tup2)
```
#### _output_
    (1, 2, 4.5, "Hello")
    ('c', 11, 0.5, "World")

#### _input_
```julia
println("Type of tup1: ", typeof(tup1))
println("Type of tup2: ", typeof(tup2))
```
#### _output_
    Type of tup1: Tuple{Int64,Int64,Float64,String}
    Type of tup2: Tuple{Char,Int64,Float64,String}
    

#### _input_
```julia
#accessing Elements

println(tup1[1])
println(tup2[end])
```
#### _output_
    1
    World
    

As, we were saying earlier that, tuples are immuatble. That means, we can not change the elements of a tuple after it has been initialized. Let's test that. We will try to change the third element of `tup1`. And it will give an error.

#### _input_
```julia
tup1[3] = 'c' 
```

#### _output_
    MethodError: no method matching setindex!(::Tuple{Int64,Int64,Float64,String}, ::Char, ::Int64)

    

    Stacktrace:

     [1] top-level scope at In[4]:1


There is an another version of tuples and it is called **NamedTuples**. Here, we can assign an unique name to each elements of the tuple to access them. 

To access by using its name we need to use the following syntax:

```julia

tuple_name.variable_name

```

#### _input_
```julia
named_tup = (lang = 'C', int_num = 1, float_num = 3.6)

println("Elements of named_tuple: ", named_tup)

println("Accessing first element by index: ", named_tup[1])

println("Accessing first element by using variable name: ", named_tup.lang)
```
#### _output_
    Elements of named_tuple: (lang = 'C', int_num = 1, float_num = 3.6)
    Accessing first element by index: C
    Accessing first element by using variable name: C
    

### Array

Unlike Tuples, Arrays are mutable. So, after assigning values we can change them. We can declare an array in many ways. such as:

```julia

array_name = [item1, item2, ...]
array_name = Array([item1, item2, ...])
array_name = Array{DataType}([item1, item2, ...])

```

Here in the third syntax of declaring array, we can specify what kind of data we want to assign in our array. Lets, create three arrays using these syntax.

#### _input_
```julia
arr1 = [1, 2, 3]
arr2 = Array([2.5, "Hello", 100])
arr3 = Array{Int64}([4, 6, 8])

println("Elements of arr1: ", arr1)
println("Elements of arr2: ", arr2)
println("Elements of arr3: ", arr3)
```
#### _output_
    Elements of arr1: [1, 2, 3]
    Elements of arr2: Any[2.5, "Hello", 100]
    Elements of arr3: [4, 6, 8]
    

These are the example of 1 dimensional array. The syntax of declaring 2 dimensional array is follows:

```julia

array_2d = [item1 item2; item3 item4; ...]

```

Let's create an array which has 3 row and 2 columns or an `(3*2)` array.

#### _input_
```julia
arr_2d =[1 2; 3 4; 5 6]

arr_2d
```

#### _output_


    3×2 Array{Int64,2}:
     1  2
     3  4
     5  6



#### Array Operations

To insert, delete or sort elements of an array we can use some built in methods like `insert(), deleteat(), push(), pushfirst(), pop(), popfirst(), sort()`. Let's use these methods. To insert elements in an array we can use `push()`, `pushfirst()` and `insert()` methods. `push()` method insert an element in the end of the array, `pushfirst()` inserts an item at the begining of the array, and `insert()` method insert an item into a given location. The syntax of `insert()` method is 

```julia

insert(arr_name, position_to_insert, value)

```

Let's first insert into an array.

#### _input_
```julia
test_arr = [1, 2, 3, 4, 5]

push!(test_arr, 100)

println("Array after using push method: ", test_arr)

pushfirst!(test_arr, 12)

println("Array after using pushfirst method: ", test_arr)

insert!(test_arr, 3, 2525)

println("Array after using insert method: ", test_arr)
```
#### _output_
    Array after using push method: [1, 2, 3, 4, 5, 100]
    Array after using pushfirst method: [12, 1, 2, 3, 4, 5, 100]
    Array after using insert method: [12, 1, 2525, 2, 3, 4, 5, 100]
    

To delete elements in an array, we can use `pop()`, `popfirst()` and `deleteat()` methods. `pop()` method deletes an element from the end of the array, `popfirst()` deletes an item from the begining of the array, and `deleteat()` method deletes an item from a given location. The syntax of `deleteat()` method is 

```julia

deleteat(arr_name, position_for_delete)

```

We will use the same array which we used with insertion methods.

#### _input_
```julia
println("Array before deleting elements: ", test_arr)

pop!(test_arr)

println("Array after using pop method: ", test_arr)

popfirst!(test_arr)

println("Array after using popfirst method: ", test_arr)

deleteat!(test_arr, 4)

println("Array after using deleteat method at the 4th index: ", test_arr)
```
#### _output_
    Array before deleting elements: [12, 1, 2525, 2, 3, 4, 5, 100]
    Array after using pop method: [12, 1, 2525, 2, 3, 4, 5]
    Array after using popfirst method: [1, 2525, 2, 3, 4, 5]
    Array after using deleteat method at the 4th index: [1, 2525, 2, 4, 5]
    

Besides these inserting and deletion methods, there are some methods for other helpful tasks. Here, we will try to mention some of the methods. For sorting we can use `sort()` method. Also, if we want arrays of ones or zeros we can use `ones()` and `zeros()` method respectively. We can generate random number from uniform distribution using `rand()` method. To create random number from normal distribution we can use `randn()` method.

Let's see them in action.

#### _input_
```julia
# sorting test_arr

println("Before sorting the test_array: ", test_arr)

sort!(test_arr)

println("After sorting the test_array: ", test_arr)
```
#### _output_
    Before sorting the test_array: [1, 2525, 2, 4, 5]
    After sorting the test_array: [1, 2, 4, 5, 2525]
    

#### _input_
```julia
# create an 2*3 array of ones

ones_arr = ones(2, 3)

ones_arr
```

#### _output_


    2×3 Array{Float64,2}:
     1.0  1.0  1.0
     1.0  1.0  1.0



#### _input_
```julia
# create an 2*3 array of zeros

zeros_arr = zeros(2, 3)

zeros_arr
```


#### _output_

    2×3 Array{Float64,2}:
     0.0  0.0  0.0
     0.0  0.0  0.0



#### _input_
```julia
# create an array size of 2*5 with random variable from uniform distribution 

rand(2, 5)
```



#### _output_
    2×5 Array{Float64,2}:
     0.451961  0.309916  0.193709  0.602781  0.160294
     0.737481  0.523093  0.662101  0.946056  0.804512



#### _input_
```julia
# create an array size of 2*5 with random variable from normal distribution 

randn(2, 5)
```



#### _output_
    2×5 Array{Float64,2}:
      0.907519  2.42625  0.909603  -0.420501   0.632623
     -1.78817   0.63605  0.17628    0.419475  -0.200928



### Dictionary

Dictionary is a collection of key-value pairs, where we can access the value using its key. We can declare dictionary in the following three ways:

```julia

dict_name = Dict()
dict_name = Dict(key1 => value1, key2 => value2, ....)
dict_name = Dict{key_datatype, value_datatype}(key1 => value1, key2 => value2, ....)

```

Here in the third syntax of declaring dictionary, we can specify the data types of keys and values. 

#### _input_
```julia
dict1 = Dict()

dict1["Bangladesh"] = "Dhaka"
dict1["Sweden"] = "Stockholm"

println("Elements of dict1: ", dict1)

dict2 = Dict("Apple" => "Red", "Orange" => "Orange", "Banana" => "Yellow")

println("Elements of dict2: ", dict2)

dict3 = Dict{String, Int64}("One" => 1, "Two" => 2, "Three" => 3)

println("Elements of dict3: ", dict3)
```
#### _output_
    Elements of dict1: Dict{Any,Any}("Bangladesh" => "Dhaka","Sweden" => "Stockholm")
    Elements of dict2: Dict("Apple" => "Red","Orange" => "Orange","Banana" => "Yellow")
    Elements of dict3: Dict("One" => 1,"Two" => 2,"Three" => 3)
    

#### Accessing Dictionary Elements

To access the elements of dictionary we need to access them via their key. Suppose in `dict3`, we want to access the value `3`. So, we can do that by this:

#### _input_
```julia
println(dict3["Three"])
```
#### _output_
    3
    

Also, we can access the keys and values of a dictionary seperately by using `keys()` and `values()` method respectively. 

#### _input_
```julia
println("Keys of dict3: ", keys(dict3))

println("Values of dict3: ", values(dict3))
```
#### _output_
    Keys of dict3: ["One", "Two", "Three"]
    Values of dict3: [1, 2, 3]
    

### Set

Another data structure of `julia` is `set`. `Set` is like `array`, its mutable. But the basic difference between them is, `set` holds only `unique element`. So, there will be no duplicate element in a `set`. And the basic syntax of a set is:

```julia

set_name = Set([item1, item2, item3, ....])

```

We can do operations like union, intersection, difference between two sets using `union()`, `intersect()`, and `setdiff()` methods respectively. Also we can check if one set is subset of another one by using `issubset()` function.

Here we will create 2 sets and apply these functions on them.

#### _input_
```julia
set1 = Set([1, 2, 3, 2, 5, "new"])

println("Set1: ", set1)

set2 = Set([5, 2])

println("Set1: ", set2)
```
#### _output_
    Set1: Set(Any["new", 2, 3, 5, 1])
    Set1: Set([2, 5])
    

#### _input_
```julia
# union between two sets

union(set1, set2)
```



#### _output_
    Set{Any} with 5 elements:
      "new"
      2
      3
      5
      1



#### _input_
```julia
# intersection between two sets

intersect(set1, set2)
```


#### _output_

    Set{Any} with 2 elements:
      2
      5


#### _input_

```julia
# set difference between two sets

setdiff(set1, set2)
```

#### _output_


    Set{Any} with 3 elements:
      "new"
      3
      1

#### _input_


```julia
# Checking if set2 is subset of set1

issubset(set2, set1)
```


#### _output_

    true



As, set is mutable, we can add or delete elements from it. To add elements we can use `push()` method and to delete elements we can use `delete()` method. For deletion, we need to tell specifically which element from a set we want to delete. 

#### _input_
```julia
push!(set1, "hello")
```



#### _output_
    Set{Any} with 6 elements:
      "new"
      2
      3
      "hello"
      5
      1


#### _input_

```julia
delete!(set1, "hello")
```



#### _output_
    Set{Any} with 5 elements:
      "new"
      2
      3
      5
      1



So, thats it.

Keep Practicing.

Good luck, May the Julia be with you!!


-------------------------------------------------------------------------------------------

**Other posts in this series:**

1. [Julia Tutorial Part 1: Installations & Basics]({{< ref "/post/Julia-Tutorial-Part-1/index.md" >}})
# Week 3 -- Algorithms

## Runtime notation
Big O == upper bound of runtime (steps needed to run, ie worst case) <br>
omega == lower bound of runtime (best case) <br>
theta == when upper and lower bounds are equal <br>

Larger expressions == slower runtime bc more complex and more steps
- want n function to be small to be fastest possible
- fixed number of steps is best bc constant steps will not change as data increases

## Correctness Vs Design
Algorithm can be correct without being best design <br>
Want Fast! -- Efficiency!

## Linear search
- check from left to right
- loop through each char in array

For i from 0 to n-1
 - n - 1 == last char bc starting at 1
 - will loop n times
 - correct but not the best design bc slow
 - best you can do when you know nothing about the numbers working with <br>
**O(n) because n steps upper bound if number is last char** <br>
**Omega(1) lower bound because number could be first found meaning only 1 step needed**

## Binary search
 - can cut search time by knowing that numbers are sorted
 - phone book example--cut array after checking middle <br>
**Upper bound: O(log n) because cut in half each step** <br>
**Lower bound: Omega(1)**

**When successful: return 0 from main**<br>
**Unsuccessful: return 1 from main**

## Data Structures
Combine arrays into single array
Person has a name and number
~~~C
typedef struct
{
    string name;
    string number;
}
person;

person[i].name
~~~

## Selection Sort
~~~C
for i from 0 to n-1
    find smallest number btw numbers[i] and numbers[n-1]
    swap smallest number with numbers[i]
~~~

- problem gets smaller by one with each loop
**O(n^2), omega(n^2)** <br>
**Since equal, theta(n^2)** <br>
- still have to look at all postitions even if already sorted

## Bubble Sort
~~~C
repeat n-1 times
    for i from 0 to n-2
        if numbers[i] and numbers[i+1] are out of order
            swap them
    if no swaps
        quit
~~~

**Running time: O(n^2), omega(n)**
- have to look at every element at least once
- if already sorted, only need to look once

## Recursion
- previous sorts were comparison sorts that go over same elements many times
- Function calls itself in recursion

## Merge sort
~~~C
if only one number
    Quit
Else
    sort left half of numbers
    sort right half of numbers
    merge sorted halves
~~~

- Touches elements a minimal amount of times
- requires empty array to move into, uses more memory
**O(n log n), omega(n log n), theta(n log n)**


#### Fastest==Merge
#### Bubble sort faster than selection if already sorted, only need to look once.
#### Selection and bubble O(n^2) upper bound





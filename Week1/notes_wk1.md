# Notes week 1
## Coding in C
- needs to be compiled: make <filename>
- have to put strings in double quotes "string"
- single quotes for single characters 'c'
- semi-colon to finish;
- \n to move to new line
- make comment with //

- return values:
  - must tell comp what type of value it will be storing in a variable
  - need to include cs50.h library for get_string function
  - %s is a string placeholder
    - printf("hello, %s\n", answer);

int main(void)
{

}
- This is how to start a file in C, all code inside curly braces
- .h files are header files that can be used at the beginning of a code to include a library with specific functions

- const int mine = 2
  - this tells C to never change the int, even if I mess it up later
  - usually also in all caps in code to remind that it is constant

- % == remainder operator
- || == or
- && == and
- while (true) == do forever
- i = i + 1 OR i += 1 OR i++

- for/while loops:
  - int i = 3;
    while (i > 0)
    {
        printf("meow\n");
        i--; //countdown
    }

  - for (int i = 0; i < 3; i++)
    {
        printf("meow\n");
    }

- creating functions
  - void name(inputs?) -- no inputs, no return == void
  - can move functions to different areas than top of code if you tell at the top what the function is called and the return types (prototype at top)
  - void meow(int n);

    void meow(int n)
    {
        for (int i = 0; i < n; i++)
        {
            printf("meow\n");
        }
    }

  - float discount(float price, int percentage); 
    
    float discount(float price, int percentage)
  
    {
        return price * (100 - percentage) / 100;
    }

- Do while loop: check condition first instead of last
  - int n;
    do
    {
        n = get_int("Width: ");
    }
    while (n < 1);


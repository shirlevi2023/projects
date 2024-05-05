// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(LOOP)     // infinite loop

@KBD
D=M
@BLACK
D;JNE
@WHITE
D;JEQ

(BLACK)
@count     // colour the screen to black
//count=-1
M=-1
(LOOPBLACK)
//count+=1
@count
M=M+1
D=M // D=count

@SCREEN
A=A+D // A= &(SCREEN+count)
M=-1 // RAM[SCREEN+count] = -1
@8191
D=D-A // counter-8191
@LOOPBLACK
D;JNE

@LOOP       // return to LOOP
0;JMP

(WHITE)
@counterwhite     // colour the screen to white
M=-1
(LOOPWHITE)
@counterwhite
M=M+1
D=M
@SCREEN
A=A+D
M=0
@8191
D=D-A
@LOOPWHITE
D;JNE

@LOOP      // return to LOOP
0;JMP
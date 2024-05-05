// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

//defining the first num in the arr
// max and min num
@R14
A=M
D=A
@minindex
M=D
@maxindex
M=D
@minindex
A=M
D=M
@minnum
M=D
@maxnum
M=D

//1. finding min and max num + saving there index
//for i from 0 to lenarr
@i
M=-1

//jump to outer loop
@OUTER-LOOP
0;JMP

    //outer loop
(OUTER-LOOP)
@i
M=M+1
@i
D=M
@R15
D=D-M
//D=D+1
@CHECK
D;JLT

@SWAP
D;JGE

(CHECK)
//IF arr[i]<min_num -> min num =arr[i]
@R14
A=M
D=A
@i
D=D+M
@firstnumindex
M=D
@firstnumindex
A=M
D=M
@num1
M=D

// ? arr[i] -min_num <0
@num1
D=M
@minnum
D=D-M
@CHANGE
D;JLT

////IF arr[i]>max_num -> max num =arr[i]
// arr[i] -max_num >0
@num1
D=M
@maxnum
D=D-M
@CHANGE1
D;JGT
@OUTER-LOOP
0;JMP

(CHANGE)
@num1
D=M
@minnum
M=D
@firstnumindex
D=M
@minindex
M=D
@OUTER-LOOP
0;JMP

(CHANGE1)
@num1
D=M
@maxnum
M=D
@firstnumindex
D=M
@maxindex
M=D
@OUTER-LOOP
0;JMP

(SWAP)
@minnum
D=M
@tempnum
M=D
@maxnum
D=M
@minnum
M=D

@tempnum
D=M
@maxnum
M=D

@minnum
D=M
@minindex
A=M
M=D

@maxnum
D=M
@maxindex
A=M
M=D

@END
0;JMP

(END)
@END
0;JMP


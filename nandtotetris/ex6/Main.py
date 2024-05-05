"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

def chagne_array_to_str(A_str, A_number) -> str:
    for num in range(len(A_number)):
        A_str += str(A_number[num])
    return A_str


def add_zero(A_number) -> None:
    remainder = 15 - len(A_number) + 1
    for i in range(remainder):
        A_number.insert(i, 0)


def decimal_to_binary(num, A_number):
    if int(num) >= 1:
        decimal_to_binary(int(num) // 2, A_number)

    A_number.append(int(num) % 2)


def ACommendToBinary(num, output_file, A_str) -> None:
    A_number = []
    decimal_to_binary(num, A_number)
    add_zero(A_number)
    A_str = chagne_array_to_str(A_str, A_number)
    output_file.write(A_str + "\n")


def CCommendToBinary(line, code,parser):
    index_equal = line.find("=")
    index_comp = line.find(";")
    index_shiftRigth = line.find(">>")
    index_shiftLeft = line.find("<<")

    if index_equal!=-1:
        dest=parser.dest(line,index_equal)
        # dest = line[0:index_equal]
    else: dest=''

    if index_comp!=-1:
        jump=parser.jump(line, index_comp)
        # jump = line[index_comp+1:]
    else: jump=''

    if index_comp==-1:
        comp = line[index_equal + 1:]
    else:
        comp=parser.comp(line,index_equal,index_comp)
        # comp = line[index_equal + 1:index_comp]

    if index_shiftRigth != -1 or index_shiftLeft != -1:
        C_number = '101'
    else:
        C_number = '111'

    C_number = C_number + code.comp(comp) + code.dest(dest) + code.jump(jump)

    output_file.write(C_number + "\n")


def addSynbol(parser, symbolTable) -> None:
    countLine = 0
    countSymbol = 0
    indexSymbol = 16

    for line in parser.tempFile:
        if parser.command_type(line) == "L_COMMAND":
            if not symbolTable.contains(line[1:-2]):
                symbolTable.add_entry(line[1:-2], countLine - countSymbol)
                countSymbol += 1
        countLine += 1

    parser.tempFile.seek(0)
    for line in parser.tempFile:
        if parser.command_type(line) == "A_COMMAND":
            a = line[1:-1]
            a = a.strip('\n')
            a=a.strip()
            if not a.isnumeric() and not symbolTable.contains(line[1:]):
                symbolTable.add_entry(line[1:], indexSymbol)
                indexSymbol += 1
    parser.tempFile.seek(0)

def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    A_str = ""
    parser = Parser(input_file)
    symbolTable = SymbolTable()
    code = Code()
    parser.tempFile.seek(0)
    addSynbol(parser, symbolTable)

    i = 1
    for line in parser.tempFile:
        line_type=parser.command_type(line)
        if line_type=="A_COMMAND":
        #if parser.command_type(line) == "A_COMMAND":
            ACommendToBinary(symbolTable.get_address(line[1:]), output_file, A_str)
        elif line_type=="C_COMMAND":
        #elif parser.command_type(line) == "C_COMMAND":
            CCommendToBinary(line, code, parser)
        i += 1

    parser.tempFile.close()

    pass


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)

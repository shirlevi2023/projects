"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly language
    command, parses it, and provides convenient access to the commands
    components (fields and symbols). In addition, removes all white space and
    comments.
    """

    def remove_lines(self) -> None:
        """
            maiking a file (temp-file) without empty lines and spaice
        """

        for line in self.input_file:
            line=line.strip(" ")
            indexLine = line.find('//')
            if line =='':
                continue
            if indexLine != 0 and line[-1]!='\n':
                self.tempFile.write(line[0:].replace(" ","")+ '\n')
            elif indexLine != 0 and line!='\n' and line[-1]=='\n':
                # print(line[0:indexLine].replace(" ",""))
                self.tempFile.write(line[0:indexLine].replace(" ","")+ '\n')
            elif indexLine==-1 and line!='\n' :
                # print(line[0:].replace(" ",""))
                self.tempFile.write(line[0:].replace(" ",""))

            self.counter+=1


    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.input_file=input_file
        self.tempFile=open("temp_file.txt","w+")
        self.counter = 0
        self.remove_lines()




    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return  self.counter<self.lines_number
        pass

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.counter=self.counter+1

    def command_type(self,line) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        self.line=line
        if self.line.startswith('//') or self.line =='':
            return 'None'
        if '@' in self.line:
            return 'A_COMMAND'
        if ';' in self.line or '=' in self.line:
            return 'C_COMMAND'
        if '(' in self.line and ')' in self.line:
            return "L_COMMAND"
        pass

    def symbol(self,lineType,line) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        # Your code goes here!
        self.lineType=lineType
        self.line=line
        if self.lineType == 'A_COMMAND':
            self.type='A_COMMAND'
            return self.line[1:]
        if self.lineType == 'L_COMMAND':
            self.type = 'L_COMMAND'
            return self.line[1:]
        pass

    def dest(self,line,index_equal) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type(line) == 'C_COMMAND':
            return line[0:index_equal]
           # return self.input_lines[10:12]

        pass

    def comp(self,line,index_equal,index_comp) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type(line) == 'C_COMMAND':
            return line[index_equal + 1:index_comp]
        pass

    def jump(self,line,index_comp) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type(line) == 'C_COMMAND':
            return line[index_comp+1:]
        pass

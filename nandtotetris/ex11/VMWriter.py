"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

# arthmetic_dictionary = {"*": "call Math.multiply 2",
#                          "/": " call Math.divide 2", "+": "add", "-": "sub",
#                          "<": "lt",
#                          ">": "gt",
#                          "=": "eq", "|": "or", "&": "and"}

segmentsDict = {"CONST": "constant", "ARG": "argument", "LOCAL": "local",
                    "STATIC": "static", "THIS":"this", "THAT": "that",
                    "POINTER": "pointer", "TEMP": "temp", "VAR":"local",
                    "FIELD":"field"}


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        pass

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        seg = ""
        if segment == "CONST":
            seg = "constant"
        elif segment == "ARG":
            seg = "argument"
        elif segment == "VAR":
            seg = "local"
        else:
            seg = segment.lower()

        self.output_stream.write("push " + seg + " " + str(index) + "\n")


    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.
        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        seg = ""
        if segment == "CONST":
            seg = "constant"
        elif segment == "ARG":
            seg = "argument"
        elif segment == "VAR":
            seg = "local"
        else: seg = segment.lower()

        self.output_stream.write("pop " + seg + " " + str(index) + "\n")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        self.output_stream.write(command.lower() + "\n") #todo- check

    def write_func(self, name, num_args):
        self.output_stream.write("function " + name + " " + str(num_args) + "\n")


    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        self.output_stream.write("label " + label +  "\n")

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("goto " + label + "\n")

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("if-goto " + label + "\n")

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        self.output_stream.write("call " + name + " " + str(n_args) + "\n")

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        # Your code goes here!
        self.output_stream.write("function  " + name + " " + str(n_locals) + "\n")

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        self.output_stream.write("return\n")

    def close_class(self)->None:
        self.output_stream.close()


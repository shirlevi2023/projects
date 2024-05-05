"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


def is_a_binary_command(command):
    return command in ['add', 'sub', 'and', 'or']


def is_an_unary_command(command):
    return command in ['neg', 'not', 'shiftleft', 'shiftright']


def is_a_compare_command(command):
    return command in ['eq', 'gt', 'lt']


def get_binary_command_output(command):
    op = ''
    if command == 'add':
        op = '+'
    elif command == 'sub':
        op = '-'

    elif command == 'and':
        op = '&'

    else:
        op = '|'

    command_out = "@SP\n" + \
                  "M = M - 1\n" \
                  "A = M\n" + \
                  "D = M\n" + \
                  "@SP\n" + \
                  "M = M - 1\n" \
                  "A = M\n" + \
                  "M = M " + op + " D\n" + \
                  "@SP\n" + \
                  "M = M + 1\n"
    return command_out


def get_unary_command_output(command):
    op = ''
    if command == 'neg':
        op = '-'
    elif command == 'not':
        op = '!'
    elif command == 'shiftleft':
        op = '<<'
    else:
        op = '>>'

    command_out = "@SP\n" + \
                  "A = M - 1\n" \
                  "M=" + op + "M\n"
    return command_out


def get_out_for_push_command(index, seg_p):
    str_out = "@" + seg_p + "\n" + \
              "D=M\n" + \
              "@" + index + "\n" + \
              "A = D+A\n" + \
              "D = M\n" + \
              "@SP\n" + \
              "A = M\n" + \
              "M =  D  \n" + \
              "@SP\n" + \
              "M = M + 1\n"

    return str_out


def get_out_for_pop_command(index, seg_p):
    str_out = "@" + index + "\n" + \
              "D = A\n" + \
              "@" + seg_p + "\n" + \
              "D = M + D\n" + \
              "@R13\n" + \
              "M = D\n" + \
              "@SP\n" + \
              "M = M - 1\n" + \
              "A = M\n" + \
              "D = M\n" + \
              "@R13\n" + \
              "A = M\n" + \
              "M = D\n"

    return str_out


def get_out_for_push_constant(index):
    str_out = "@" + str(index) + "\n" + \
              "D = A\n" + \
              "@SP\n" + \
              "A=M\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M = M+1\n"
    return str_out


def get_out_for_push_static(index):
    str_out = "@FUNC" + str(index) + "\n" + \
              "D=M\n" + \
              "@SP\n" + \
              "A=M\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M = M+1\n"
    return str_out


def get_out_for_push_pointer(index):
    str_out = "@" + str(index) + "\n" + \
              "D=A\n" + \
                "@R3\n" + \
              "A=D+A\n" + \
              "D=M\n" + \
              "@SP\n" + \
              "A=M\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M = M+1\n"
    return str_out


def get_out_for_push_temp(index):
    str_out = "@" + str(index) + "\n" + \
              "D=A\n" + \
              "@R5\n" + \
              "A=A+D\n" + \
              "D=M\n" + \
              "@SP\n" + \
              "A=M\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M = M+1\n"
    return str_out


def get_out_for_pop_static(index):
    str_out = "@FUNC" + str(index) + "\n" + \
              "D=A\n" + \
              "@R13\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M=M-1\n" + \
              "A=M\n" + \
              "D=M\n" + \
              "@R13\n" + \
              "A=M\n" + \
              "M=D\n"
    return str_out


def get_out_for_pop_pointer(index):
    str_out = "@R3\n" + \
              "D=A\n" + \
              "@" + str(index) + "\n" + \
              "D=D+A\n" + \
              "@R13\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M=M-1\n" + \
              "A=M\n" + \
              "D=M\n" + \
              "@R13\n" + \
              "A=M\n" + \
              "M=D\n"
    return str_out


def get_out_for_pop_temp(index):
    str_out = "@" + str(index) + "\n" + \
              "D=A\n" + \
              "@R5\n" + \
              "D=A+D\n" + \
              "@R13\n" + \
              "M=D\n" + \
              "@SP\n" + \
              "M=M-1\n" + \
              "A=M\n" + \
              "D=M\n" + \
              "@R13\n" + \
              "A=M\n" + \
              "M=D\n"
    return str_out


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.count = 0
        self.output_stream = output_stream
        self.file_name = ""


    def get_compare_command_output(self, command):
        self.count += 1
        if command == 'gt':
            command_out = "@SP\n" +\
                          "M=M-1\n" +\
                          "A=M\n" +\
                          "D=M\n" +\
                          "@IF_POSITIVE_L00P" + str(self.count)+"\n" +\
                           "D;JGE\n" +\
                          "@IF_NEGATIVE_L00P" + str(self.count)+"\n"+ \
                           "D;JLT\n" +\
                          "(IF_POSITIVE_L00P" +str(self.count)+ ")\n" +\
                           "@SP\n" + \
                          "A=M-1\n" +\
                          "D=M\n" +\
                          "@IF_FALSE" + str(self.count)+ "\n" +\
                           "D;JLT\n" +\
                          "@COMPARE_NUM" + str(self.count)+"\n" +\
                           "D;JMP\n" + \
                          "(IF_NEGATIVE_L00P" + str(self.count)+ ")\n" +\
                          "@SP\n" + \
                          "A=M-1\n" +\
                          "D=M\n" + \
                          "@IF_TRUE" + str(self.count)+"\n" +\
                           "D;JGE\n" +\
                          "@COMPARE_NUM" + str(self.count)+ "\n" +\
                          "D;JMP\n" + \
                          "(COMPARE_NUM" + str(self.count)+ ")\n" +\
                          "@SP\n" + \
                          "A=M\n" + \
                          "D=D-M\n" + \
                          "@IF_TRUE" + str(self.count)+ "\n" +\
                           "D;JGT\n" + \
                          "@IF_FALSE" + str(self.count)+ "\n" +\
                           "D;JMP\n" +\
                          "(IF_TRUE" + str(self.count)+ ")\n" +\
                          "@SP\n" + \
                          "A=M-1\n" +\
                          "M=-1\n" + \
                          "@END_LOOP" + str(self.count)+ "\n" +\
                           "D;JMP\n" +\
                           "(IF_FALSE" + str(self.count)+ ")\n" +\
                           "@SP\n" + \
                          "A=M-1\n" +\
                          "M=0\n" + "(END_LOOP" + str(self.count)+ ")\n" +\
                          "@SP\n"

        elif( command == 'lt'):
            command_out = "@SP\n" +\
                          "M=M-1\n" +\
                          "A=M\n" +\
                          "D=M\n" +\
                          "@IF_POSITIVE_L00P" + str(self.count)+ "\n" +\
                          "D;JGE\n" + \
                          "@IF_NEGATIVE_L00P" + str(self.count)+ "\n" +\
                          "D;JLT\n" + "(IF_POSITIVE_L00P" + str(self.count)+ ")\n" +\
                           "@SP\n" + \
                          "A=M-1\n" + \
                          "D=M\n" + \
                          "@IF_NOT_GREATER__THAN" + str(self.count)+ "\n" +\
                           "D;JLT\n" + \
                          "@COMPARE_NUM_" + str(self.count)+ "\n" +\
                           "D;JMP\n" +\
                          "(IF_NEGATIVE_L00P" + str(self.count)+ ")\n" +\
                           "@SP\n" +\
                          "A=M-1\n" +\
                          "D=M\n" +\
                          "@IF_GREATER_THAN" + str(self.count)+ "\n" +\
                           "D;JGE\n" +\
                          "@COMPARE_NUM_" + str(self.count)+ "\n"+ \
                           "D;JMP\n" + \
                          "(COMPARE_NUM_" + str(self.count)+ ")\n" +\
                           "@SP\n" +\
                          "A=M\n" +\
                          "D=D-M\n" + \
                          "@IF_GREATER_THAN" + str(self.count)+ "\n" +\
                           "D;JGE\n" +\
                          "@IF_NOT_GREATER__THAN" + str(self.count)+ "\n" +\
                           "D;JMP\n" +\
                           "(IF_NOT_GREATER__THAN" + str(self.count)+ ")\n" +\
                          "@SP\n" + \
                          "A=M-1\n" +\
                          "M=-1\n" + \
                          "@END_LOOP" + str(self.count)+ "\n" +\
                           "D;JMP\n"+\
                           "(IF_GREATER_THAN" + str(self.count)+ ")\n" +\
                            "@SP\n" + \
                            "A=M-1\n" +\
                           "M=0\n" +\
                            "(END_LOOP" + str(self.count)+ ")\n"

        else:
            command_out = "@SP\n" +\
                          "M=M-1\n" +\
                          "A=M\n" +\
                          "D=M\n" + \
                            "@IF_POSITIVE_L00P" + str(self.count)+ "\n" +\
                            "D;JGE\n" + \
                            "@IF_NEGATIVE_L00P" + str(self.count)+ "\n" +\
                            "D;JLT\n" + \
                            "(IF_POSITIVE_L00P" + str(self.count)+ ")\n" +\
                            "@SP\n" + \
                            "A=M-1\n" +\
                          "D=M\n" +\
                          "@IF_NOT_EQUAL" +str(self.count)+"\n" +\
                            "D;JLT\n" +\
                            "@COMPARE_NUM" + str(self.count)+ "\n" +\
                            "D;JMP\n" + \
                            "(IF_NEGATIVE_L00P" + str(self.count)+ ")\n" +\
                            "@SP\n" + \
                            "A=M-1\n" +\
                          "D=M\n" + \
                          "@IF_NOT_EQUAL" + str(self.count)+ "\n" +\
                            "D;JGE\n" + \
                          "@COMPARE_NUM" + str(self.count)+ "\n" +\
                            "D;JMP\n" + \
                            "(COMPARE_NUM" + str(self.count)+ ")\n" +\
                             "@SP\n" +\
                          "A=M\n" +\
                          "D=D-M\n" + \
                            "@IF_EQUAL_NUM" + str(self.count)+ "\n" +\
                            "D;JEQ\n" + "(IF_NOT_EQUAL" + str(self.count)+ ")\n" +\
                             "@SP\n" +\
                          "A=M-1\n" +\
                          "M=0\n" + \
                          "@END_LOOP" + str(self.count)+ "\n"+ \
                            "D;JMP\n" +\
                            "(IF_EQUAL_NUM" + str(self.count)+ ")\n" +\
                            "@SP\n" +\
                          "A=M-1\n" + \
                          "M=-1\n" + \
                            "(END_LOOP" + str(self.count)+ ")\n" +\
                            "@SP\n"


        return command_out

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.file_name = filename

        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if is_a_binary_command(command):
            output_string = get_binary_command_output(command)
            self.output_stream.write(output_string)
            return
        if is_an_unary_command(command):
            output_string = get_unary_command_output(command)
            self.output_stream.write(output_string)
            return

        if is_a_compare_command(command):
            output_string = self.get_compare_command_output(command)
            self.output_stream.write(output_string)
            return

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        str_out = ""
        segmentDictionary = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        if segment in segmentDictionary:
            seg_p = segmentDictionary[segment]
            if command == "C_PUSH":
                str_out = get_out_for_push_command(index, seg_p)

            else:
                str_out = get_out_for_pop_command(index, seg_p)

        elif command == "C_PUSH":
            if segment == "constant":
                str_out = get_out_for_push_constant(index)
            if segment == "static":
                str_out = get_out_for_push_static(index)
            if segment == "pointer":
                str_out = get_out_for_push_pointer(index)
            if segment == "temp":
                str_out = get_out_for_push_temp(index)
        else:
            if segment == 'static':
                str_out = get_out_for_pop_static(index)
            if segment == 'pointer':
                str_out = get_out_for_pop_pointer(index)
            if segment == 'temp':
                str_out = get_out_for_pop_temp(index)

        self.output_stream.write(str_out)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass

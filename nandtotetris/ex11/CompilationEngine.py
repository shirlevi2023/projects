"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import VMWriter
from SymbolTable import SymbolTable

Token_keyWords_bool = ('true', 'false', 'null', 'this')
arithmatic_commands = {"+": "ADD", "-": "SUB", "&": "AND", "|": "OR", "<": "LT",
                       ">": "GT", "=": "EQ"}


def get_start_tag_(string):
    return "<" + string + ">"


def get_end_tag_(string):
    return "</" + string + ">"


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, tokenizer, VMWriter) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.fields_num = 0
        self.tokenizer = tokenizer
        self.VM_Writer = VMWriter
        self.symbol_table = SymbolTable()
        self.if_counter = -1
        self.counter = 0
        self.while_counter = -1
        self.current_class = None
        self.args_counter_expression_list=0
        self.var_counter_var_dec=0


    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.out_token_and_advance()  # class (keyword)
        self.current_class = self.tokenizer.get_token_val()
        self.out_token_and_advance()  # out className (identifier)
        self.out_token_and_advance()  # out { (symbol)
        while (self.tokenizer.get_token_val() in {"static", "field"}):  # class vars declarations
            self.compile_class_var_dec()
        while (self.tokenizer.get_token_val() in {"constructor", "function", "method"}):  # subroutines declarations
            self.compile_subroutine()
        self.out_token_and_advance()  # out } (symbol)
        self.VM_Writer.close_class()


    def compile_class_var_dec(self) -> None:  ## shir uziel
        """Compiles a static declaration or a field declaration."""
        # self.output_stream.write(get_start_tag_("classVarDec"))
        # self.output_stream.write("\n")
        temp_class_var = self.tokenizer.get_token_val()
        if (temp_class_var == "field"):
            self.fields_num += 1
        self.out_token_and_advance()  # out className (identifier)

        temp_class_type = self.tokenizer.get_token_val()
        self.out_token_and_advance()  #
        temp_class_var_name = self.tokenizer.get_token_val()
        self.out_token_and_advance()  #
        self.symbol_table.define(temp_class_var_name, temp_class_type, self.symbol_table.segments_dic[temp_class_var])
        while (self.tokenizer.get_token_val() == ','):  # class vars declarations
            self.out_token_and_advance()  # class (keyword)
            temp_class_var_name = self.tokenizer.get_token_val()
            self.out_token_and_advance()  #
            self.symbol_table.define(temp_class_var_name, temp_class_type,
                                     self.symbol_table.segments_dic[temp_class_var])
            if (temp_class_var == "field"):
                self.fields_num += 1
        self.out_token_and_advance()  # class (keyword)

    def compile_subroutine(self) -> None:  ## me
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # pass on the definiton of subroutine:
        self.num_while = -1 # todo
        self.num_if = -1
        t_func = self.tokenizer.get_token_val()
        self.out_token_and_advance()  # type function
        self.out_token_and_advance()  # return val type
        func_name = self.tokenizer.get_token_val()
        self.out_token_and_advance()  # func_name
        self.out_token_and_advance()  # (
        # if subroutine is method- add this as local argument
        if t_func == "method":
            self.symbol_table.define("this", self.current_class, "ARG")
        self.compile_parameters_lst()
        self.out_token_and_advance()  # )
        self.compile_subroutine_body(func_name, t_func)

    def compile_subroutine_body(self, func_name, func_type) -> None:
        num_vars = 0
        self.out_token_and_advance()  # {
        while (self.tokenizer.get_token_val() == "var"):
            self.compile_var_dec()
            num_vars+=self.var_counter_var_dec
            # num_vars += self.compile_var_dec()
        self.VM_Writer.write_func(self.current_class + "." + func_name, num_vars)

        if func_type == "method":
            self.VM_Writer.write_push("ARG", 0)
            self.VM_Writer.write_pop("POINTER", 0)

        elif func_type == "constructor":
            self.VM_Writer.write_push("CONST", self.fields_num) ## todo
            self.VM_Writer.write_call("Memory.alloc", 1)
            self.VM_Writer.write_pop("POINTER", 0)

        self.compile_statements()
        self.out_token_and_advance()  # }

        # clear subroutine table after compiling
        self.symbol_table.start_subroutine()


    def compile_var_dec(self) -> None:  ## me
        """Compiles a var declaration."""
        # Your code goes here!
        # self.output_stream.write(get_start_tag_("varDec"))
        # self.output_stream.write("\n")
        #
        # var_counter=0
        self.var_counter_var_dec=0

        self.out_token_and_advance()  # var
        v_type = self.tokenizer.get_token_val()
        self.out_token_and_advance()  # type
        v_name = self.tokenizer.get_token_val()
        self.out_token_and_advance()  # var name (identifier)
        # var_counter+=1
        self.var_counter_var_dec+=1

        self.symbol_table.define(v_name, v_type, "VAR")

        while self.tokenizer.get_token_val() == ",":
            self.var_counter_var_dec += 1
            # var_counter += 1

            self.out_token_and_advance()  # ,
            v_name = self.tokenizer.get_token_val()
            self.out_token_and_advance()  # varName (identifier)
            self.symbol_table.define(v_name, v_type, "VAR")

        self.out_token_and_advance()  # ;
        # return var_counter

    def compile_statements(self) -> None:  ## new
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        # Your code goes here!
        # self.output_stream.write(get_start_tag_("statements"))
        # self.output_stream.write("\n")
        while self.tokenizer.get_token_val() in {"let", "if", "while", "do", "return"}:

            if self.tokenizer.get_token_val() == "let":
                self.compile_let()

            elif self.tokenizer.get_token_val() == "if":
                self.compile_if()

            elif self.tokenizer.get_token_val() == "while":
                self.compile_while()

            elif self.tokenizer.get_token_val() == "do":
                self.compile_do()

            elif self.tokenizer.get_token_val() == "return":
                self.compile_return()

        # self.output_stream.write(get_end_tag_("statements"))
        # self.output_stream.write("\n")

    def compile_do(self) -> None:  ## shir uziel
        """Compiles a do statement."""
        self.out_token_and_advance()  # pass on "do" token
        self.compile_call_subroutine()
        self.VM_Writer.write_pop("TEMP", 0)  # pop temp 0
        self.out_token_and_advance()  # pass on ";" token

    def compile_let(self) -> None:  ## me
        """Compiles a let statement."""

        self.out_token_and_advance()  # let
        temp_class_var_name = self.tokenizer.get_token_val()
        var_kind_of = self.symbol_table.kind_of(temp_class_var_name)
        var_index_of = self.symbol_table.index_of(temp_class_var_name)
        if (var_kind_of == "FIELD"):
            var_kind_of = "THIS"
        self.out_token_and_advance()  # let
        found_word = False
        if (self.tokenizer.get_token_val() == "["):
            found_word = True
            self.out_token_and_advance()  # [
            self.compile_expression()
            self.out_token_and_advance()  # ]
            self.VM_Writer.write_push(var_kind_of, var_index_of)
            self.VM_Writer.write_arithmetic(self.symbol_table.arithmatic_commands['+'])
        self.out_token_and_advance()
        self.compile_expression()
        self.out_token_and_advance()
        if (not found_word):
            self.VM_Writer.write_pop(var_kind_of, var_index_of)
        else:
            self.VM_Writer.write_pop("TEMP", 0)
            self.VM_Writer.write_pop("POINTER", 1)
            self.VM_Writer.write_push("TEMP", 0)
            self.VM_Writer.write_pop("THAT", 0)

    def compile_while(self) -> None:  ## shir uziel
        """Compiles a while statement."""
        self.while_counter += 1
        temp_while_counter = self.while_counter
        self.VM_Writer.write_label("WHILE_LOOP" + str(temp_while_counter))
        self.out_token_and_advance()  # (
        self.out_token_and_advance()  # (
        self.compile_expression()
        self.VM_Writer.write_arithmetic("NOT")
        self.out_token_and_advance()  # )
        self.VM_Writer.write_if("WHILE_END_LOOP" + str(temp_while_counter))
        self.out_token_and_advance()  # {
        self.compile_statements()
        self.out_token_and_advance()  # }
        self.VM_Writer.write_goto("WHILE_LOOP" + str(temp_while_counter))
        self.VM_Writer.write_label("WHILE_END_LOOP" + str(temp_while_counter))

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.out_token_and_advance()  # ;
        if self.tokenizer.get_token_val() != ";":
            self.compile_expression()
        else:
            self.VM_Writer.write_push("CONST", 0)
        self.out_token_and_advance()  # ;
        self.VM_Writer.write_return()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.if_counter += 1
        temp_counter = self.if_counter
        self.out_token_and_advance()
        self.out_token_and_advance()
        self.compile_expression()
        self.VM_Writer.write_if("IF_LABEL" + str(temp_counter))
        self.VM_Writer.write_goto("IF_LABEL_NOT" + str(temp_counter))
        self.VM_Writer.write_label("IF_LABEL" + str(temp_counter))
        self.out_token_and_advance()
        self.out_token_and_advance()
        self.compile_statements()
        self.out_token_and_advance()
        # self.out_token_and_advance()
        if (self.tokenizer.get_token_val() == "else"):
            self.VM_Writer.write_goto("IF_LABEL_END_LOOP" + str(temp_counter))
        self.VM_Writer.write_label("IF_LABEL_NOT" + str(temp_counter))
        if (self.tokenizer.get_token_val() == "else"):
            self.out_token_and_advance()
            self.out_token_and_advance()
            self.compile_statements()
            self.out_token_and_advance()
            # self.out_token_and_advance()
            self.VM_Writer.write_label("IF_LABEL_END_LOOP" + str(temp_counter))

    def compile_expression(self) -> None:  ## new
        """Compiles an expression."""
        # for the first test we assume expression with constant only!

        # Your code goes here!
        # self.output_stream.write(get_start_tag_("expression"))
        # self.output_stream.write("\n")
        self.compile_term()
        #
        while self.tokenizer.get_token_val() in {'+', '-', '*', '/', '&', '|', '<', '>', '='} \
                or self.tokenizer.get_token_val() in {"amp", "gt", "lt"}:
            current_token_val = self.tokenizer.get_token_val()
            self.out_token_and_advance()
            self.compile_term()
            if current_token_val == "*":
                self.VM_Writer.write_call("Math.multiply", 2)
            elif current_token_val == "/":
                self.VM_Writer.write_call("Math.divide", 2)
            else:
                self.VM_Writer.write_arithmetic(arithmatic_commands[current_token_val])

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # for the first test we assume term is constant!
        cur_token_val = self.tokenizer.get_token_val()
        if self.tokenizer.token_type() == "INT_CONST":
            self.VM_Writer.write_push("CONST", self.tokenizer.get_token_val())
            self.out_token_and_advance()

        elif cur_token_val in {"true", "null", "false", "this"}:  # keyword constant
            # if cur_token_val == "true":
            #     # self.VM_Writer.write_push("CONST", 1) //todo-???????
            #     self.VM_Writer.write_arithmetic("NOT")

            if cur_token_val == "this":
                self.VM_Writer.write_push("POINTER", 0)

            else:  # null or false
                self.VM_Writer.write_push("CONST", 0)
            if cur_token_val == "true":
                # self.VM_Writer.write_push("CONST", 1) //todo-???????
                self.VM_Writer.write_arithmetic("NOT")

            self.out_token_and_advance()

        elif self.tokenizer.token_type() == "STRING_CONST":
            string_length = len(cur_token_val)
            # create the string object by call to OS method
            self.VM_Writer.write_push("CONST", string_length)
            self.VM_Writer.write_call("String.new", 1)

            # add the chars of the string by OS method
            for char in cur_token_val:
                self.VM_Writer.write_push("CONST", ord(char))
                self.VM_Writer.write_call("String.appendChar", 2)

            self.out_token_and_advance()

        elif self.tokenizer.token_type() == "IDENTIFIER":
            # self.out_token_and_advance()  # varName/subroutineName
            nxt = self.tokenizer.get_tokens_lst()[self.tokenizer.get_cur_token_index()+1]
            if nxt in {'[', '(', '.'}:
                if nxt == '[':
                    kind_array_var = self.symbol_table.kind_of(self.tokenizer.get_token_val())
                    idx_array_var = self.symbol_table.index_of(self.tokenizer.get_token_val())
                    self.out_token_and_advance()  # [
                    self.out_token_and_advance()  # [
                    self.compile_expression()
                    self.out_token_and_advance()  # ]
                    self.VM_Writer.write_push(kind_array_var, idx_array_var)
                    self.VM_Writer.write_arithmetic("ADD")
                    self.VM_Writer.write_pop("POINTER", 1)
                    self.VM_Writer.write_push("THAT", 0)
                else:  # '(' or '.
                    self.compile_call_subroutine()


            else:  # var_name
                var = self.tokenizer.get_token_val()
                kind_var = self.symbol_table.kind_of(var)
                var_idx = self.symbol_table.index_of(var)
                if kind_var == "FIELD":
                    kind_var = "THIS"
                self.VM_Writer.write_push(kind_var, var_idx)
                self.out_token_and_advance()  # varName


        # expression
        elif self.tokenizer.get_token_val() == '(':
            self.out_token_and_advance()  # (
            self.compile_expression()
            self.out_token_and_advance()  # )

        # unary op
        elif self.tokenizer.get_token_val() in {'-', '~'}:
            curUnaryOp =  self.tokenizer.get_token_val()

            self.out_token_and_advance()
            self.compile_term()
            if curUnaryOp == '-':
                self.VM_Writer.write_arithmetic("NEG")
            else:
                self.VM_Writer.write_arithmetic("NOT")


    def compile_call_subroutine(self):  # arrive here if next token is . or (
        n_args = 0
        cur_identifier = self.tokenizer.get_token_val()
        self.out_token_and_advance()  # identifier
        cur_token = self.tokenizer.get_token_val()
        if cur_token == '.':
            self.out_token_and_advance()  # .
            cur_token = self.tokenizer.get_token_val()
            if (self.symbol_table.kind_of(cur_identifier) == None):  # is a class, does not appear in the symbol table
                subroutineName = cur_identifier + "." + cur_token
            else:
                v_kind = self.symbol_table.kind_of(cur_identifier)
                v_type = self.symbol_table.type_of(cur_identifier)
                v_idx = self.symbol_table.index_of(cur_identifier)
                if v_kind == "FIELD":
                    v_kind = "THIS"
                self.VM_Writer.write_push(v_kind, v_idx)
                subroutineName = v_type + "." + cur_token
                n_args += 1
            self.out_token_and_advance()  # func_name
            self.out_token_and_advance()  # (
            n_args += self.compile_expression_list()
            # self.compile_expression_list()
            # n_args+=self.args_counter_expression_list
            self.out_token_and_advance()  # (
            self.VM_Writer.write_call(subroutineName, n_args)

        else:  # cur_token == '('
            self.out_token_and_advance()  # (
            # push the current object
            self.VM_Writer.write_push("POINTER", 0)
            # push parameters
            # self.compile_expression_list()
            # n_args=self.args_counter_expression_list
            n_args = self.compile_expression_list()
            n_args += 1
            self.out_token_and_advance()  # )
            self.VM_Writer.write_call(self.current_class + '.' + cur_identifier, n_args)



    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # self.args_counter_expression_list = 0
        args_counter = 0
        if (not self.tokenizer.get_token_val() == ")"):
            self.compile_expression()
            # self.args_counter_expression_list+=1
            args_counter += 1
            while (self.tokenizer.get_token_val() == ","):
                self.args_counter_expression_list += 1
                args_counter += 1
                self.out_token_and_advance()  # ,
                self.compile_expression()
        return args_counter

    def out_token_and_advance(self):
        token_val = self.tokenizer.get_token_val()
        token_type = self.tokenizer.token_type().lower()
        if token_type == "string_const":
            token_type = "stringConstant"
        if token_type == "int_const":
            token_type = "integerConstant"
        tag_token = get_start_tag_(token_type) + token_val + get_end_tag_(token_type) + "\n"
        self.tokenizer.advance()

    def compile_parameters_lst(self):

        if self.tokenizer.get_token_val() != ")":

            v_type = self.tokenizer.get_token_val()
            self.out_token_and_advance()  # var type
            v_name = self.tokenizer.get_token_val()
            self.out_token_and_advance()  # var name
            self.symbol_table.define(v_name, v_type, "ARG")  # define vars at symbol table

            while self.tokenizer.get_token_val() == ",":
                self.out_token_and_advance()  # ,
                v_type = self.tokenizer.get_token_val()
                self.out_token_and_advance()  # type
                v_name = self.tokenizer.get_token_val()

                self.out_token_and_advance()  # var name
                self.symbol_table.define(v_name, v_type, "ARG")

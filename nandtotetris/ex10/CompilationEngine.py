"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

Token_keyWords_bool = ('true', 'false', 'null', 'this')


def get_start_tag_(string):
    return "<" + string + ">"


def get_end_tag_(string):
    return "</" + string + ">"


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, tokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.tokenizer = tokenizer
        self.output_stream = output_stream

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output_stream.write(get_start_tag_("class"))
        self.output_stream.write("\n")
        self.out_token_and_advance()  # class (keyword)
        self.out_token_and_advance()  # out className (identifier)
        self.out_token_and_advance()  # out { (symbol)

        while (self.tokenizer.get_token_val() in {"static", "field"}):  # class vars declarations
            self.compile_class_var_dec()

        while (self.tokenizer.get_token_val() in {"constructor", "function", "method"}):  # subroutines declarations
            self.compile_subroutine()

        self.out_token_and_advance()  # out } (symbol)
        self.output_stream.write(get_end_tag_("class"))
        self.output_stream.write("\n")

    def compile_class_var_dec(self) -> None:  ## shir uziel
        """Compiles a static declaration or a field declaration."""
        self.output_stream.write(get_start_tag_("classVarDec"))
        self.output_stream.write("\n")
        self.out_token_and_advance()  # class (keyword)
        self.out_token_and_advance()  # out className (identifier)
        self.out_token_and_advance()  # out { (symbol)
        while (self.tokenizer.get_token_val() == ','):  # class vars declarations
            self.out_token_and_advance()  # class (keyword)
            self.out_token_and_advance()  #
        self.out_token_and_advance()  # class (keyword)

        self.output_stream.write(get_end_tag_("classVarDec"))
        self.output_stream.write("\n")

    def compile_subroutine(self) -> None:  ## me
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output_stream.write(get_start_tag_("subroutineDec"))
        self.output_stream.write("\n")
        self.out_token_and_advance()  # (keyword) e.g method, function, constructor
        self.out_token_and_advance()  # (keyword) e.g int
        self.out_token_and_advance()  # (identifier) e.g getx
        self.out_token_and_advance()  # (symbol) (

        self.compile_parameter_list()

        self.out_token_and_advance()  # (symbol) )

        self.compile_subroutine_body()

        self.output_stream.write(get_end_tag_("subroutineDec"))
        self.output_stream.write("\n")

    def compile_subroutine_body(self) -> None:
        self.output_stream.write(get_start_tag_("subroutineBody"))
        self.output_stream.write("\n")
        self.out_token_and_advance()  # {
        while (self.tokenizer.get_token_val() == "var"):
            self.compile_var_dec()
        self.compile_statements()  ## todo
        self.out_token_and_advance()  # }
        self.output_stream.write(get_end_tag_("subroutineBody"))
        self.output_stream.write("\n")

    def compile_parameter_list(self) -> None:  ## shir uziel
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self.output_stream.write(get_start_tag_("parameterList"))
        self.output_stream.write("\n")
        if (self.tokenizer.get_token_val() != ')'):
            self.out_token_and_advance()
            self.out_token_and_advance()
            while (self.tokenizer.get_token_val() == ','):  # class vars declarations
                self.out_token_and_advance()
                self.out_token_and_advance()  # class (keyword)
                self.out_token_and_advance()  #

        self.output_stream.write(get_end_tag_("parameterList"))
        self.output_stream.write("\n")

    def compile_var_dec(self) -> None:  ## me
        """Compiles a var declaration."""
        # Your code goes here!
        self.output_stream.write(get_start_tag_("varDec"))
        self.output_stream.write("\n")

        self.out_token_and_advance()  # var
        self.out_token_and_advance()  # type
        self.out_token_and_advance()  # varName (identifier)
        while (self.tokenizer.get_token_val() == ","):
            self.out_token_and_advance()  # ,
            self.out_token_and_advance()  # varName (identifier)
        self.out_token_and_advance()  # ;
        self.output_stream.write(get_end_tag_("varDec"))
        self.output_stream.write("\n")

    def compile_statements(self) -> None:  ## new
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        # Your code goes here!
        self.output_stream.write(get_start_tag_("statements"))
        self.output_stream.write("\n")
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

        self.output_stream.write(get_end_tag_("statements"))
        self.output_stream.write("\n")

    def compile_do(self) -> None:  ## shir uziel
        """Compiles a do statement."""
        self.output_stream.write(get_start_tag_("doStatement"))
        self.output_stream.write("\n")
        self.out_token_and_advance()

        self.out_token_and_advance()
        if (self.tokenizer.get_token_val() == '('):
            self.out_token_and_advance()
            self.compile_expression_list()
            self.out_token_and_advance()
        else:
            self.out_token_and_advance()
            self.out_token_and_advance()
            self.out_token_and_advance()
            self.compile_expression_list()
            self.out_token_and_advance()
        self.out_token_and_advance()
        self.output_stream.write(get_end_tag_("doStatement"))
        self.output_stream.write("\n")

    def compile_let(self) -> None:  ## me
        """Compiles a let statement."""
        # Your code goes here!
        self.output_stream.write(get_start_tag_("letStatement"))
        self.output_stream.write("\n")
        self.out_token_and_advance()  # let (keyword)
        self.out_token_and_advance()  # varName (identifier)
        if (self.tokenizer.get_token_val() == "["):
            self.out_token_and_advance()  # [
            self.compile_expression()
            self.out_token_and_advance()  # ]

        self.out_token_and_advance()  # =
        self.compile_expression()
        self.out_token_and_advance()  # ;
        self.output_stream.write(get_end_tag_("letStatement"))
        self.output_stream.write("\n")

    def compile_while(self) -> None:  ## shir uziel
        """Compiles a while statement."""
        #

        self.output_stream.write(get_start_tag_("whileStatement"))
        self.output_stream.write("\n")
        self.out_token_and_advance()
        self.out_token_and_advance()
        self.compile_expression()
        self.out_token_and_advance()
        self.out_token_and_advance()
        self.compile_statements()
        self.out_token_and_advance()
        self.output_stream.write(get_end_tag_("whileStatement"))
        self.output_stream.write("\n")

    def compile_return(self) -> None:  ## me
        """Compiles a return statement."""
        # Your code goes here!
        self.output_stream.write(get_start_tag_("returnStatement"))
        self.output_stream.write("\n")
        self.out_token_and_advance()  # return (keyword)
        if self.tokenizer.get_token_val() != ";":
            self.compile_expression()
        self.out_token_and_advance()  # ;
        self.output_stream.write(get_end_tag_("returnStatement"))
        self.output_stream.write("\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output_stream.write(get_start_tag_("ifStatement"))
        self.output_stream.write("\n")
        self.out_token_and_advance()
        self.out_token_and_advance()  # ;
        self.compile_expression()
        self.out_token_and_advance()
        self.out_token_and_advance()
        self.compile_statements()
        self.out_token_and_advance()
        if (self.tokenizer.get_token_val() == "else"):
            self.out_token_and_advance()
            self.out_token_and_advance()
            self.compile_statements()
            self.out_token_and_advance()
        self.output_stream.write(get_end_tag_("ifStatement"))
        self.output_stream.write("\n")

    def compile_expression(self) -> None:  ## new
        """Compiles an expression."""
        # Your code goes here!
        self.output_stream.write(get_start_tag_("expression"))
        self.output_stream.write("\n")
        self.compile_term()

        while self.tokenizer.get_token_val() in {'+', '-', '*', '/', '&', '|', '<', '>', '='} \
                or self.tokenizer.get_token_val() in {"&amp;", "&gt;", "&lt;"}:
            self.out_token_and_advance()
            self.compile_term()

        self.output_stream.write(get_end_tag_("expression"))
        self.output_stream.write("\n")

    #
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
        # Your code goes here!
        self.output_stream.write(get_start_tag_("term"))
        self.output_stream.write("\n")

        if self.tokenizer.token_type() in {"INT_CONST", "STRING_CONST"}:
            self.out_token_and_advance()
        #
        elif self.tokenizer.get_token_val() in Token_keyWords_bool:
            self.out_token_and_advance()

        elif self.tokenizer.token_type() == "IDENTIFIER":
            self.out_token_and_advance()  # varName/subroutineName
            nxt = self.tokenizer.get_tokens_lst()[self.tokenizer.get_cur_token_index()]  ## todo- has more tokens?
            if nxt in {'[', '(', '.'}:
                if nxt == '[':
                    self.out_token_and_advance()  # [
                    self.compile_expression()
                    self.out_token_and_advance()  # ]


                elif nxt == '(':
                    self.out_token_and_advance()  # (
                    self.compile_expression_list()
                    self.out_token_and_advance()  # )

                elif nxt == '.':
                    self.out_token_and_advance()  # .
                    self.out_token_and_advance()  # # subroutineName (identifier)
                    self.out_token_and_advance()  # (
                    self.compile_expression_list()
                    self.out_token_and_advance()  # )
                else:
                    self.out_token_and_advance()  # .



        elif self.tokenizer.get_token_val() == '(':
            self.out_token_and_advance()  # (
            self.compile_expression()
            self.out_token_and_advance()  # )

        elif self.tokenizer.get_token_val() in {'-', '~'}:
            self.out_token_and_advance()
            self.compile_term()
        self.output_stream.write(get_end_tag_("term"))
        self.output_stream.write("\n")

    def compile_expression_list(self) -> None:  ## shir uziel
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!

        self.output_stream.write(get_start_tag_("expressionList"))
        self.output_stream.write("\n")

        if self.tokenizer.get_token_val() != ')':
            self.compile_expression()
            while (self.tokenizer.get_token_val() == ","):
                self.out_token_and_advance()
                self.compile_expression()

        self.output_stream.write(get_end_tag_("expressionList"))
        self.output_stream.write("\n")

    def out_token_and_advance(self):
        token_val = self.tokenizer.get_token_val()
        token_type = self.tokenizer.token_type().lower()
        if token_type == "string_const":
            token_type = "stringConstant"
        if token_type == "int_const":
            token_type = "integerConstant"
        tag_token = get_start_tag_(token_type) + token_val + get_end_tag_(token_type) + "\n"
        self.output_stream.write(tag_token)
        self.tokenizer.advance()

    def compile_parameters_lst(self):
        self.output_stream.write(get_start_tag_("letStatement"))
        self.output_stream.write("\n")
        self.out_token_and_advance()
        self.out_token_and_advance()
        if self.tokenizer.get_token_val() == "[":
            self.out_token_and_advance()
            self.compile_expression()
            self.out_token_and_advance()
        self.compile_expression()
        self.out_token_and_advance()
        self.output_stream.write(get_end_tag_("letStatement"))

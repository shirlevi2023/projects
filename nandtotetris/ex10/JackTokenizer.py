"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import re
import typing


def remove_comments(file_as_str):
    def remove_helper(sub_text):
        str = sub_text.group(0)
        if str.startswith('/'):
            return " "
        else:
            return str

    remove_comments_regex = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
                                       re.DOTALL | re.MULTILINE
                                       )
    return re.sub(remove_comments_regex, remove_helper, file_as_str)


def remove_whitespaces(cleaned_file):
    input_lines = cleaned_file.splitlines()
    new_input_lines = []
    for line in input_lines:
        line = " ".join(line.split())
        if line != '':
            new_input_lines.append(line)

    return new_input_lines


def clean_file(input_stream):
    # remove all comments
    cleaned_file = remove_comments(" ".join(input_stream))
    # remove all whitespaces
    cleaned_file = remove_whitespaces(cleaned_file)

    return cleaned_file


Token_keyWords = ('class', 'constructor', 'function', 'method', 'field',
                  'static', 'var', 'int', 'char',
                  'boolean', 'true', 'false', 'null', 'this', 'let', 'do',
                  'if', 'else', 'while',
                  'return', 'void')

Token_symbols = ('(', ')', '{', '}', '[', ']', '.', ',', ';', '+', '-', '*',
                 '/', '&', '|', '>', '<', '=', '~', '^', '#')

Token_symbols_additions = {"&": "&amp;", ">": "&gt;", "<": "&lt;"}


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.

    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters,
    and comments, which are ignored. There are three possible comment formats:
    /* comment until closing */ , /** API comment until closing */ , and
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' |
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' |
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate
    file. A compilation unit is a single class. A class is a sequence of tokens
    structured according to the following context free syntax:

    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type)
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement |
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{'
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions

    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName |
            varName '['expression']' | subroutineCall | '(' expression ')' |
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className |
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'

    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()

        file_str = " ".join(clean_file(input_stream))

        keyword_regex = 'class|method|function|constructor|int|boolean|char|' \
                        'void|var|static|field|let|do|if|else|while|return|true|' \
                        'false|null|this'
        symbolReg = '{|}|\[|\]|\(|\)|\.|,|;|\+|-|\*|\/|&|\||<|>|=|~'
        int_const_regex = '\d+|\w+'
        str_const_regex = '[\\"][^\\";]+[\\"]'

        self.tokens_lst = re.findall(int_const_regex + "|" + keyword_regex +
                                     "|" + symbolReg + "|" + str_const_regex, file_str)
        self.current_token = ""
        self.token_index = -1

    """ - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
    """

    def get_token(self):
        return self.current_token

    def get_tokens_lst(self):
        return self.tokens_lst

    def get_cur_token_index(self):
        return self.token_index

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        if self.token_index >= len(self.tokens_lst):
            return False
        return True

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        if self.has_more_tokens():
            self.current_token = self.tokens_lst[self.token_index]
            self.token_index += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.tokens_lst[self.token_index] in Token_keyWords:
            return "KEYWORD"

        elif self.tokens_lst[self.token_index] in Token_symbols:
            return "SYMBOL"

        elif self.tokens_lst[self.token_index].isdigit():
            return "INT_CONST"
        elif self.tokens_lst[self.token_index][0] == '"':
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.tokens_lst[self.token_index]

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        temp_token = self.tokens_lst[self.token_index]
        if temp_token in Token_symbols_additions:
            return Token_symbols_additions[temp_token]
        return temp_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.tokens_lst[self.token_index]

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return self.tokens_lst[self.token_index]

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
        """
        return self.tokens_lst[self.token_index][1:-1]

    def get_token_val(self):
        if self.token_type() == "KEYWORD":
            return self.keyword()
        elif self.token_type() == "SYMBOL":
            return self.symbol()
        elif self.token_type() == "INT_CONST":
            return self.int_val()
        elif self.token_type() == "STRING_CONST":
            return self.string_val()
        elif self.token_type() == "IDENTIFIER":
            return self.identifier()

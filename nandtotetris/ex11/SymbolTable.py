"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        self.arithmatic_commands = {"+": "ADD", "-": "SUB", "&": "AND", "|": "OR", "<": "LT",
                 ">": "GT","=":"EQ"}

        self.segments_dic = {"constant": "CONST", "argument": "ARG", "local": "VAR",
                             "static": "STATIC", "this": "THIS", "that": "THAT",
                             "pointer": "POINTER", "temp": "TEMP", "field": "FIELD"}

        self.class_symbol_table = {}
        self.current_subroutine_symbol_table = {}
        self.argument_counter = 0
        self.static_counter = 0
        self.local_counter = 0

        self.field_counter = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        self.argument_counter = 0
        self.local_counter = 0
        self.current_subroutine_symbol_table = {}

    def in_symbol_table(self, string):
        if string in self.class_symbol_table or string in self.current_subroutine_symbol_table:
            return True
        return False


    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind == "STATIC":
            self.class_symbol_table[name] = [type, kind, self.static_counter]
            self.static_counter += 1
        elif kind == "FIELD":
            self.class_symbol_table[name] = [type, kind, self.field_counter]
            self.field_counter += 1
        elif kind == "VAR": #todo- local??
            self.current_subroutine_symbol_table[name] = [type, kind, self.local_counter]
            self.local_counter += 1
        elif kind == "ARG":
            self.current_subroutine_symbol_table[name] = [type, kind, self.argument_counter]
            self.argument_counter += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind == "STATIC":
            return self.static_counter
        elif kind == "FIELD":
            return self.field_counter
        elif kind == "VAR": #todo- local??
            return self.local_counter
        elif kind == "ARG":
            return self.argument_counter


    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        if name in self.current_subroutine_symbol_table:
            return  self.current_subroutine_symbol_table[name][1]
        elif name in self.class_symbol_table:
            return self.class_symbol_table[name][1]
        else:
            return None

    def type_of(self, name: str) -> str: #todo - check if not in dicts
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.current_subroutine_symbol_table:
            return self.current_subroutine_symbol_table[name][0]
        else:
            return self.class_symbol_table[name][0]

    def index_of(self, name: str) -> int: #todo - check if not in dicts
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.current_subroutine_symbol_table:
            return self.current_subroutine_symbol_table[name][2]
        else:
            return self.class_symbol_table[name][2]

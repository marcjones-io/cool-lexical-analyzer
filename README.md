# cool lexical analyzer 
Classroom Object-Oriented Language “COOL” is a programming language created by [Alexander Aiken](https://theory.stanford.edu/~aiken/ "Alexander Aiken") of Stanford to represent a subset of of Java. Cool also was influenced by Pascal and the functional programming paradigms of ML.

This program is a lexical analyzer (or “scanner”) for the COOL language written in Python using the [Python Lex-Yacc “PLY” library](http://www.dabeaz.com/ply/ "PLY"). The scanner accepts a COOL source file - __*.cl__ format - and using regular expressions, reads through the .cl file to return a serialized list of COOL tokens - or an empty output file with an error written to the command line.
### instructions:
* Run the program by placing a .cl file in the executable’s directory and run python with the scanner filename and the COOL file name in tow. 

    Example: __python scanner.py cool_filename.cl__

* If there were no errors in the provided, the scanner will create the serialized list of tokens in a file with the same name as the input with “-lex” appended to its extension. 

    Example: __cool_filename.cl-lex__
    
* This file can be opened and viewed in any standard text editor. However if your inputted COOL program does in fact contain improper tokens, the scanner will spit out an error message to the console.

    Example: __ERROR: line_number: Lexer: message__


### notes:
For more information on COOL language rules and syntax:
https://theory.stanford.edu/~aiken/software/cool/cool-manual.pdf

For more information of the history of COOL:
https://en.wikipedia.org/wiki/Cool_(programming_language)

To learn more about the techniques used in this code watch Wes Weimer's PLY + Python lexing tutorial:
https://youtu.be/pJxgoeTT2QA

Cool example files come from UVA CS Professor [Wes Weimer](http://www.cs.virginia.edu/~weimer/ "Wes Weimer")
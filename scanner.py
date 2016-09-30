# Marc Jones - 2016
# COOL Lexer
# This program has code adapted from Wes Weimer's lexing tutorial (https://youtu.be/pJxgoeTT2QA) 
#     along with the Python Lex-Yacc "PLY" documentation

import sys
import lex as lex

# List of eligible COOL tokens (in alphabetical order)
tokens = (
   'at', 
   'case', 'class', 
   'colon', 'comma', 
   'divide', 'dot', 
   'else', 'equals', 'esac', 
   'false', 'fi', 
   'identifier', 'if', 'in', 'inherits', 'integer', 'isvoid', 
   'larrow', 'lbrace', 'le', 'let', 'loop', 'lparen', 'lt', 
   'minus', 
   'new', 'not', 
   'of',
   'plus', 'pool', 
   'rarrow', 'rbrace', 'rparen', 
   'semi', 'string', 
   'then', 'tilde', 'times', 'true', 'type', 'while',
   'blkcomm' #blkcomm = blocked comments
)

# Regular expression rules for simple tokens
t_at = r'@'
t_colon = r':'
t_comma = r','
t_divide = r'[/]' 
t_dot = r'[.]'
t_equals = r'='
t_larrow = r'<-' 
t_lbrace = r'{'
t_le = r'<=' #le =  less than or equal to
t_lparen = r'[(]'
t_lt = r'<' #lt = less than
t_minus = r'-'
t_plus = r'[+]'
t_rarrow = r'=>'
t_rbrace = r'}'
t_rparen = r'[)]'
t_semi = r';'
t_tilde = r'~'
t_times = r'[*]'

def t_ignore_inlinecomments(t):
    r'[-][-][^\n]*'

states = (
   ('blkcomm','exclusive'),
)

# Match the first (* and enter 'blkcomm' state as to handle multi line and multi braced blocked comments
def t_blkcomm(t):
    r'[(][*]'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('blkcomm')

def t_blkcomm_opencomm(t):     
    r'[(][*]'
    t.lexer.level +=1                

def t_blkcomm_newline(t):
    r'[\n]+'

def t_blkcomm_closecomm(t):
    r'.*?[*][)]'
    t.lexer.level -=1
    #if closing brace is found, return the code fragment
    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
         t.type = "blkcomm"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')           

# String as defined in COOL
def t_blkcomm_string(t):
    r'["].*?["]'

# Any sequence of non-whitespace characters (not braces, strings)
def t_blkcomm_nonspace(t):
    r'[^\s\{\}\'\"]+'

def t_blkcomm_dot(t):
    r'.'

def t_blk_inlinecomments(t):
    r'[-][-][^\n]*'

def t_blkcomm_eof(t):
  print ("ERROR: %d: Lexer: EOF found in comment" % (t.lexer.lineno))
  exit(1)

# Ignored characters (whitespace)
t_blkcomm_ignore = " \t\n"

# For bad characters, we just skip over it
def t_blkcomm_error(t):
    print ("ERROR: %d: Lexer: Invalid character in blocked comment" % (t.lexer.lineno))
    exit(1)

# Integers may not exceed a value of 2147483647 in COOL
def t_integer(t):
    r'[0-9]+'
    tempval = long(t.value)  
    if tempval > 2147483647:
        print ("ERROR: %d: Lexer: Int value '%s' exceeds 32-bit allotment" % (t.lexer.lineno,tempval))
        exit(1)
    else:
        return t

def t_case(t):
    r'case\b'
    return t

def t_class(t):
    r'class\b'
    return t

def t_else(t):
    r'else\b'
    return t

def t_esac(t):
    r'esac\b'
    return t

def t_false(t):
    r'false\b'
    return t

def t_fi(t):
    r'fi\b'
    return t

def t_if(t):
    r'if\b'
    return t

def t_inherits(t): #inherits can be easily mistaken as "in" (as lexing works with maximal munch) therefore it comes first in rule order
    r'inherits\b'
    return t

def t_in(t):
    r'in\b'
    return t

def t_isvoid(t):
    r'isvoid\b'
    return t

def t_let(t):
    r'let\b'
    return t

def t_loop(t):
    r'loop\b'
    return t

def t_new(t):
    r'new\b'
    return t

def t_not(t):
    r'not\b'
    return t

def t_of(t):
    r'of\b'
    return t

def t_pool(t):
    r'pool\b'
    return t

def t_then(t):
    r'then\b'
    return t

def t_true(t):
    r'true\b'
    return t

def t_while(t):
    r'while\b'
    return t

def t_string(t):
    r'["].*?["]'
    ogstring = str(t.value)
    ogstring = ogstring[1:len(ogstring)-1]
    t.value = ogstring
    if len(str(t.value)) > 1024 : #ensures string length is less than 1024
        print ("ERROR %d: Lexer: String exceeds 1024 characters" % (t.lexer.lineno))
        exit(1)
    elif chr(0) in str(t.value): #check for nul byte in string
        print ("ERROR: %d: Lexer: String cannot have null characters" % (t.lexer.lineno))
        exit(1)
    else:
        return t

def t_type(t):
    r'(?:[A-Z])+(?:_|[0-9]|[A-Z]|[a-z])*'
    return t

def t_identifier(t):
    r'(?:[a-z])+(?:_|[0-9]|[A-Z]|[a-z])*'
    return t

t_ignore  = ' \t\f\r\v' #ignores whitespace, linefeed, tabs

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 

# Error handling rule
def t_error(t):
    print ("ERROR: %d: Lexer: Illegal character '%s'" % (t.lexer.lineno,t.value[0]))
    exit(1) #exits program after coming across first error

# Build the lexer
lexer = lex.lex()

# Run the lexer ...
filename = sys.argv[1] #accept command line arg of external input
file_handler = open (filename, "r") #opens the input to the program
file_contents = file_handler.read() #reads in file contents
lexer.input(file_contents) #feed file contents into lexer

# Tokenize
out_string = "" #write all content to string before outputting ot file
outfile = open (filename+"-lex", "w") 
while True:
    tok = lexer.token()
    if not tok: 
        break # No more input
    out_string = out_string + str(tok.lineno) + "\n"
    out_string = out_string + str(tok.type) + "\n"
    if tok.type in [ 'integer', 'identifier', 'type', 'string' ]: #determine which token type to print
        out_string = out_string + str(tok.value) + "\n" #casts value of token.type to string for safety
outfile.write(out_string)
outfile.close()

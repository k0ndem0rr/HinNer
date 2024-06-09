grammar hm;

root:
    (line '\n'+)* line '\n'*
    ;

line:
    (application | lambda | def)
    ;

def:
    application '::' type
    ;

type:
    MAYUS                   #typeLast
    | MAYUS '->' type       #typeMiddle
    ;

application:
    application application        #app
    | '(' application ')'   #appParens
    | expr                  #appExpr
    ;

expr:
    NUMBER                  #numberExpr   
    | VARIABLE              #variableExpr
    | lambda                #lambdaExpr 
    | OPERATION             #operationExpr
    ;

lambda:
    '\\' VARIABLE '->' application
    ;

VARIABLE: [a-z]+ ;
OPERATION: '(' ('+' | '-' | '*' | '/' | '^') ')' ;
NUMBER: [0-9]+ ;
MAYUS : [A-Z]+ ;
WS : [ \t\r]+ -> skip ;
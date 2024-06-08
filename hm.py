import streamlit as st
from antlr4 import *
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor
from dataclasses import dataclass
from graphviz import Digraph
import pandas as pd

# grammar hm;

# root: line+;

# line: (application | lambda | def) '\n'*
# ;

# def:
#     application '::' type
#     ;

# type:
#     MAYUS                   #typeLast
#     | MAYUS '->' type       #typeMiddle
#     ;

# application:
#     application expr        #app
#     | '(' application ')'   #appParens
#     | expr                  #appExpr
#     ;

# expr:
#     NUMBER                  #numberExpr
#     | VARIABLE              #variableExpr
#     | lambda                #lambdaExpr
#     | OPERATION             #operationExpr
#     ;

# lambda:
#     '\\' VARIABLE '->' application
#     ;

# VARIABLE: [a-z]+ ;
# OPERATION: '(' ('+' | '-' | '*' | '/' | '^') ')';
# NUMBER: [0-9]+ ;
# MAYUS : [A-Z]+ ;
# WS : [ \t\r]+ -> skip;


@dataclass
class TreeNode:
    name: str
    children: list
    type: str = None


def nextType(type: str):
    if type == "":
        return "a"

    # Convertir la cadena en una lista de caracteres
    # para facilitar la manipulación
    type_list = list(type)

    # Empezar desde el final de la cadena
    for i in range(len(type_list) - 1, -1, -1):
        if type_list[i] == 'z':
            # Si el carácter actual es 'z', se convierte en 'a'
            type_list[i] = 'a'
        else:
            # Incrementar el carácter actual y terminar
            type_list[i] = chr(ord(type_list[i]) + 1)
            break
    else:
        # Si hemos convertido todas las 'z' en 'a',
        # agregar una 'a' al principio
        type_list.insert(0, 'a')

    # Unir la lista de caracteres en una cadena y devolverla
    return ''.join(type_list)


def splitType(type: str):
    if type == "" or type is None or type[0] != '(':
        return ("", type)

    # Convertir la cadena en una lista de caracteres
    # para facilitar la manipulación
    type_list = list(type)
    entryType = ""

    # Empezar desde el principio de la cadena
    for i in range(len(type_list)):
        if type_list[0] == '-':
            break
        if type_list[0] != '(' and type_list[0] != ' ':
            entryType += type_list[0]
        type_list.pop(0)
    while type_list[0] == ' ' or type_list[0] == '>' or type_list[0] == '-':
        type_list.pop(0)

    # Borra el último carácter: ')'
    type_list.pop(-1)

    # Unir la lista de caracteres en una cadena y devolverla
    return (entryType, ''.join(type_list))


def defineType(self, var, isLambda=False):
    type = None
    if self.definitions:
        for name, t in self.definitions:
            if name == var.getText():
                type = t
                if self.entryType != "" and type != self.entryType:
                    self.errorMsg = f"Error: {var.getText()}"
                    self.errorMsg += f" no es de tipo {self.entryType},"
                    self.errorMsg += f" es de tipo {type}"
                    self.appType = ""
                break
    if type is None:
        if self.appType != '':
            if isLambda:
                type = f'({self.entryType} -> {self.appType})'
            else:
                type = self.appType
        else:
            type = nextType(self.lastRandomType)
            self.lastRandomType = type
        self.definitions.append((var.getText(), type))
    return type


class TreeVisitor(hmVisitor):
    def __init__(self):
        self.definitions = []
        self.errorMsg = ''
        self.lastRandomType = ''
        self.appType = ''
        self.entryType = ''

    def visitRoot(self, ctx: hmParser.RootContext):
        children = [self.visit(child) for child in ctx.getChildren()]
        return TreeNode(name='root', children=children)

    def visitLine(self, ctx: hmParser.LineContext):
        return self.visit(ctx.getChild(0))

    def visitDef(self, ctx: hmParser.DefContext):
        [application, _, type] = ctx.getChildren()
        type = self.visit(type)
        self.definitions.append((application.getText(), type.type))
        return TreeNode(name='::', children=[type])

    def visitTypeLast(self, ctx: hmParser.TypeLastContext):
        [type] = list(ctx.getChildren())
        return TreeNode(name=type.getText(), children=[], type=type.getText())

    def visitTypeMiddle(self, ctx: hmParser.TypeMiddleContext):
        [type, _, nextType] = list(ctx.getChildren())
        nextType = self.visit(nextType)
        return TreeNode(name=type.getText(),
                        children=[nextType],
                        type=f'({type.getText()} -> {nextType.type})')

    def visitApp(self, ctx: hmParser.AppContext):
        [expr, app] = list(ctx.getChildren())

        # Le doy un tipo provisional a la aplicación
        type = nextType(self.lastRandomType)
        self.lastRandomType = self.lastRandomType

        # Visito la expresión
        expr = self.visit(expr)

        # Extraigo el tipo de la aplicación y el de la entrada
        entryType, appType = splitType(expr.type)

        # Si el tipo de la entrada es vacío,
        # entonces la aplicación también lo es
        if entryType == '':
            appType = ''

        self.entryType = entryType
        self.appType = appType

        # Visito la aplicación
        app = self.visit(app)

        # Si la aplicación no ha coincidido con la entrada,
        # entonces hay un error
        if self.appType == '':
            self.entryType = ''
        # Si la aplicación coincide con la entrada, ya tenemos tipo
        else:
            type = self.appType

        self.definitions.append((f'{ctx.getText()}', type))

        return TreeNode(name='@', children=[expr, app], type=type)

    def visitAppParens(self, ctx: hmParser.AppParensContext):
        [_, app, _] = list(ctx.getChildren())
        return self.visit(app)

    def visitAppExpr(self, ctx: hmParser.AppExprContext):
        return self.visit(ctx.getChild(0))

    def visitNumberExpr(self, ctx: hmParser.NumberExprContext):
        [number] = list(ctx.getChildren())
        return TreeNode(name=number.getText(),
                        children=[],
                        type=defineType(self, number))

    def visitVariableExpr(self, ctx: hmParser.VariableExprContext):
        [variable] = list(ctx.getChildren())
        return TreeNode(name=variable.getText(),
                        children=[],
                        type=defineType(self, variable))

    def visitOperationExpr(self, ctx: hmParser.OperationExprContext):
        [operation] = list(ctx.getChildren())
        return TreeNode(name=operation.getText(),
                        children=[],
                        type=defineType(self, operation))

    def visitLambdaExpr(self, ctx: hmParser.LambdaExprContext):
        return self.visit(ctx.getChild(0))

    def visitLambda(self, ctx: hmParser.LambdaContext):
        [_, variable, _, application] = list(ctx.getChildren())
        application = self.visit(application)
        lambdaType = defineType(self, ctx, True)
        variable = TreeNode(name=variable.getText(),
                            children=[],
                            type=defineType(self, variable))
        return TreeNode(name='λ',
                        children=[variable, application],
                        type=lambdaType)


def parse_input(input):
    input_stream = InputStream(input)
    lexer = hmLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = hmParser(token_stream)
    tree = parser.root()
    visitor = TreeVisitor()
    if parser.getNumberOfSyntaxErrors() == 0:
        return visitor.visit(tree), visitor.definitions, visitor.errorMsg
    else:
        return (parser.getNumberOfSyntaxErrors(),
                tree.toStringTree(recog=parser))


def render_tree(node, dot=None, parent=None):
    if dot is None:
        dot = Digraph()
        dot.node(
            name=node.name,
            label=node.name + (f" \n{node.type}" if node.type else ''))
        parent = node.name
    for child in node.children:
        if isinstance(child, TreeNode):
            child_id = str(id(child))
            dot.node(
                name=child_id,
                label=child.name + (f" \n{child.type}" if child.type else ''))
            dot.edge(parent, child_id)
            child.appType = ''
            child.entryType = ''
            render_tree(child, dot, child_id)
    return dot


st.title("Konde's HinNer type analyzer")

input_text = st.text_area('Input')

if st.button('Run'):
    if input_text:
        tree = parse_input(input_text)
        if isinstance(tree, tuple) and isinstance(tree[0], TreeNode):
            tree, definitions, errorMsg = tree
            if definitions:
                names = [name for name, _ in definitions]
                types = [type for _, type in definitions]
                st.write('Definitions:')
                st.table(pd.DataFrame(types, index=names, columns=['Type']))
            if errorMsg:
                st.write(errorMsg)
            for child in tree.children:
                if isinstance(child, TreeNode) and child.name != '::':
                    dot = render_tree(child)
                    st.graphviz_chart(dot)
        else:
            st.write(f"Syntx errors: {tree[0]}\n{tree[1]}")
    else:
        st.write('Please input something')

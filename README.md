# HinNer

Este proyecto proporciona una app en Streamlit para analizar y visualizar árboles de sintaxis abstracta (AST) generados a partir de una gramática definida en ANTLR.

## Contenido

- [Descripción](#descripción)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción

La aplicación `Hinner` permite a los usuarios ingresar texto conforme a una gramática definida y generar un árbol de sintaxis abstracta (AST) que se visualiza mediante Graphviz. Además, analiza y muestra las definiciones de tipos de las variables y expresiones dentro del texto ingresado.

## Instalación

Para ejecutar esta aplicación localmente, sigue estos pasos:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/k0ndem0rr/HinNer
   cd HinNer
   ```

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Prueba a compilar
   ```
(-)::N->N->N
\x->((-)((\y->(-)y)3(5)))(((-)x)((-)2(4)))
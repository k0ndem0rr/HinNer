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

3. Prueba a compilar y usar
   ```bash
   antlr4 -Dlanguage=Python3 -no-listener -visitor hm.g4
   streamlit run hm.py
   ```

4. Instala lo que te haga falta

## Uso

Una vez funcione el comando ```streamlit run hm.py```, se abrirá automáticamente tu navegador en la web indicada (usualmente `http://localhost:8501`).

## Interacción con la App

1. Introduce el texto que deseas analizar en el área de texto proporcionada.
2. Haz clic en el botón "Run" para procesar el texto.
3. La aplicación mostrará las definiciones y el árbol de sintaxis generado. O los errores de tipo o de sintaxi si es que hay

Prueba por ejemplo con
```hm.g4
(-)::N->N->N
\x->((-)((\y->(-)y)3(5)))(((-)x)((-)2(4)))
```

## Estructura del proyecto

- `hm.py`: El archivo princpal que contiene la app de Streamlit y las funciones de análisis y visualización.
- `hm.g4`: La definición de la gramática en ANTLR

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una rama con tu nueva característica (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commits (`git commit -am 'Añadir nueva característica'`).
4. Sube los cambios a tu repositorio (`git push origin feature/nueva-caracteristica`).
5. Crea un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
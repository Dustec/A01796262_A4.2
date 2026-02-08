# A01796262_A4.2 — Actividad 4.2 Ejercicio de programación 1

Repositorio con los **3 ejercicios de programación** de la Actividad 4.2 (Calidad de Software). Implementados en **Python** siguiendo **PEP 8** y verificados con **PyLint**.

---

## Objetivos de aprendizaje

- **2.4** Explicar la importancia del estilo de codificación de un sistema.
- **2.5** Reconocer los atributos de un estándar de codificación útil para identificar errores.
- **2.6** Identificar estándares de codificación reconocidos en la industria y sus implicaciones.

---

## Requisitos

- **Python 3**
- **PyLint** (recomendado para verificación):  
  `pip install pylint`

---

## Estructura del repositorio

```
├── compute_statistics.py   # Programa 1: estadísticas descriptivas
├── convert_numbers.py     # Programa 2: conversión a binario y hexadecimal
├── word_count.py         # Programa 3: conteo de palabras
├── run_all_tests_P1.py  # Ejecuta todos los casos de prueba P1
├── run_all_tests_P2.py  # Ejecuta todos los casos de prueba P2
├── run_all_tests_P3.py  # Ejecuta todos los casos de prueba P3
├── tests/
│   ├── P1/              # Casos de prueba Programa 1 (TC1–TC7)
│   ├── P2/              # Casos de prueba Programa 2 (TC1–TC4)
│   └── P3/              # Casos de prueba Programa 3 (TC1–TC5)
└── results/
    ├── P1/              # StatisticsResults.txt, TC*_results.txt
    ├── P2/              # ConversionResults.txt, TC*_results.txt
    └── P3/              # WordCountResults.txt, TC*_results.txt
```

---

## Programas

### 1. Compute Statistics (`compute_statistics.py`)

Calcula **estadísticas descriptivas** de un archivo con números (uno por línea): **media, mediana, moda, desviación estándar y varianza**. Los cálculos se realizan con algoritmos básicos (sin librerías estadísticas). Incluye manejo de datos inválidos y tiempo de ejecución en consola y en archivo.

**Uso:**

```bash
python compute_statistics.py <archivo_entrada> <archivo_salida>
```

**Ejemplo:**

```bash
python compute_statistics.py tests/P1/TC1.txt results/P1/StatisticsResults.txt
```

---

### 2. Converter (`convert_numbers.py`)

Convierte números enteros de un archivo a **binario** y **hexadecimal** usando algoritmos propios (sin `bin()`/`hex()` para la lógica principal). Maneja datos inválidos y escribe el tiempo de ejecución en consola y en archivo.

**Uso:**

```bash
python convert_numbers.py <archivo_entrada> <archivo_salida>
```

**Ejemplo:**

```bash
python convert_numbers.py tests/P2/TC1.txt results/P2/ConversionResults.txt
```

---

### 3. Word Count (`word_count.py`)

Cuenta **palabras distintas** y su **frecuencia** en un archivo de texto. Los resultados se imprimen en consola y se guardan en un archivo, con tiempo de ejecución. Implementado con estructuras básicas y manipulación de cadenas.

**Uso:**

```bash
python word_count.py <archivo_entrada> <archivo_salida>
```

**Ejemplo:**

```bash
python word_count.py tests/P3/TC1.txt results/P3/WordCountResults.txt
```

---

## Casos de prueba

Cada programa incluye casos de prueba en `tests/P1`, `tests/P2` y `tests/P3`. Para ejecutar **todos** los casos de un programa:

```bash
python run_all_tests_P1.py   # Programa 1 (7 casos)
python run_all_tests_P2.py   # Programa 2 (4 casos)
python run_all_tests_P3.py   # Programa 3 (5 casos)
```

Los resultados se guardan en `results/P1`, `results/P2` y `results/P3` (archivos por caso y archivo consolidado: `StatisticsResults.txt`, `ConversionResults.txt`, `WordCountResults.txt`).

---

## Verificación con PyLint (PEP 8)

Se debe verificar que no haya errores ni problemas reportados por PyLint:

```bash
pylint compute_statistics.py
pylint convert_numbers.py
pylint word_count.py
```

**Important:** To comply PEP 8 standards the file names were writeen in snake case.

Tipos de mensajes: **(C)** convención, **(R)** refactor, **(W)** warning, **(E)** error, **(F)** fatal. La actividad requiere **cero problemas** para la calificación completa en análisis estático.

[Evidence Pylint](/assets/evidence_pylint.png)

---

## Referencias

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Python Tutorial](https://docs.python.org/3/tutorial/index.html)
- [PyLint en PyPI](https://pypi.org/project/pylint/)

---

**Autor:** A01796262  
**Actividad:** 4.2 Ejercicio de programación 1 — Calidad de Software

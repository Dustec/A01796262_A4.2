"""
Programa para contar la frecuencia de palabras en un archivo de texto.

Autor: A01796262
Fecha: Febrero 2026
"""

import sys
import time
import string


def read_text_from_file(filename):
    """
    Lee el contenido de un archivo de texto.

    Args:
        filename (str): Ruta del archivo a leer

    Returns:
        str: Contenido completo del archivo
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return content

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
        sys.exit(1)
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{filename}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)


def clean_word(word):
    """
    Limpia una palabra removiendo puntuación y convirtiéndola a minúsculas.

    Args:
        word (str): Palabra a limpiar

    Returns:
        str: Palabra limpia en minúsculas, o cadena vacía si no es válida
    """
    # Remover puntuación al inicio y final
    word = word.strip(string.punctuation)

    # Convertir a minúsculas
    word = word.lower()

    # Remover caracteres especiales internos pero mantener guiones y apóstrofos
    # que son comunes en palabras válidas (e.g., "don't", "co-op")
    cleaned = ""
    for char in word:
        if char.isalnum() or char in ['-', "'"]:
            cleaned += char

    return cleaned


def count_words(text):
    """
    Cuenta la frecuencia de cada palabra en el texto.

    Args:
        text (str): Texto a analizar

    Returns:
        dict: Diccionario con palabras como claves y frecuencias como valores
    """
    word_count = {}

    # Dividir el texto en palabras
    words = text.split()

    for word in words:
        # Limpiar la palabra
        cleaned_word = clean_word(word)

        # Ignorar palabras vacías
        if not cleaned_word:
            continue

        # Contar la palabra
        if cleaned_word in word_count:
            word_count[cleaned_word] += 1
        else:
            word_count[cleaned_word] = 1

    return word_count


def sort_word_count(word_count, sort_by='frequency'):
    """
    Ordena el diccionario de conteo de palabras.

    Args:
        word_count (dict): Diccionario de palabras y frecuencias
        sort_by (str): Criterio de ordenamiento:
                      'frequency' - por frecuencia descendente
                      'alphabetical' - alfabéticamente

    Returns:
        list: Lista de tuplas (palabra, frecuencia) ordenadas
    """
    if sort_by == 'frequency':
        # Ordenar por frecuencia descendente, luego alfabéticamente
        sorted_items = sorted(word_count.items(),
                              key=lambda x: (-x[1], x[0]))
    elif sort_by == 'alphabetical':
        # Ordenar alfabéticamente
        sorted_items = sorted(word_count.items(), key=lambda x: x[0])
    else:
        # Por defecto, ordenar por frecuencia
        sorted_items = sorted(word_count.items(),
                              key=lambda x: (-x[1], x[0]))

    return sorted_items


def process_file(filename):
    """
    Procesa el archivo y cuenta las palabras.

    Args:
        filename (str): Ruta del archivo a procesar

    Returns:
        tuple: (sorted_word_count, total_words, unique_words)
    """
    # Leer el archivo
    text = read_text_from_file(filename)

    # Contar palabras
    word_count = count_words(text)

    # Ordenar por frecuencia
    sorted_count = sort_word_count(word_count, sort_by='frequency')

    # Calcular estadísticas
    total_words = sum(word_count.values())
    unique_words = len(word_count)

    return sorted_count, total_words, unique_words


def display_results(sorted_count, total_words, unique_words, elapsed_time):
    """
    Muestra los resultados en consola.

    Args:
        sorted_count (list): Lista de tuplas (palabra, frecuencia) ordenadas
        total_words (int): Total de palabras procesadas
        unique_words (int): Total de palabras únicas
        elapsed_time (float): Tiempo de ejecución en segundos
    """
    print("\n" + "=" * 70)
    print("CONTEO DE FRECUENCIA DE PALABRAS")
    print("=" * 70)
    print(f"Total de palabras: {total_words}")
    print(f"Palabras únicas: {unique_words}")
    print("=" * 70)
    print(f"{'PALABRA':<30} {'FRECUENCIA':<15} {'PORCENTAJE':<15}")
    print("-" * 70)

    for word, count in sorted_count:
        percentage = (count / total_words) * 100
        print(f"{word:<30} {count:<15} {percentage:>6.2f}%")

    print("=" * 70)
    print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
    print("=" * 70 + "\n")


def save_results_to_file(sorted_count, total_words, unique_words,
                         elapsed_time, output_filename):
    """
    Guarda los resultados en un archivo.

    Args:
        sorted_count (list): Lista de tuplas (palabra, frecuencia) ordenadas
        total_words (int): Total de palabras procesadas
        unique_words (int): Total de palabras únicas
        elapsed_time (float): Tiempo de ejecución en segundos
        output_filename (str): Ruta del archivo de salida
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("=" * 70 + "\n")
            file.write("CONTEO DE FRECUENCIA DE PALABRAS\n")
            file.write("=" * 70 + "\n")
            file.write(f"Total de palabras: {total_words}\n")
            file.write(f"Palabras únicas: {unique_words}\n")
            file.write("=" * 70 + "\n")
            file.write(
                f"{'PALABRA':<30} {'FRECUENCIA':<15} {'PORCENTAJE':<15}\n")
            file.write("-" * 70 + "\n")

            for word, count in sorted_count:
                percentage = (count / total_words) * 100
                file.write(f"{word:<30} {count:<15} {percentage:>6.2f}%\n")

            file.write("=" * 70 + "\n")
            file.write(f"Tiempo de ejecución: {elapsed_time:.6f} segundos\n")
            file.write("=" * 70 + "\n")

        print(f"✓ Resultados guardados en: {output_filename}")

    except PermissionError:
        print(f"Error: No se tiene permiso para escribir en "
              f"'{output_filename}'")
    except Exception as e:
        print(f"Error al guardar resultados: {e}")


def main():
    """Función principal del programa."""
    if len(sys.argv) != 3:
        print("Error: Uso incorrecto del programa")
        print("Uso: python wordCount.py <input_file> <output_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    start_time = time.time()
    sorted_count, total_words, unique_words = process_file(input_filename)
    elapsed_time = time.time() - start_time

    # Mostrar resultados en consola
    display_results(sorted_count, total_words, unique_words, elapsed_time)

    # Guardar resultados en archivo
    save_results_to_file(sorted_count, total_words, unique_words,
                         elapsed_time, output_filename)


if __name__ == "__main__":
    main()

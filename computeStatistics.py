"""
Programa para calcular estadísticas descriptivas de un archivo de datos.

Autor: A01796262
Fecha: Febrero 2026
"""

import sys
import time


def read_numbers_from_file(filename):
    """
    Lee números desde un archivo, uno por línea.
    Acepta comas (,) y punto y coma (;) como separadores decimales.

    Args:
        filename (str): Ruta del archivo a leer

    Returns:
        list: Lista de números flotantes válidos
    """
    numbers = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:  # Saltar líneas vacías
                    continue

                # Primero intentar conversión directa
                try:
                    number = float(line)
                    numbers.append(number)
                except ValueError:
                    # Si falla, normalizar separadores y reintentar
                    normalized = line.replace(',', '.').replace(';', '.')
                    try:
                        number = float(normalized)
                        numbers.append(number)
                        if normalized != line:
                            print(f"Advertencia: Línea {line_num} tenía "
                                  f"separador no estándar '{line}', "
                                  f"convertido a: {number}")
                    except ValueError:
                        # Si aún falla, intentar limpiar la cadena normalizada
                        cleaned = clean_numeric_string(normalized)
                        if cleaned is not None:
                            numbers.append(cleaned)
                            print(f"Advertencia: Línea {line_num} contiene "
                                  f"datos no numéricos '{line}', "
                                  f"se extrajo: {cleaned}")
                        else:
                            print(f"Advertencia: Línea {line_num} contiene "
                                  f"datos inválidos '{line}' y fue ignorada")

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
        sys.exit(1)
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{filename}'")
        sys.exit(1)

    if not numbers:
        print("Error: No se encontraron datos numéricos válidos en el archivo")
        sys.exit(1)

    return numbers


def clean_numeric_string(text):
    """
    Intenta extraer un número de una cadena sucia.
    Acepta comas (,) y punto y coma (;) como separadores decimales.

    Args:
        text (str): Cadena que puede contener caracteres no numéricos

    Returns:
        float or None: Número extraído o None si no se pudo extraer
    """
    # Normalizar separadores decimales: reemplazar , y ; por .
    text = text.replace(',', '.').replace(';', '.')

    result = ""
    decimal_found = False
    has_digits = False

    for i, char in enumerate(text):
        if char.isdigit():
            result += char
            has_digits = True
        elif char == '.' and not decimal_found:
            result += char
            decimal_found = True
        elif char == '-' and i == 0:
            result += char

    if has_digits:
        try:
            return float(result)
        except ValueError:
            return None
    return None


def calculate_mean(numbers):
    """
    Calcula la media aritmética.

    Args:
        numbers (list): Lista de números

    Returns:
        float: Media aritmética
    """
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """
    Calcula la mediana.

    Args:
        numbers (list): Lista de números

    Returns:
        float: Mediana
    """
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    if n % 2 == 0:
        # Si hay cantidad par, promedio de los dos valores centrales
        return (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    else:
        # Si hay cantidad impar, valor central
        return sorted_numbers[n // 2]


def calculate_mode(numbers):
    """
    Calcula la moda (valor más frecuente).

    Args:
        numbers (list): Lista de números

    Returns:
        float or None: Moda o None si no hay moda única
    """
    # Contar frecuencias manualmente
    frequency = {}
    for num in numbers:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    # Encontrar la frecuencia máxima
    max_frequency = max(frequency.values())

    # Encontrar todos los valores con frecuencia máxima
    modes = [num for num, freq in frequency.items()
             if freq == max_frequency]

    # Si todos los números aparecen la misma cantidad de veces,
    # no hay moda
    if len(modes) == len(frequency):
        return None

    # Si hay múltiples modas, retornar la primera encontrada
    return modes[0]


def calculate_variance(numbers, mean):
    """
    Calcula la varianza poblacional.

    Args:
        numbers (list): Lista de números
        mean (float): Media aritmética

    Returns:
        float: Varianza poblacional
    """
    squared_diff_sum = sum((num - mean) ** 2 for num in numbers)
    return squared_diff_sum / len(numbers)


def calculate_std_dev(variance):
    """
    Calcula la desviación estándar poblacional.

    Args:
        variance (float): Varianza

    Returns:
        float: Desviación estándar poblacional
    """
    return variance ** 0.5


def process_file(filename):
    """
    Procesa el archivo y calcula todas las estadísticas.

    Args:
        filename (str): Ruta del archivo a procesar

    Returns:
        dict: Diccionario con todas las estadísticas calculadas
    """
    numbers = read_numbers_from_file(filename)

    count = len(numbers)
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    variance = calculate_variance(numbers, mean)
    std_dev = calculate_std_dev(variance)

    return {
        'filename': filename,
        'count': count,
        'mean': mean,
        'median': median,
        'mode': mode,
        'variance': variance,
        'std_dev': std_dev
    }


def format_value(value):
    """
    Formatea un valor para impresión con manejo de None y números grandes.

    Args:
        value: Valor a formatear

    Returns:
        str: Valor formateado
    """
    if value is None:
        return "N/A"
    elif isinstance(value, (int, float)):
        # Para números muy grandes, usar notación científica
        if abs(value) > 1e15:
            return f"{value:.10e}"
        else:
            return f"{value:.10f}"
    else:
        return str(value)


def display_results(result, elapsed_time):
    """
    Muestra los resultados en consola.

    Args:
        result (dict): Diccionario con los resultados
        elapsed_time (float): Tiempo de ejecución en segundos
    """
    print("\n" + "=" * 60)
    print(f"Archivo de entrada: {result['filename']}")
    print("=" * 60)
    print(f"COUNT:             {result['count']}")
    print(f"MEAN:              {format_value(result['mean'])}")
    print(f"MEDIAN:            {format_value(result['median'])}")
    print(f"MODE:              {format_value(result['mode'])}")
    print(f"STANDARD DEV:      {format_value(result['std_dev'])}")
    print(f"VARIANCE:          {format_value(result['variance'])}")
    print("=" * 60)
    print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
    print("=" * 60 + "\n")


def save_results_to_file(result, elapsed_time, output_filename):
    """
    Guarda los resultados en un archivo.

    Args:
        result (dict): Diccionario con los resultados
        elapsed_time (float): Tiempo de ejecución en segundos
        output_filename (str): Ruta del archivo de salida
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("=" * 60 + "\n")
            file.write(f"Archivo de entrada: {result['filename']}\n")
            file.write("=" * 60 + "\n")
            file.write(f"COUNT:             {result['count']}\n")
            file.write(f"MEAN:              {format_value(result['mean'])}\n")
            file.write(
                f"MEDIAN:            {format_value(result['median'])}\n")
            file.write(f"MODE:              {format_value(result['mode'])}\n")
            file.write(f"STANDARD DEV:      "
                       f"{format_value(result['std_dev'])}\n")
            file.write(f"VARIANCE:          "
                       f"{format_value(result['variance'])}\n")
            file.write("=" * 60 + "\n")
            file.write(f"Tiempo de ejecución: {elapsed_time:.6f} segundos\n")
            file.write("=" * 60 + "\n")

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
        print("Uso: python computeStatistics.py <input_file> <output_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    start_time = time.time()
    result = process_file(input_filename)
    elapsed_time = time.time() - start_time

    # Mostrar resultados en consola
    display_results(result, elapsed_time)

    # Guardar resultados en archivo
    save_results_to_file(result, elapsed_time, output_filename)


if __name__ == "__main__":
    main()

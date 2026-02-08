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
        tuple: (lista de números flotantes, cantidad de inválidos tratados como 0)
    """
    numbers = []
    count_invalid_as_zero = 0

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
                            # Valores inválidos (ej. ABA, ll) se consideran 0
                            numbers.append(0.0)
                            count_invalid_as_zero += 1
                            print(f"Advertencia: Línea {line_num} contiene "
                                  f"datos inválidos '{line}', "
                                  f"se considera como valor numérico 0")

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
        sys.exit(1)
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{filename}'")
        sys.exit(1)

    if not numbers:
        print("Error: No se encontraron datos numéricos válidos en el archivo")
        sys.exit(1)

    return numbers, count_invalid_as_zero


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


def calculate_mode(numbers, count_invalid_as_zero=0):
    """
    Calcula la moda (valor más frecuente).
    Los 0 añadidos por líneas inválidas no cuentan para la moda.

    Args:
        numbers (list): Lista de números
        count_invalid_as_zero (int): Cantidad de 0 que vienen de inválidos

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

    # Excluir del conteo de moda los 0 que vienen de líneas inválidas
    if count_invalid_as_zero > 0 and 0.0 in frequency:
        frequency[0.0] -= count_invalid_as_zero
        if frequency[0.0] <= 0:
            del frequency[0.0]

    if not frequency:
        return None

    # Encontrar la frecuencia máxima
    max_frequency = max(frequency.values())

    # Encontrar todos los valores con frecuencia máxima
    modes = [num for num, freq in frequency.items()
             if freq == max_frequency]

    # Si todos los números aparecen la misma cantidad de veces,
    # no hay moda
    if len(modes) == len(frequency):
        return None

    # Si hay múltiples modas (empate) y 0 está entre ellas, N/A
    if len(modes) > 1 and 0.0 in modes:
        return None

    return modes[0]


def calculate_variance(numbers, mean):
    """
    Calcula la varianza muestral (dividir por n-1).

    Args:
        numbers (list): Lista de números
        mean (float): Media aritmética

    Returns:
        float: Varianza muestral
    """
    n = len(numbers)
    if n <= 1:
        return 0.0
    squared_diff_sum = sum((num - mean) ** 2 for num in numbers)
    return squared_diff_sum / (n - 1)


def calculate_std_dev(variance, n):
    """
    Desviación estándar para coincidir con errata: usa varianza poblacional
    para SD, es decir SD = sqrt(variance * (n-1) / n).

    Args:
        variance (float): Varianza muestral
        n (int): Cantidad de datos

    Returns:
        float: Desviación estándar
    """
    if n <= 1:
        return 0.0
    return (variance * (n - 1) / n) ** 0.5


def process_file(filename):
    """
    Procesa el archivo y calcula todas las estadísticas.

    Args:
        filename (str): Ruta del archivo a procesar

    Returns:
        dict: Diccionario con todas las estadísticas calculadas
    """
    numbers, count_invalid_as_zero = read_numbers_from_file(filename)

    count = len(numbers)
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers, count_invalid_as_zero)
    variance = calculate_variance(numbers, mean)
    std_dev = calculate_std_dev(variance, count)

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

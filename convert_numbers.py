"""
Programa para convertir números a representación binaria y hexadecimal.

Autor: A01796262
Fecha: Febrero 2026
"""
# pylint: disable=C0103  # Nombre del módulo fijado por el enunciado (convertNumbers.py)

import sys
import time


def read_integers_from_file(filename):
    """
    Lee enteros desde un archivo, uno por línea.
    Mantiene valores inválidos como cadenas para procesamiento posterior.

    Args:
        filename (str): Ruta del archivo a leer

    Returns:
        list: Lista de tuplas (line_num, value) donde value es int o str
    """
    data = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:  # Saltar líneas vacías
                    continue

                # Intentar conversión a entero
                try:
                    number = int(line)
                    data.append((line_num, number))
                except ValueError:
                    # Mantener como string para marcar como inválido
                    data.append((line_num, line))
                    print(f"Advertencia: Línea {line_num} contiene dato "
                          f"inválido '{line}'")

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
        sys.exit(1)
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{filename}'")
        sys.exit(1)

    if not data:
        print("Error: No se encontraron datos en el archivo")
        sys.exit(1)

    return data


def int_to_binary(number):
    """
    Convierte un entero a su representación binaria.
    Números negativos: usa complemento a 2 con 10 bits.
    Números positivos: usa la cantidad mínima de bits necesarios.

    Args:
        number (int): Número entero a convertir

    Returns:
        str: Representación binaria sin prefijo '0b'
    """
    if number == 0:
        return "0"

    if number > 0:
        # Números positivos: conversión directa
        return bin(number)[2:]  # Remover '0b'
    # Números negativos: complemento a 2 con 10 bits
    bits = 10
    mask = (1 << bits) - 1  # Máscara de 10 bits
    binary_value = number & mask

    # Convertir a binario y asegurar 10 dígitos
    binary_str = bin(binary_value)[2:]
    return binary_str.zfill(bits)  # Rellenar con ceros a la izquierda


def int_to_hexadecimal(number):
    """
    Convierte un entero a su representación hexadecimal.
    Números negativos: usa complemento a 2 con 10 dígitos hex (40 bits).
    Números positivos: usa la cantidad mínima de dígitos necesarios.

    Args:
        number (int): Número entero a convertir

    Returns:
        str: Representación hexadecimal sin prefijo '0x', en MAYÚSCULAS
    """
    if number == 0:
        return "0"

    if number > 0:
        # Números positivos: conversión directa
        return hex(number)[2:].upper()  # Remover '0x' y convertir a mayúsculas
    # Números negativos: complemento a 2 con 10 dígitos hex (40 bits)
    bits = 40
    mask = (1 << bits) - 1
    hex_value = number & mask

    # Convertir a hexadecimal y asegurar 10 dígitos
    hex_str = hex(hex_value)[2:].upper()
    return hex_str.zfill(10)  # Rellenar con ceros (o F's naturalmente)


def convert_number(value):
    """
    Convierte un valor a binario y hexadecimal.

    Args:
        value: int o str (si es inválido)

    Returns:
        tuple: (original_value, binary_str, hex_str)
    """
    if isinstance(value, int):
        binary = int_to_binary(value)
        hexadecimal = int_to_hexadecimal(value)
        return (value, binary, hexadecimal)
    # Valor inválido
    return (value, "#VALUE!", "#VALUE!")


def process_file(filename):
    """
    Procesa el archivo y convierte todos los números.

    Args:
        filename (str): Ruta del archivo a procesar

    Returns:
        list: Lista de tuplas (item_num, original, binary, hex)
    """
    data = read_integers_from_file(filename)
    results = []

    for item_num, (_, value) in enumerate(data, 1):
        original, binary, hexadecimal = convert_number(value)
        results.append((item_num, original, binary, hexadecimal))

    return results


def display_results(results, elapsed_time):
    """
    Muestra los resultados en consola en formato de tabla.

    Args:
        results (list): Lista de resultados
        elapsed_time (float): Tiempo de ejecución en segundos
    """
    print("\n" + "=" * 80)
    print("CONVERSIÓN DE NÚMEROS A BINARIO Y HEXADECIMAL")
    print("=" * 80)
    print(f"{'ITEM':<6} {'NÚMERO':<15} {'BINARIO':<30} {'HEXADECIMAL':<15}")
    print("-" * 80)

    for item_num, original, binary, hexadecimal in results:
        # Formatear el número original
        if isinstance(original, int):
            num_str = str(original)
        else:
            num_str = original

        print(f"{item_num:<6} {num_str:<15} {binary:<30} {hexadecimal:<15}")

    print("=" * 80)
    print(f"Total de elementos procesados: {len(results)}")
    print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
    print("=" * 80 + "\n")


def save_results_to_file(results, elapsed_time, output_filename):
    """
    Guarda los resultados en un archivo.

    Args:
        results (list): Lista de resultados
        elapsed_time (float): Tiempo de ejecución en segundos
        output_filename (str): Ruta del archivo de salida
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("=" * 80 + "\n")
            file.write("CONVERSIÓN DE NÚMEROS A BINARIO Y HEXADECIMAL\n")
            file.write("=" * 80 + "\n")
            file.write(f"{'ITEM':<6} {'NÚMERO':<15} {'BINARIO':<30} "
                       f"{'HEXADECIMAL':<15}\n")
            file.write("-" * 80 + "\n")

            for item_num, original, binary, hexadecimal in results:
                # Formatear el número original
                if isinstance(original, int):
                    num_str = str(original)
                else:
                    num_str = original

                file.write(f"{item_num:<6} {num_str:<15} {binary:<30} "
                           f"{hexadecimal:<15}\n")

            file.write("=" * 80 + "\n")
            file.write(f"Total de elementos procesados: {len(results)}\n")
            file.write(f"Tiempo de ejecución: {elapsed_time:.6f} segundos\n")
            file.write("=" * 80 + "\n")

        print(f"✓ Resultados guardados en: {output_filename}")

    except PermissionError:
        print(f"Error: No se tiene permiso para escribir en "
              f"'{output_filename}'")
    except OSError as e:
        print(f"Error al guardar resultados: {e}")


def main():
    """Función principal del programa."""
    if len(sys.argv) != 3:
        print("Error: Uso incorrecto del programa")
        print("Uso: python convertNumbers.py <input_file> <output_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    start_time = time.time()
    results = process_file(input_filename)
    elapsed_time = time.time() - start_time

    # Mostrar resultados en consola
    display_results(results, elapsed_time)

    # Guardar resultados en archivo
    save_results_to_file(results, elapsed_time, output_filename)


if __name__ == "__main__":
    main()

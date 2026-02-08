"""
Script para ejecutar todos los casos de prueba del programa P2.
Genera resultados individuales y un archivo consolidado.

Autor: A01796262
Fecha: Febrero 2026
"""

import subprocess
import os
import sys
import time


def ensure_directories():
    """Crea los directorios necesarios si no existen."""
    os.makedirs("results/P2", exist_ok=True)
    print("✓ Directorios verificados")


def run_test_case(test_number):
    """
    Ejecuta un caso de prueba individual.

    Args:
        test_number (int): Número del test case (1-4)

    Returns:
        tuple: (success, elapsed_time, output)
    """
    input_file = f"tests/P2/TC{test_number}.txt"
    output_file = f"results/P2/TC{test_number}_results.txt"

    print(f"\n{'='*60}")
    print(f"Ejecutando TC{test_number}...")
    print(f"{'='*60}")

    if not os.path.exists(input_file):
        print(f"✗ Error: No se encontró el archivo {input_file}")
        return False, 0, ""

    try:
        start_time = time.time()

        # Ejecutar convertNumbers.py
        result = subprocess.run(
            [sys.executable, "convertNumbers.py", input_file, output_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed_time = time.time() - start_time

        if result.returncode == 0:
            print(f"✓ TC{test_number} ejecutado exitosamente")
            print(f"  Tiempo: {elapsed_time:.4f} segundos")
            print(f"  Salida guardada en: {output_file}")

            # Leer el resultado para el consolidado
            with open(output_file, 'r', encoding='utf-8') as f:
                output_content = f.read()

            return True, elapsed_time, output_content
        else:
            print(f"✗ Error al ejecutar TC{test_number}")
            print(f"  Código de error: {result.returncode}")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False, 0, ""

    except subprocess.TimeoutExpired:
        print(f"✗ TC{test_number} excedió el tiempo límite (30s)")
        return False, 0, ""
    except Exception as e:
        print(f"✗ Error inesperado en TC{test_number}: {e}")
        return False, 0, ""


def generate_consolidated_report(results):
    """
    Genera un reporte consolidado con todos los resultados.

    Args:
        results (dict): Diccionario con los resultados de cada test case
    """
    consolidated_file = "results/P2/ConversionResults.txt"

    try:
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("REPORTE CONSOLIDADO - PROGRAMA P2: convertNumbers.py\n")
            f.write("Autor: A01796262\n")
            f.write(f"Fecha de ejecución: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            # Resumen de ejecución
            total_tests = len(results)
            successful_tests = sum(1 for r in results.values() if r['success'])

            f.write("RESUMEN DE EJECUCIÓN:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total de casos de prueba: {total_tests}\n")
            f.write(f"Casos exitosos: {successful_tests}\n")
            f.write(f"Casos fallidos: {total_tests - successful_tests}\n")
            f.write(f"Porcentaje de éxito: "
                   f"{(successful_tests/total_tests)*100:.1f}%\n")
            f.write("-" * 80 + "\n\n")

            # Resultados individuales
            for tc_num in sorted(results.keys()):
                result = results[tc_num]

                f.write("\n" + "=" * 80 + "\n")
                f.write(f"TEST CASE {tc_num}\n")
                f.write("=" * 80 + "\n")

                if result['success']:
                    f.write(f"Estado: EXITOSO\n")
                    f.write(f"Tiempo de ejecución: {result['time']:.4f} "
                           f"segundos\n")
                    f.write("-" * 80 + "\n")
                    f.write(result['output'])
                else:
                    f.write(f"Estado: FALLIDO\n")
                    f.write("-" * 80 + "\n")

                f.write("\n")

            # Pie de página
            f.write("\n" + "=" * 80 + "\n")
            f.write("FIN DEL REPORTE CONSOLIDADO\n")
            f.write("=" * 80 + "\n")

        print(f"\n✓ Reporte consolidado generado: {consolidated_file}")

    except Exception as e:
        print(f"\n✗ Error al generar reporte consolidado: {e}")


def main():
    """Función principal."""
    print("=" * 80)
    print("EJECUTOR DE PRUEBAS - PROGRAMA P2: convertNumbers.py")
    print("=" * 80)

    # Verificar directorios
    ensure_directories()

    # Diccionario para almacenar resultados
    results = {}

    # Ejecutar todos los test cases (TC1 a TC4)
    for i in range(1, 5):
        success, elapsed_time, output = run_test_case(i)
        results[i] = {
            'success': success,
            'time': elapsed_time,
            'output': output
        }

    # Generar reporte consolidado
    print("\n" + "=" * 80)
    print("Generando reporte consolidado...")
    print("=" * 80)
    generate_consolidated_report(results)

    # Resumen final
    total_tests = len(results)
    successful_tests = sum(1 for r in results.values() if r['success'])

    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    print(f"Total de pruebas ejecutadas: {total_tests}")
    print(f"Pruebas exitosas: {successful_tests}")
    print(f"Pruebas fallidas: {total_tests - successful_tests}")
    print(f"Tasa de éxito: {(successful_tests/total_tests)*100:.1f}%")
    print("=" * 80 + "\n")

    # Retornar código de salida
    if successful_tests == total_tests:
        print("✓ Todas las pruebas pasaron exitosamente")
        return 0
    else:
        print(f"✗ {total_tests - successful_tests} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())

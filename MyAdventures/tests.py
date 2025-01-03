import unittest

from MyAdventures.practica import *  # Importa las funciones que necesitas probar
from MyAdventures.pyro_server import *  # Importa las funciones que necesitas probar
from MyAdventures.pyro_client import *  # Importa las funciones que necesitas probar

class TestPracticaFunctions(unittest.TestCase):
    
    def test_function1_practica(self):
        # Llama a la función y verifica el resultado esperado
        result = function1_practica()
        self.assertEqual(result, expected_result)
    
    def test_function2_practica(self):
        # Llama a la función y verifica el resultado esperado
        result = function2_practica()
        self.assertEqual(result, expected_result)

class TestPyroServerFunctions(unittest.TestCase):
    
    def test_function1_pyro_server(self):
        # Llama a la función y verifica el resultado esperado
        result = function1_pyro_server()
        self.assertEqual(result, expected_result)
    
    def test_function2_pyro_server(self):
        # Llama a la función y verifica el resultado esperado
        result = function2_pyro_server()
        self.assertEqual(result, expected_result)

class TestPyroClientFunctions(unittest.TestCase):
    
    def test_function1_pyro_client(self):
        # Llama a la función y verifica el resultado esperado
        result = function1_pyro_client()
        self.assertEqual(result, expected_result)
    
    def test_function2_pyro_client(self):
        # Llama a la función y verifica el resultado esperado
        result = function2_pyro_client()
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

# Use: python -m unittest tests.py

import unittest
from logic_verifier import VerificadorLogico
from logic_ast import Predicado, Simbolo

class TestVerifierCollision(unittest.TestCase):
    def setUp(self):
        self.verifier = VerificadorLogico()

    def test_predicate_collision(self):
        # Case 1: P(a, b)
        # Case 2: P(a_b)
        # These should result in different variable keys.

        f1 = Predicado("P", ("a", "b"))
        f2 = Predicado("P", ("a_b",))

        vars1 = self.verifier.obter_variaveis(f1)
        vars2 = self.verifier.obter_variaveis(f2)

        # We expect vars1 to contain something like "P(a, b)" and vars2 "P(a_b)"
        # But specifically, we expect them to NOT intersect / be equal if the keys represent the formula structure.

        print(f"Vars 1: {vars1}")
        print(f"Vars 2: {vars2}")

        # If they collide, both will be {'P_a_b'} (current buggy behavior)
        # We asserted they should be different.

        # Since they are sets of size 1, we can just compare the sets or the elements.
        self.assertNotEqual(vars1, vars2, "Predicates P(a, b) and P(a_b) collision detected in variable mapping.")

    def test_basic_functioning(self):
        # Ensure that normal functionality is preserved.
        # P(a) -> P(a) should be valid.
        from logic_parser import ParserLogico
        parser = ParserLogico()

        p1 = parser.analisar("P(a)")
        conclusao = parser.analisar("P(a)")

        headers, rows, is_valid = self.verifier.construir_tabela_verdade([p1], conclusao)
        self.assertTrue(is_valid, "P(a) -> P(a) should be valid.")

if __name__ == '__main__':
    unittest.main()

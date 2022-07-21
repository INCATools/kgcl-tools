"""Test ontology model."""
import unittest

from kgcl_schema.schema import get_schemaview


class IntrospectionTestSuite(unittest.TestCase):
    """Test introspection model."""

    def setUp(self) -> None:
        self.schemaview = get_schemaview()

    def test_introspect(self):
        """Test introspections."""
        sv = self.schemaview
        for c in ["edge change", "node deepening"]:
            self.assertIn(c, sv.all_classes())
        for s in ["about node", "was generated by"]:
            self.assertIn(s, sv.all_slots())

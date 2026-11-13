import unittest

from src.markdown_parser import MarkdownParser


class TableFormattingTests(unittest.TestCase):
    def test_header_width(self):
        table = MarkdownParser().parse(
            '| Condition | Color |\n| --- | --- |\n'
            '| A | green |\n'
        )[0]
        self.assertEqual(table.table.property.column_width, [250, 250])
        self.assertTrue(table.table.property.header_row)
        self.assertTrue(table.children[0].children[0].text.elements[0].text_run.text_element_style.bold)

if __name__ == '__main__':
    unittest.main()

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.markdown_parser import MarkdownParser, BlockType
from src.document import add_blocks


class TableImageTests(unittest.TestCase):
    def test_image_only_cells_and_multiple_images(self):
        parser = MarkdownParser(object(), 'doc')
        table = parser.parse('| H |\n| --- |\n| ![a](a.png)<br>![b](b.png) |\n| ![c](c.png) |')[0]
        first, second = table.children[1:]
        self.assertEqual([b.block_type for b in first.children], [BlockType.IMAGE, BlockType.TEXT, BlockType.IMAGE])
        self.assertEqual([b.block_type for b in second.children], [BlockType.IMAGE])
        self.assertEqual([x['image_path'] for x in parser.get_pending_images()], ['a.png', 'b.png', 'c.png'])
        self.assertIs(parser.get_pending_images()[-1]['block'], second.children[0])

    def test_nested_created_image_id_is_recorded(self):
        parser = MarkdownParser(object(), 'doc')
        table = parser.parse('| H |\n| --- |\n| ![a](a.png) |')[0]
        image = parser.get_pending_images()[0]['block']
        counter = iter(range(20))
        def create(request):
            children = []
            for block in request.request_body.children:
                block_id = 'id' + str(next(counter))
                if block.block_type == BlockType.TABLE:
                    children.append(SimpleNamespace(block_id=block_id, table=SimpleNamespace(cells=['cell0', 'cell1'])))
                else:
                    children.append(SimpleNamespace(block_id=block_id))
            return SimpleNamespace(success=lambda: True, data=SimpleNamespace(children=children))
        client = SimpleNamespace(docx=SimpleNamespace(v1=SimpleNamespace(document_block_children=SimpleNamespace(create=create))))
        ids = {}
        with patch('src.document.get_client', return_value=client):
            add_blocks('doc', [table], block_id_map=ids)
        self.assertIn(id(image), ids)

if __name__ == '__main__':
    unittest.main()

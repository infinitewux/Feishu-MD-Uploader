import unittest
from types import SimpleNamespace
from unittest.mock import patch
from src.document import add_editor

class ShareTests(unittest.TestCase):
    def test_adds_email_as_editor_without_notification(self):
        seen = []
        def create(request):
            seen.append(request)
            return SimpleNamespace(success=lambda: True)
        client = SimpleNamespace(drive=SimpleNamespace(v1=SimpleNamespace(permission_member=SimpleNamespace(create=create))))
        with patch('src.document.get_client', return_value=client):
            add_editor('doc', 'person@example.com')
        req = seen[0]
        self.assertEqual(req.token, 'doc')
        self.assertEqual(req.type, 'docx')
        self.assertFalse(req.need_notification)
        self.assertEqual((req.request_body.member_type, req.request_body.member_id, req.request_body.perm), ('email', 'person@example.com', 'edit'))

    def test_share_failure_is_reported(self):
        response = SimpleNamespace(success=lambda: False, code=123, msg='denied', error=None)
        client = SimpleNamespace(drive=SimpleNamespace(v1=SimpleNamespace(permission_member=SimpleNamespace(create=lambda request: response))))
        with patch('src.document.get_client', return_value=client):
            with self.assertRaisesRegex(Exception, '123'):
                add_editor('doc', 'person@example.com')

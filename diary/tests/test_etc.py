import os

from django.test import TestCase


class TestTemplate(TestCase):

    def test_render(self):
        """params = {}
        rendered = render(None, 'base_document.html', params)
        a = bytes(b'')
        self.assertEqual(rendered.content, a)
        parser = HTML(html=rendered.content.decode())
        elements = parser.find('a')
        for index in range(len(params)):
            element = elements[index]
            self.assertEqual(element.text, "title"+str(index))"""

class TestFileExistCheck(TestCase):
    test_path = os.getcwd() + '/private_diary'

    def test_diary_file(self):
        diary_files = ['admin/admin.py', 'admin/__init__.py',
                       'media/IPAexfont00401', 'media/印刷依頼書EXCEL', 'media/売上管理表PDF',
                       'media/年末調整PDF', 'media/提出一覧PDF',
                       'media/源泉税納期特例チェックPDF', 'media/確定申告PDF', 'media/請求書PDF',
                       'media/贈与税PDF', 'media/関与名簿PDF',
                       'media/documents.txt', 'media/filing_final_tax_template.pdf',
                       'middleware/middleware.py', 'migrations/__init__.py',
                       'static/css', 'static/debug_toolbar', 'static/img/favicon.ico',
                       'tekitou', 'templates', 'tests', 'views', 'apps.py', 'forms.py',
                       'forms_choices.py', 'models.py', 'urls.py']
        diary_path = self.test_path + '/diary/'
        for i in range(len(diary_files)):
            if os.path.exists(diary_path + diary_files[i]) is False:
                print("error!", diary_path + diary_files[i])
            self.assertTrue(os.path.exists(diary_path + diary_files[i]))

    def test_private_diary_file(self):
        private_diary_files = ['asgi.py', 'settings.py', 'urls.py', 'wsgi.py']
        private_diary_path = self.test_path + '/private_diary/'
        for i in range(len(private_diary_files)):
            if os.path.exists(private_diary_path + private_diary_files[i]) is False:
                print("error!", private_diary_path + private_diary_files[i])
            self.assertTrue(os.path.exists(private_diary_path + private_diary_files[i]))

    def test_other_file(self):
        private_diary_files = ['project/templatetags/tags.py', 'static/favicon.ico',
                               'templates/404.html', 'templates/500.html',
                               '.env', 'README.md', 'requirements.txt', ]
        private_diary_path = self.test_path + '/'
        for i in range(len(private_diary_files)):
            if os.path.exists(private_diary_path + private_diary_files[i]) is False:
                print("error!", private_diary_path + private_diary_files[i])
            self.assertTrue(os.path.exists(private_diary_path + private_diary_files[i]))

import unittest
from flask import Flask
from flask.testing import FlaskClient
from tinydb import TinyDB, Query
from wsgi import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        # Inicialize o banco de dados com alguns dados de exemplo
        self.db = TinyDB('db.json')
        self.db.truncate()  # Limpe o banco de dados antes de cada teste

        # Adicione dados de exemplo
        self.db.insert({
            "script_id": "script1",
            "activate": True,
            "errors": []
        })
        self.db.insert({
            "script_id": "script2",
            "activate": False,
            "errors": []
        })
        self.db.insert({
            "script_id": "script3",
            "activate": True,
            "errors": []
        })

    def tearDown(self):
        self.db.truncate()
          # Limpe o banco de dados após cada teste

    def test_get_scripts_list(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {
                "script_id": "script1",
                "activate": True,
                "errors": []
            },
            {
                "script_id": "script2",
                "activate": False,
                "errors": []
            },
            {
                "script_id": "script3",
                "activate": True,
                "errors": []
            }
        ])
        # Verifique se o conteúdo da resposta é o esperado

    def test_get_script(self):
        response = self.app.get('/get_script/script1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "activate": True,
            "errors": [],
            "script_id": "script1"
        })
     
        # Verifique se o conteúdo da resposta é o esperado

    def test_save_script(self):
        payload = {
            "script_id": "new_script_id",
            "activate": True,
            "errors": []
        }
        response = self.app.post('/save_script', json=payload)
        self.assertEqual(response.status_code, 200)
        # Verifique se o script foi salvo corretamente

    def test_delete_script(self):
        response = self.app.delete('/delete_script/script1')
        self.assertEqual(response.status_code, 204)
        # Verifique se o script foi excluído corretamente

    def test_activate_script(self):
        response = self.app.put('/activate_script/script2')
        self.assertEqual(response.status_code, 200)
        # Verifique se o script foi ativado corretamente

    def test_deactivate_script(self):
        response = self.app.put('/deactivate_script/script1')
        self.assertEqual(response.status_code, 200)
        # Verifique se o script foi desativado corretamente
    
    def test_get_errors(self):
        payload = {
            "error_list": {
                "datetime": "YYYY-MM-DDTHH:MM:SS.ssssss±hh:mm",
                "errors": [
                    "error_message1",
                    "error_message2",
                    "error_message3"
                ]
            }
        }
        response = self.app.put('/send_errors/script1', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "script_id": "script1",
            "activate": True,
            "errors": [payload]
        })



if __name__ == '__main__':
    unittest.main()
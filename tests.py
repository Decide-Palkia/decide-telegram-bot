import unittest
import auxiliar


class db_tests(unittest.TestCase):

    def test_1_db_connection(self):
        self.assertIsNotNone(auxiliar.get_db())

    def test_2_create_db(self):
        auxiliar.create_db()
        conn = auxiliar.get_db()
        cursor = conn.execute("SELECT * FROM USER;")
        conn.commit()
        users = cursor.fetchall()
        conn.close()
        self.assertTrue(len(users) == 0)

    def test_3_create_user(self):
        chat_id = 1010
        self.assertIsNone(auxiliar.check_user(chat_id))
        auxiliar.create_user(chat_id)
        self.assertIsNotNone(auxiliar.check_user(chat_id))

    def test_4_set_is_login(self):
        chat_id = 1010
        self.assertFalse(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))
        auxiliar.set_is_login(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))

    def test_5_set_is_not_login(self):
        chat_id = 1010
        self.assertTrue(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))
        auxiliar.set_is_not_login(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))

    def test_6_save_value(self):
        chat_id = 1010
        token = 9999
        self.assertIsNone(auxiliar.check_value(chat_id, "TOKEN", "USER"))
        auxiliar.save_value(chat_id, token, "TOKEN", "USER")
        self.assertTrue(auxiliar.check_value(chat_id, "TOKEN", "USER") == str(token))

    def test_7_delete_value(self):
        chat_id = 1010
        token = 9999
        self.assertTrue(auxiliar.check_value(chat_id, "TOKEN", "USER") == str(token))
        auxiliar.delete_value(chat_id, "TOKEN", "USER")
        self.assertIsNone(auxiliar.check_value(chat_id, "TOKEN", "USER"))


if __name__ == "__main__":
    unittest.main()
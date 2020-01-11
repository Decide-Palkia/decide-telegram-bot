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
        auxiliar.create_db()
        self.assertIsNone(auxiliar.check_user(chat_id))
        auxiliar.create_user(chat_id)
        self.assertIsNotNone(auxiliar.check_user(chat_id))

    def test_4_set_is_login(self):
        chat_id = 1010
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))
        auxiliar.set_is_login(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))

    def test_5_set_is_not_login(self):
        chat_id = 1010
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        auxiliar.set_is_login(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))
        auxiliar.set_is_not_login(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_LOGIN", "STATUS"))

    def test_6_save_value(self):
        chat_id = 1010
        token = 9999
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        self.assertIsNone(auxiliar.check_value(chat_id, "TOKEN", "USER"))
        auxiliar.save_value(chat_id, token, "TOKEN", "USER")
        self.assertTrue(auxiliar.check_value(chat_id, "TOKEN", "USER") == str(token))

    def test_7_delete_value(self):
        chat_id = 1010
        token = 9999
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        auxiliar.save_value(chat_id, token, "TOKEN", "USER")
        self.assertTrue(auxiliar.check_value(chat_id, "TOKEN", "USER") == str(token))
        auxiliar.delete_value(chat_id, "TOKEN", "USER")
        self.assertIsNone(auxiliar.check_value(chat_id, "TOKEN", "USER"))


    def test_8_create_voting(self):
        chat_id = 1515
        vot_id  = 2
        name = 'Voting Example Name'
        desc = 'Voting Example Desc'
        p = '76279431444911789137721520931211617431758124898619560218258158308275307031699'
        g = '55639360083148991254755253568493586800624709304278148849771074759843265239689'
        y = '17621527376193702731471166712896638306854884225650388978524218742192837961334'
        auxiliar.create_db()
        self.assertIsNone(auxiliar.check_test('VOTING','CHAT_ID',chat_id))
        auxiliar. create_voting(chat_id, vot_id , name , desc , p, g , y )
        self.assertIsNotNone(auxiliar.check_test('VOTING','CHAT_ID',chat_id))

    def test_9_create_option(self):
        vot_id  = 2
        number = 3
        text = 'Option 3 of example'
        auxiliar.create_db()
        self.assertIsNone(auxiliar.check_test('OPTION','VOTING_ID',vot_id))
        auxiliar.create_option(vot_id , number , text)
        self.assertIsNotNone(auxiliar.check_test('OPTION','VOTING_ID',vot_id))


    def test_10_set_is_voting(self):
        chat_id = 1515
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_VOTING", "STATUS"))
        auxiliar.set_is_voting(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_VOTING", "STATUS"))

    def test_11_set_is_not_voting(self):
        chat_id = 1515
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        auxiliar.set_is_voting(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_VOTING", "STATUS"))
        auxiliar.set_is_not_voting(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_VOTING", "STATUS"))

    def test_12_set_is_sending(self):
        chat_id = 1515
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_SENDING", "STATUS"))
        auxiliar.set_is_sending(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_SENDING", "STATUS"))

    def test_13_set_is_not_sending(self):
        chat_id = 1515
        auxiliar.create_db()
        auxiliar.create_user(chat_id)
        auxiliar.set_is_sending(chat_id)
        self.assertTrue(auxiliar.check_value(chat_id, "IS_SENDING", "STATUS"))
        auxiliar.set_is_not_sending(chat_id)
        self.assertFalse(auxiliar.check_value(chat_id, "IS_SENDING", "STATUS"))

    def test_14_send_data(self):
        user=1
        token='3b7fb31e5f773ec98e1765016e6b8849bd58a5d0'
        voting=1
        vote=[74992538839646296004726663185834817572060750836415531801474354089190162666204,62314593341405448893305169141281618287582639200558260911053918507862958690957]
        base_url='https://decide-palkia-django.herokuapp.com'
        res = auxiliar.send_data(user, token, voting, vote, base_url)
        res.status_code is 200
        self.assertTrue(res.status_code is 200)
            

if __name__ == "__main__":
    unittest.main()
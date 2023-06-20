import sqlite3


class Base:
    _table_name = ""

    def __init__(self):
        self._connect = sqlite3.connect("my_passwords.db", check_same_thread=False)
        self._cursor = self._connect.cursor()

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS passwords(
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              product TEXT,
                              username TEXT,
                              password TEXT)""")
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS products(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product TEXT UNIQUE)""")

    def insert(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def select(self, **kwargs):
        pass


class Password(Base):
    _table_name = "passwords"

    def select(self, columns: list, key_word: str, value) -> list[tuple]:
        """
        :param columns:list, id, product, username, password, *
        :param key_word:str, product, username,
        :param value:any,
        """

        return self._cursor.execute(f"""SELECT {','.join(columns)} FROM {self._table_name} WHERE {key_word} = ? """, (value,)).fetchall()

    def insert(self, product, username, password):
        self._cursor.execute(f"""INSERT INTO {self._table_name} (product, username, password) VALUES (?,?,?)""",
                             (product, username, password,))
        self._connect.commit()
        return "Done"

    def delete(self, product: str, by_user_name=False, user_value=None):
        """
        :param product:str
        :param by_user_name:bool, if True - selects all usernames for input product and deletes all with user_value
        :param user_value:None by default
        """
        print(by_user_name)
        if not by_user_name:
            self._cursor.execute(f"""DELETE FROM {self._table_name} WHERE product = ?""", (product,))
            self._connect.commit()

        else:
            selection = self.select(["id", "username", ], "product", product)
            print(selection)
            for id_, user in selection:
                if user == user_value:
                    print('got here')
                    self._cursor.execute(f"""DELETE FROM {self._table_name} WHERE id = ?""", (id_,))
                    self._connect.commit()
        return "Done"

    def update(self, product, user_name, password_old, password_new):
        selection = self.select(["id", "username", "password"], "product", product)
        print(selection)
        for id_, user, passwrd in selection:
            if password_old == passwrd and user == user_name:
                self._cursor.execute(f"""UPDATE {self._table_name} SET password = "{password_new}" WHERE id = {id_}""")
                self._connect.commit()
                return "Password had been updated successfully"
            else:
                return "Incorrect input"


class Product(Base):
    _table_name = "product"

    def select(self):
        return self._cursor.execute(f"""SELECT * FROM {self._table_name}""")

    def delete(self, product):
        self._cursor.execute(f"""DELETE FROM {self._table_name} WHERE product = ?""", (product, ))
        self._connect.commit()

    def insert(self, product):
        self._cursor.execute(f"""INSERT INTO {self._table_name} VALUES (?)""", (product, ))
        self._connect.commit()

    def update(self, old_product, new_product):
        self._cursor.execute(f"""UPDATE {self._table_name} SET product = {new_product} WHERE product = {old_product}""")
        self._connect.commit()


obj = Password()

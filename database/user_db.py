from .base_db import BaseDB

class UserDB(BaseDB):
    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        );
        """)
        self.conn.commit()

    def add_data(self, name, age):
        self.cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        self.conn.commit()

    def delete_data(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.cursor.execute("DELETE FROM step1 WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM step2 WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def update_data(self, user_id, name, age):
        self.cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, user_id))
        self.conn.commit()
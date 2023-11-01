from .base_db import BaseDB
from models.step4_analysis import Step4Analysis


class Step4DB(BaseDB):
    def __init__(self, db_name):
        super().__init__(db_name)
        analysis = Step4Analysis()
        self.boolean_columns = self.cat2col(analysis.sub_categories)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS step4 (
            id INTEGER PRIMARY KEY,
            step1_summary_id INTEGER,
            user_id INTEGER,
        """
        query += ",\n".join([f"{column} BOOLEAN" for column in self.boolean_columns])
        query += ")"
        self.cursor.execute(query)
        self.conn.commit()

    def add(self, step1_summary_id, user_id, **kwargs):
        query = """
        INSERT INTO step4 (step1_summary_id, user_id, """
        query += ", ".join(self.boolean_columns)
        query += ") VALUES (?, ?, "
        query += ", ".join(["?" for _ in self.boolean_columns])
        query += ")"
        values = [step1_summary_id, user_id] + [
            kwargs.get(column) for column in self.boolean_columns
        ]
        self.cursor.execute(query, values)
        self.conn.commit()

    def update(self, step1_summary_id, user_id, **kwargs):
        query = "UPDATE step4 SET "
        query += ", ".join([f"{column} = ?" for column in self.boolean_columns])
        query += " WHERE step1_summary_id = ? AND user_id = ?"
        values = [kwargs.get(column) for column in self.boolean_columns] + [
            step1_summary_id,
            user_id,
        ]
        self.cursor.execute(query, values)
        self.conn.commit()

    def entry_exists(self, step1_summary_id):
        # Check if the entry exists in the step4 table
        self.cursor.execute(
            "SELECT COUNT(*) FROM step4 WHERE step1_summary_id = ?", (step1_summary_id,)
        )
        count = self.cursor.fetchone()[0]
        return count > 0

    def delete(self, id):
        query = "DELETE FROM step4 WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def read(self, id):
        query = "SELECT * FROM step4 WHERE id = ?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def read_user_entries(self, user_id):
        query = "SELECT * FROM step4 WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def close(self):
        super().close()

    def get_summary_count(self, user_id):
        query = "SELECT COUNT(step1_summary_id) FROM step4 WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        count = self.cursor.fetchone()[0]
        return count

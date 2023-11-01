from .base_db import BaseDB

class Step1DB(BaseDB):
    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS step1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            life_stage TEXT,
            achievements TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)
        self.conn.commit()

    def add_data(self, life_stage, achievements, user_id):
        self.cursor.execute("INSERT INTO step1 (life_stage, achievements, user_id) VALUES (?, ?, ?)", (life_stage, achievements, user_id))
        self.conn.commit()

    def fetch_data(self, user_id):
        self.cursor.execute("SELECT * FROM step1 WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def fetch_summary_details_by_id(self, summary_id, user_id):
        self.cursor.execute("SELECT * FROM step1 WHERE id = ? and user_id = ?", (summary_id, user_id,))
        row = self.cursor.fetchone()
        if row:
            return {'life_stage': row[1], 'achievement': row[2]}
        return {}
    
    def update_data(self, id, life_stage, achievement, user_id):
        self.cursor.execute("UPDATE step1 SET life_stage = ?, achievements = ? WHERE id = ? and user_id = ?", (life_stage, achievement, id, user_id))
        self.conn.commit()

    def delete_data(self, id, user_id):
        self.cursor.execute("DELETE FROM step1 WHERE id = ? and user_id = ?", (id, user_id))
        self.conn.commit()
    
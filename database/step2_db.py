from .base_db import BaseDB

class Step2DB(BaseDB):
    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS step2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary_id INTEGER,
            q1 TEXT,
            q2 TEXT,
            q3 TEXT,
            user_id INTEGER,
            FOREIGN KEY (summary_id) REFERENCES step1(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)
        self.conn.commit()

    def add_data(self, summary_id, q1, q2, q3, user_id):
        self.cursor.execute("INSERT INTO step2 (summary_id, q1, q2, q3, user_id) VALUES (?, ?, ?, ?, ?)", (summary_id, q1, q2, q3, user_id))
        self.conn.commit()

    def update_data(self, summary_id, q1, q2, q3, user_id):
        self.cursor.execute("UPDATE step2 SET q1 = ?, q2 = ?, q3 = ? WHERE user_id = ? and summary_id = ?", (q1, q2, q3, user_id, summary_id))
        self.conn.commit()

    def fetch_data_by_summary_id(self, summary_id):
        self.cursor.execute("SELECT * FROM step2 WHERE summary_id = ?", (summary_id,))
        return self.cursor.fetchall()

    def fetch_data_by_user_id(self, user_id):
        self.cursor.execute("SELECT * FROM step2 WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()
    
    def fetch_step2_with_step1(self, user_id):
        self.cursor.execute("""
            SELECT s2.*, s1.life_stage, s1.achievements
            FROM step2 AS s2
            INNER JOIN step1 AS s1 ON s2.summary_id = s1.id
            WHERE s2.user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()
    
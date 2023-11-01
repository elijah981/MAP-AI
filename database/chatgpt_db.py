from datetime import datetime

from .base_db import BaseDB


class ChatGPTDB(BaseDB):
    def create_table(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS chatgpt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step1_summary_id INTEGER,
            current_step TEXT,
            prompt TEXT,
            response TEXT,
            usage TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        )
        self.conn.commit()

    def add_entry(self, step1_summary_id, current_step, prompt, response, usage):
        self.cursor.execute(
            "INSERT INTO chatgpt (step1_summary_id, current_step, prompt, response, usage, created_at) VALUES (?, ?, ?, ?, ?, datetime('now'))",
            (step1_summary_id, current_step, prompt, response, usage),
        )
        self.conn.commit()

    def read_entry(self, step1_summary_id, current_step):
        self.cursor.execute(
            "SELECT * FROM chatgpt WHERE step1_summary_id = ? AND current_step = ?",
            (
                step1_summary_id,
                current_step,
            ),
        )
        return self.cursor.fetchone()

    def update_entry(self, step1_summary_id, current_step, response, usage):
        self.cursor.execute(
            "UPDATE chatgpt SET response = ?, usage = ? WHERE step1_summary_id = ? AND current_step = ?",
            (
                response,
                usage,
                step1_summary_id,
                current_step,
            ),
        )
        self.conn.commit()

    def delete_entry(self, step1_summary_id, current_step):
        self.cursor.execute(
            "DELETE FROM chatgpt WHERE step1_summary_id = ? AND current_step = ?",
            (
                step1_summary_id,
                current_step,
            ),
        )
        self.conn.commit()

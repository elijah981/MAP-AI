from .base_db import BaseDB


class StepsSummary(BaseDB):
    def create_table(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS steps_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step_num INTEGER,
            user_id INTEGER,
            step_info TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
        )
        self.conn.commit()

    def add_data(self, step_num, user_id, step_info):
        self.cursor.execute(
            "INSERT INTO steps_summary (step_num, user_id, step_info) VALUES (?, ?, ?)",
            (step_num, user_id, step_info),
        )
        self.conn.commit()

    def update_data(self, step_num, user_id, step_info):
        self.cursor.execute(
            "UPDATE steps_summary SET step_info = ? WHERE user_id = ? and step_num = ?",
            (step_info, user_id, step_num),
        )
        self.conn.commit()

    def fetch_data(
        self,
        step_num,
        user_id,
    ):
        self.cursor.execute(
            "SELECT * FROM steps_summary WHERE user_id = ? and step_num = ?",
            (user_id, step_num),
        )
        return self.cursor.fetchone()

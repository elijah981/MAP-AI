import sqlite3


class BaseDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def cat2col(self, cat_dict):
        columns = []
        for cat, sub_cats in cat_dict.items():
            cat_word = cat.strip().lower().replace("/", "_").replace(" ", "_")
            for sub_cat in sub_cats:
                sub_cat_word = (
                    sub_cat.strip().lower().replace(" ", "_").replace(",", "")
                )
                column = f"{cat_word}_0_{sub_cat_word}"
                column = column.replace("&", "")
                columns.append(column)
        return columns

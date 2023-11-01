from .base_db import BaseDB


class Step3DB(BaseDB):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.boolean_columns = [
            "intangibles_emotions_feelings",
            "intangibles_ideas_theories_philosophy",
            "intangibles_knowledge_thoughts_understanding",
            "intangibles_logic",
            "intangibles_personal_goals",
            "intangibles_policies_information",
            "intangibles_principles_concepts_fundamentals",
            "intangibles_values_ethics_spiritual",
            "intangibles_others",
            "tangibles_animals",
            "tangibles_food",
            "tangibles_instruments_gadgets_tools",
            "tangibles_machinery_equipment",
            "tangibles_materials",
            "tangibles_motion_movement",
            "tangibles_phenomena",
            "tangibles_physical_manual_sensory",
            "tangibles_plants",
            "tangibles_shapes",
            "tangibles_sound",
            "tangibles_sports_athletics",
            "tangibles_structural_objects",
            "tangibles_vehicles",
            "tangibles_visual",
            "tangibles_other",
            "data_data_facts_resources",
            "data_details_particulars",
            "data_logistics_arrangements",
            "data_money_dollars",
            "data_numbers_finances",
            "data_words_language",
            "data_other",
            "mechanisms_art_personal_expertise",
            "mechanisms_controls_constraints",
            "mechanisms_graphics_pictorial",
            "mechanisms_models_examples",
            "mechanisms_organizational_processes_operations",
            "mechanisms_procedures",
            "mechanisms_roles_parts",
            "mechanisms_stories_literature",
            "mechanisms_strategies_tactics_angles",
            "mechanisms_systems_networks",
            "mechanisms_techniques_methods",
            "mechanisms_technology_science_computers",
            "mechanisms_time_space",
            "mechanisms_trade_craft",
            "mechanisms_other",
            "people_human_behavior",
            "people_people_groups",
            "people_people_individuals",
            "people_people_societies_cultures",
            "people_relationships",
            "people_other",
        ]

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS step3 (
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
        INSERT INTO step3 (step1_summary_id, user_id, """
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
        query = "UPDATE step3 SET "
        query += ", ".join([f"{column} = ?" for column in self.boolean_columns])
        query += " WHERE step1_summary_id = ? AND user_id = ?"
        values = [kwargs.get(column) for column in self.boolean_columns] + [
            step1_summary_id,
            user_id,
        ]
        self.cursor.execute(query, values)
        self.conn.commit()

    def entry_exists(self, step1_summary_id):
        # Check if the entry exists in the step3 table
        self.cursor.execute(
            "SELECT COUNT(*) FROM step3 WHERE step1_summary_id = ?", (step1_summary_id,)
        )
        count = self.cursor.fetchone()[0]
        return count > 0

    def delete(self, id):
        query = "DELETE FROM step3 WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def read(self, id):
        query = "SELECT * FROM step3 WHERE id = ?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def read_user_entries(self, user_id):
        query = "SELECT * FROM step3 WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def close(self):
        super().close()

    def get_summary_count(self, user_id):
        query = "SELECT COUNT(step1_summary_id) FROM step3 WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        count = self.cursor.fetchone()[0]
        return count

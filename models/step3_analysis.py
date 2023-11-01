import json

from models.base_analysis import BaseAnalysis


class Step3Analysis(BaseAnalysis):

    def __init__(self):
        super().__init__()
        # Specific categories and sub-categories for Step 3
        self.set_categories(['Intangibles', 'Tangibles', 'Data', 'Mechanisms', 'People'])
        self.set_sub_categories({
            'Intangibles': ['Emotions, feelings', 'Ideas, theories, philosophy', 'Knowledge, thoughts, understanding', 'Logic', 'Personal goals', 'Policies, information', 'Principles, concepts, fundamentals', 'Values, ethics, spiritual', 'Others'],
            'Tangibles': ['Animals', 'Food', 'Instruments, gadgets, tools', 'Machinery, equipment', 'Materials', 'Motion, movement', 'Phenomena', 'Physical, manual, sensory', 'Plants', 'Shapes', 'Sound', 'Sports, athletics', 'Structural objects', 'Vehicles', 'Visual', 'Other'],
            'Data': ['Data, facts, resources', 'Details, particulars', 'Logistics, arrangements', 'Money, dollars', 'Numbers, finances', 'Words, language', 'Other'],
            'Mechanisms': ['Art, personal expertise', 'Controls, constraints', 'Graphics, pictorial', 'Models, examples', 'Organizational processes, operations', 'Procedures', 'Roles, parts', 'Stories, literature', 'Strategies, tactics, angles', 'Systems, networks', 'Techniques, methods', 'Technology, science, computers', 'Time, space', 'Trade, craft', 'Other'],
            'People': ['Human behavior', 'People: groups', 'People: individuals', 'People: societies, cultures', 'Relationships', 'Other']
        })

    def generate_prompt(self, text):
        # Generate a specific prompt for Step 3 analysis
        sub_categories = self.get_sub_categories_string()

        json_example = {
                        "intangibles": {
                            "emotions, feelings": ["happy", "satisfied", "frustrating", "exhilarating"],
                            "personal goals": ["gift for mom", "painting handkerchief", "artistic challenge"],
                            "ideas, theories, philosophy": ["treasure something I made", "work in secrecy"],
                            "knowledge, thoughts, understanding": ["color mixing", "sketching"]
                        },
                        "tangibles": {
                            "instruments, gadgets, tools": ["fabric", "handkerchief", "paint brush", "palette", "bowl", "circular ring"],
                            "materials": ["colors", "water"],
                            "physical, manual, sensory": ["hands", "sketched borders", "traced borders"]
                        },
                        "data": {
                            "logistics, arrangements": ["activity preparation", "time management"],
                            "details, particulars": ["classmate's image", "desired shade", "broken lines"]
                        },
                        "mechanisms": {
                            "art, personal expertise": ["drawing classes", "fabric painting"],
                            "procedures": ["color mixing", "border tracing", "correcting mistakes"],
                            "techniques, methods": ["canvas tightening", "color matching", "painting outside the sketched borders"]
                        },
                        "people": {
                            "people: individuals": ["mom", "classmate"],
                            "relationships": ["mom's appreciation", "classmate's image loan"]
                        }
                        }

        json_string = json.dumps(json_example)

        prompt = f"""
                    Based on the given text, please identify the nouns or noun-phrases that pertain to the speaker. Additionally, categorize each tagged noun or noun-phrase under the appropriate subject matter sub-category:
                    [Text Start]
                    {text}
                    [Text End]

                    The Subject Matter categories and sub-categories are below:
                    {sub_categories}

                    Return the response without any comments or descriptions, just return the JSON once as described below:
                    {json_string}
                """
        return prompt

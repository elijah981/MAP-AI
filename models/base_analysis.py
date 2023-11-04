import json
import os
import re

import openai


class BaseAnalysis:
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_MAP_API_KEY")
        self.categories = []
        self.sub_categories = {}

    def set_categories(self, categories):
        self.categories = categories

    def set_sub_categories(self, sub_categories):
        self.sub_categories = sub_categories

    def get_sub_categories_string(self):
        sub_categories = ""
        for n, cat in enumerate(self.sub_categories.keys()):
            sub_categories += f"\n{n+1}. {cat}\n"
            for sub_cat in self.sub_categories[cat]:
                sub_categories += f"- {sub_cat}\n"

        return sub_categories

    def generate_prompt(self, text):
        raise NotImplementedError("Derived classes must implement this method")

    def get_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        self.usage = response.usage
        return json.loads(response.choices[0].message["content"])

    def tag_text(self, text, tag_name, categories):
        # Split text into words
        words = re.split("(\W+)", text)

        # Process each keyword
        for category_count, (category, subcategories) in enumerate(
            categories.items(), 1
        ):
            for subcategory_count, (subcategory, keywords) in enumerate(
                subcategories.items(), 1
            ):
                for keyword in sorted(keywords, key=len, reverse=True):
                    title = f"{keyword}<br>Category:{category}<br>Sub-category:{subcategory}"
                    tag = f"<span class={tag_name} data-toggle='tooltip' data-html='true' id={category_count} category='{category}' subcategory='{subcategory}' title='{title}'>{keyword}</span>"

                    # Replace words in the list
                    words = [tag if word == keyword else word for word in words]

        # Join words back into a string
        return "".join(words)

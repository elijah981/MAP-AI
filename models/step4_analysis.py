import json

from models.base_analysis import BaseAnalysis


class Step4Analysis(BaseAnalysis):
    def __init__(self):
        super().__init__()
        # Specific categories and sub-categories for Step 4
        self.set_categories(
            [
                "Learning/Investigating",
                "Evaluating/Deciding Tangibles",
                "Planning/Organizing",
                "Influencing/Informing",
                "Implementing/Developing",
            ]
        )
        self.set_sub_categories(
            {
                "Learning/Investigating": [
                    "Asking, probing, questioning",
                    "Experimenting, tinkering",
                    "Listening, discussing, expressing ",
                    "Memorizing, repeating",
                    "Observing, examining",
                    "Reading, studying",
                    "Surveying, gathering information ",
                    "Trying, doing",
                    "Other",
                ],
                "Evaluating/Deciding Tangibles": [
                    "Analyzing, dissecting",
                    "Assessing worth or value",
                    "Comparing to a standard",
                    "Empathizing, discerning",
                    "Figuring, calculating",
                    "Judging, weighing pros & cons",
                    "Other",
                ],
                "Planning/Organizing": [
                    "Anticipating, charting a course ",
                    "Arranging details, scheduling ",
                    "Categorizing, classifying",
                    "Conceiving ideas or concepts ",
                    "Fantasizing, theorizing",
                    "Fitting pieces together, integrating ",
                    "Laying things out",
                    "Picturing, visualizing",
                    "Practicing, getting ready",
                    "Providing definition",
                    "Setting goals",
                    "Strategizing, charting a course",
                    "Systematizing, proceduralizing",
                    "Other",
                ],
                "Influencing/Informing": [
                    "Checking, monitoring",
                    "Convincing, persuading",
                    "Coordinating activity of others",
                    "Counseling, consulting",
                    "Demonstrating, showing",
                    "Directing how it is done",
                    "Discussing, conferring",
                    "Coaching, tutoring",
                    "Facilitating, providing a way",
                    "Getting others involved",
                    "Instructing, guiding",
                    "Lecturing, explaining",
                    "Managing talent of others",
                    "Mediating, arbitrating",
                    "Motivating, inspiring",
                    "Negotiating, bargaining",
                    "Nurturing, encouraging",
                    "Overseeing indirectly",
                    "Subtly controlling",
                    "Performing, entertaining",
                    "Promoting, publicizing",
                    "Reporting, describing",
                    "Selling, confronting",
                    "Showing the way, leading",
                    "Suggesting, initiating",
                    "Teaching, training",
                    "Writing",
                    "Other ",
                ],
                "Implementing/Developing": [
                    "Assembling, fabricating",
                    "Adapting, modifying, improving ",
                    "Blending, synthesizing",
                    "Building relationships",
                    "Carrying out directions",
                    "Composing, formulating",
                    "Conceiving, originating",
                    "Constructing things",
                    "Designing",
                    "Documenting, logging data",
                    "Doing physically, manually",
                    "Fixing, repairing",
                    "Growing, nurturing, cultivating",
                    "Inventing, innovating, creating",
                    "Maintaining, keeping in condition ",
                    "Operating something, running it ",
                    "Participating in athletics",
                    "Processing",
                    "Refining, clarifying",
                    "Other",
                ],
            }
        )

    def generate_prompt(self, text):
        # Generate a specific prompt for Step 3 analysis
        sub_categories = self.get_sub_categories_string()

        json_example = {
            "Learning/Investigating": {
                "Asking, probing, questioning": ["requested"],
                "Observing, examining": ["seen", "sketched"],
                "Trying, doing": [
                    "attending",
                    "started",
                    "took",
                    "worked",
                    "arranged",
                    "mixed",
                    "colored",
                    "traced",
                    "made",
                    "correct",
                    "worked",
                    "gifted",
                    "liked",
                    "able",
                    "make",
                    "kept",
                    "going",
                ],
            },
            "Evaluating/Deciding Tangibles": {
                "Analyzing, dissecting": ["satisfied"],
                "Assessing worth or value": [
                    "knew",
                    "treasure",
                    "appreciation",
                    "happy",
                    "satisfied",
                ],
                "Judging, weighing pros & cons": ["satisfied"],
            },
            "Planning/Organizing": {
                "Arranging details, scheduling": ["arranged"],
                "Conceiving ideas or concepts": ["challenge", "image"],
                "Picturing, visualizing": ["imagine"],
                "Setting goals": ["challenge"],
                "Practicing, getting ready": ["tightened", "ready", "getting"],
            },
            "Influencing/Informing": {
                "Motivating, inspiring": ["happy", "kept", "going"],
                "Showing the way, leading": ["took"],
            },
            "Implementing/Developing": {
                "Assembling, fabricating": ["make", "made", "gifted"],
                "Adapting, modifying, improving": [
                    "started",
                    "correct",
                    "extra",
                    "recolor",
                ],
                "Designing": ["paint", "sketched"],
                "Doing physically, manually": [
                    "attended",
                    "paint",
                    "sketched",
                    "worked",
                    "mixed",
                    "colored",
                    "traced",
                    "made",
                    "correct",
                    "worked",
                ],
                "Fixing, repairing": ["correct"],
                "Inventing, innovating, creating": ["made", "gifted"],
            },
        }

        json_string = json.dumps(json_example)

        prompt = f"""
                    Based on the given text, please identify the verbs that pertain to the speaker. Additionally, categorize each tagged verb under the appropriate motivated abilities sub-category:
                    [Text Start]
                    {text}
                    [Text End]

                    The Motivated Abilities categories and sub-categories are below:
                    {sub_categories}

                    Return the response without any comments or descriptions, just return the JSON once as described below:
                    {json_string}
                    When a sub-category is empty do not return it in the response.
                """
        return prompt

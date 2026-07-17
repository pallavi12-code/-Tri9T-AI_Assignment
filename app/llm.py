"""
LLM integration module.

Handles communication with language models
for document structure extraction.
"""

import json
import os


class LLMService:


    def __init__(self):

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )


    def extract_structure(self, text):

        """
        Extract heading hierarchy
        from document text.

        Returns JSON:

        {
            "headings":[
                {
                    "title":"Introduction",
                    "level":1
                }
            ]
        }

        """


        prompt = f"""

You are a document structure parser.

Analyze the following document text.

Identify headings and their hierarchy.

Rules:

- Return only JSON.
- Level should be between 1 and 6.
- Do not include explanations.


Document:

{text}


Output format:

{{
 "headings":[
    {{
      "title":"Heading name",
      "level":1
    }}
 ]
}}

"""


        response = self.call_llm(prompt)


        return self.parse_json(
            response
        )



    def call_llm(self, prompt):

        """
        LLM API wrapper.

        Replace with OpenAI/Gemini call.
        """

        # temporary fallback
        # keeps system testable

        return json.dumps({

            "headings":[

                {
                    "title":"Introduction",
                    "level":1
                },

                {
                    "title":"Overview",
                    "level":2
                }

            ]

        })



    def parse_json(self, response):

        try:

            return json.loads(
                response
            )

        except Exception:

            return {
                "headings":[]
            }

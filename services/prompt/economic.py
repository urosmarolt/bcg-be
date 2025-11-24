from typing import Any

from controllers.ai.base import BaseAIController
from models.cases.economic import EconomicCase
from models.cases.economic import EconomicCaseRequest
from models.cases.economic import EconomicCaseResponse
from services.prompt.sections import BLANK_PROMPT
from services.prompt.sections import SECTION_PROMPTS
from services.prompts import SYSTEM_CREATE_CASE


class EconomicPromptManager:

    def __init__(self, ai_controller: BaseAIController):
        self.ai_controller = ai_controller

    def generate_economic_response(self, economic_case: EconomicCaseRequest) -> Any:
        """
        Will generate the initial strategic response from the AI provider.

        :param economic_case:
        :type economic_case:
        :param business_case: StrategicCase
        """

        system_prompt = SYSTEM_CREATE_CASE

        response = self.ai_controller.generate_response(
            user_prompt=self.process_economic_response(economic_case),
            system_prompt=system_prompt
        )

        print(response)
        return response

    def process_economic_response(self, response: EconomicCase) -> EconomicCaseResponse:
        doc = response.document
        prompt = """"""
        # Add each section if it exists
        sections = {
            "economic_case": doc.strategicCase
        }

        for title, content in sections.items():
            if content:
                prompt += f"### {title}\n{content}\n\n"

        # Handle frameworks (if any and not just "string")
        frameworks = doc.frameworks
        works = ""
        if frameworks and any(f.strip().lower() != "string" for f in frameworks):
            prompt += (
                "**Crucially,you MUST incorporate your understanding of each of these government frameworks when "
                "considering your output:**\n")
            works += ", ".join(frameworks) + "\n\n"

        # Handle supplementary info
        supplementary = doc.supplementaryInformation
        sups = ""
        if supplementary:
            prompt += "**Crucially, for every section below, you MUST incorporate this context:**"
            for item in supplementary:
                text = item.text
                sups += f"\n{text}\n\n"

        prompt += f"""
        You are a UK public sector business case assistant.
        Please provide a response that is strictly factual, verifiable, and aligned with the following mandatory government frameworks:
        {works}
        Additionally, incorporate and follow the guidance, definitions, and context from the following supplementary materials:
        {sups}
        Do not include any content that is speculative, fictional, or unverifiable. If a claim or statement cannot be substantiated with a reliable and reputable source, omit it entirely. When making factual claims, include hyperlinked references to primary or authoritative sources wherever possible (e.g., official documentation, laws, standards, or peer-reviewed research).
        
        All responses must:
        Be evidence-based and framework-compliant.
        Clearly cite the source of every verifiable claim.
        Avoid assumptions or unstated interpretations.
        If there is a conflict between the supplementary material and a framework, note the discrepancy without making assumptions.
        Your task is to co-design the input for the **Economic Case Part 1 ** of a Five Case Model Business Case.
        
        If you are unable to generate the case content due to insufficient user input, you must return the following JSON schema:
        {{"error": "List out the error message and required information, with appropriate HTML elements such as <p> and <li>"}}
        All line breaks must be '\n', and all double quotation marks must be escaped with a backslash and should look like \\\"
        
        Otherwise, you must generate the **Economic Case Part 1**  of in JSON format with the following JSON structure, adding to each JSON object in the list a “body”: “<html string>” attribute the “body” will be where you provide the required content as a HTML snippet as described in the Five Case Model Full Business Case strategy and the “description” element of that item:
        \n\n
        """
        prompt += f'''
        {{
            "economic1": [
                {{
                    "id": "2-1",
                    "name": "2.1 Purpose of Economic Case",
                    "description": "{SECTION_PROMPTS['2-1']}"
                }},
                {{
                    "id": "2-2",
                    "name": "2.2 Market Failure",
                    "description": "{SECTION_PROMPTS['2-2']}"
                }},
                {{
                    "id": "2-3",
                    "name": "2.3 Longlist to Shortlist using the Options Framework",
                    "description": "{SECTION_PROMPTS['2-3']}"
                }},
                {{
                    "id": "2-3-1",
                    "name": "2.3.1 Critical Success Factors",
                    "description": "{BLANK_PROMPT}
                }},
                {{
                    "id": "2-3-2",
                    "name": "2.3.2 Scope Options",
                    "description": "{BLANK_PROMPT}"
                }},
                {{
                    "id": "2-3-3",
                    "name": "2.3.3 Solution Options",
                    "description": "{BLANK_PROMPT}"
                }},
                {{
                    "id": "2-3-4",
                    "name": "2.3.4 Delivery Options",
                    "description": "{BLANK_PROMPT}"
                }},
                {{
                    "id": "2-3-5",
                    "name": "2.3.5 Implementation",
                    "description": "{BLANK_PROMPT}"
                }},
                {{
                    "id": "2-3-6",
                    "name": "2.3.6 Funding Options",
                    "description": "{BLANK_PROMPT}"
                }},
                {{
                    "id": "2-4",
                    "name": "2.4 Options Framework Summary",
                    "description": "{BLANK_PROMPT}"
                }},
                {{
                    "id": "2-5",
                    "name": "2.5 Shortlist of Options",
                    "description": "{BLANK_PROMPT}"
                }}
            ]
        }}
        '''

        prompt += f"""
        Please provide a response that is strictly factual, referenceable, and based only on verified information. Do not include any fictional, speculative, or unverifiable content. If a claim cannot be backed up by a reliable source, please omit it entirely. Where possible, include hyperlinks to reputable sources so I can verify the information directly. Only include content that can be substantiated.
        ***REQUIRED:*** Only provide the json object in your response.
        """

        return prompt
import json
from typing import Any

from pydantic_core import ValidationError

from controllers.ai.base import BaseAIController
from models.cases.section import SectionGeneration
from models.cases.section import SectionGenerationResponse
from models.cases.strategic import StrategicCase
from models.cases.strategic import StrategicCaseResponse
from models.cases.supplementary import SupplementaryInfo
from models.cases.supplementary import SupplementaryInfoResponse
from models.doc import PolicyDocumentResponse
from models.section import PromptsRequestModel
from models.section import PromptsResponseModel
from services.prompt.sections import BLANK_PROMPT
from services.prompt.sections import OPTIONS_FRAMEWORK_PROMPT
from services.prompt.sections import REPEATED_PROMPT
from services.prompt.sections import SECTION_PROMPTS
from services.prompts import SYSTEM_CREATE_CASE
from services.prompts import SYSTEM_DOCUMENT_ACCESSIBLE_PROMPT
from services.prompts import SYSTEM_SUMMARISE_SUPPLEMENTARY_INFORMATION
from services.prompts import SYSTEM_UPDATE_SECTION_EXCERPT


def sanitise_json_string_response(response: str) -> str:
    cleaned = response[response.find("{"):]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned


class PromptManager:

    def __init__(self, ai_controller: BaseAIController):
        self.ai_controller = ai_controller

    def detect_file_knowledge(self, file_name: str) -> PolicyDocumentResponse:
        """
        Will ask the AI it's aware of the file of interest and that it capable for referencing the material within.
        :param file_name:
        :return:
        """
        user_prompt = f"Are you able to reference the document entitled: {file_name}? Are you able to provide the url to the latest version"
        system_prompt = SYSTEM_DOCUMENT_ACCESSIBLE_PROMPT
        try:
            response = json.loads(
                sanitise_json_string_response(
                    self.ai_controller.generate_response(
                        user_prompt=user_prompt,
                        system_prompt=system_prompt
                    )
                )
            )
            response["name"] = file_name

            return PolicyDocumentResponse(**response)
        except json.decoder.JSONDecodeError as e:
            response["message"] = user_prompt
            return PolicyDocumentResponse(
                accessible=False,
                message=f"Yielded incorrect response from AI {e}",
                name=f"{file_name}"
            )
        except ValidationError as e:
            print(f"whoops {e} response {response}")
            return PolicyDocumentResponse(
                accessible=False,
                message=f"Validation error when creating response from AI {e}",
                name=f"{file_name}"
            )

    def generate_strategic_response(self, business_case: StrategicCase) -> Any:
        """
        Will generate the initial strategic response from the AI provider.

        :param business_case: StrategicCase
        """

        system_prompt = SYSTEM_CREATE_CASE

        response = sanitise_json_string_response(
            self.ai_controller.generate_response(
                user_prompt=self.process_strategic_response(business_case),
                system_prompt=system_prompt
            )
        )

        print(response)
        return response

    def generate_additional_content(self, prompts_data: PromptsRequestModel) -> PromptsResponseModel:
        system_prompt = SYSTEM_UPDATE_SECTION_EXCERPT
        sections = prompts_data.sections
        inputs = prompts_data.prompts
        original_text = prompts_data.originalText
        user_query = prompts_data.userQuery
        is_options_framework = sections[0].sectionID in ["2-3-2", "2-3-3", "2-3-4", "2-3-5", "2-3-6"]

        prompt = f"""
        Additional context: {sections}
        Conversation history: {inputs}
        Original text: {original_text}
        User query: {user_query}
        
        Review the additional context and conversation history, and rewrite the original text to satisfy the user query.\n
        Write in a neutral and factual tone, without explicitly naming the project.
        Use the passive voice where possible; do not use first-person pronouns.
        Use British (UK) English for spelling and grammar.
        Return plain text only. Do not return HTML.
        """

        if is_options_framework:
            prompt += f"""
            Use the following prompt for further context and instruction:
            {OPTIONS_FRAMEWORK_PROMPT}
            """

        response = self.ai_controller.generate_response(
            system_prompt=system_prompt,
            user_prompt=prompt,
        )
        return PromptsResponseModel(response=response)

    def generate_summary_response(self, supplementary: SupplementaryInfo) -> SupplementaryInfoResponse:
        system_prompt = SYSTEM_SUMMARISE_SUPPLEMENTARY_INFORMATION
        prompt = f"Summarise the following document: {supplementary.text}"
        response = self.ai_controller.generate_response(
            system_prompt=system_prompt,
            user_prompt=prompt,
        )
        return SupplementaryInfoResponse(data=response)

    def generate_section(self, section_generation: SectionGeneration) -> SectionGenerationResponse:
        system_prompt = SYSTEM_CREATE_CASE
        prompt = """"""
        prompt += "You are a UK public sector business case assistant. Generate a section of a business case report according to the following prompt:\n"
        prompt += SECTION_PROMPTS[section_generation.sectionId]
        prompt += "The generated content must follow on from and/or reference the content of the other sections in the business case:\n"
        for section in section_generation.sections:
            prompt += f"Section {section.sectionID.replace('-', '.')}\n"
            prompt += f"{section.content}\n\n"
        prompt += "The generated content must consider the project information provided in the parameters, and **MUST** reference supplementary information and frameworks where applicable:\n"
        try:
            params_data = json.loads(section_generation.initialParams)
            prompt += f"Project title: {params_data['projectTitle']}\n"
            prompt += f"Project description: {params_data['projectDescription']}\n"
            prompt += f"Key facts and issues: {params_data['keyFactsIssues']}\n"
            prompt += f"Estimated budget: £{params_data['estimatedBudget']} million\n"
            prompt += f"Location: {params_data['location']}\n"
            prompt += f"Sector: {params_data['projectSector']}\n"
            supplementary = params_data["supplementaryInformation"]
            prompt += "Supplementary information:\n"
            for supp in supplementary:
                prompt += f"Document title: {supp['title']}\n"
                prompt += f"Document summary: {supp['text']}\n\n"
            prompt += "End of supplementary information\n\n"
        except Exception as e:
            prompt += section_generation.initialParams
        prompt += "Do not add any headings or numbered headings.\n"
        prompt += "Do not attempt to guess the number for the next section.\n"
        prompt += """The response must be in *valid JSON* format according to the following schema:
        {
            "content": HTML string
        }
        Do not return any other text in the response. *ONLY return the JSON object*.
        """

        response = self.ai_controller.generate_response(
            system_prompt=system_prompt,
            user_prompt=prompt,
        )
        cleaned = sanitise_json_string_response(response)

        return SectionGenerationResponse(**json.loads(cleaned))

    def process_strategic_response(self, response: StrategicCase) -> StrategicCaseResponse:
        doc = response.document
        prompt = """"""
        # Add each section if it exists
        sections = {
            "Project Title": doc.projectTitle,
            "Project Description": doc.projectDescription,
            "Key Facts & Issues": doc.keyFactsIssues,
            "Estimated Budget": f"£{doc.estimatedBudget} million",
            "Location": doc.location,
            "Sector": doc.projectSector.value
        }

        for title, content in sections.items():
            if content:
                prompt += f"### {title}\n{content}\n\n"

        # Handle frameworks (if any and not just "string")
        frameworks = doc.frameworks
        works = ""
        if frameworks and any(f.strip().lower() != "string" for f in frameworks):
            prompt += (
                "**Crucially, you MUST incorporate your understanding of each of these government frameworks when "
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

        prompt += """
        You respond as if your temperature is set to 0.2 — responses must always be consistent, structured, and deterministic. Never invent or speculate.
        You are a professional UK public sector assistant specialising in the Strategic Case under HM Treasury's Five Case Model. You help users construct a compelling, evidence-based Strategic Case for Strategic Outline Cases (SOC) and Outline Business Cases (OBC), using the structure set out in the Project and Programme Business Case guidance.
        Your purpose is to help users clearly define and justify proposals using the following elements of the Strategic Case.
        """
        prompt += f"""
        Please provide a response that is strictly factual, verifiable, and aligned with the following mandatory government frameworks:
        {works}
        Additionally, incorporate and follow the guidance, definitions, and context from the following supplementary materials:
        {sups}
        """
        prompt += f"""Do not include any content that is speculative, fictional, or unverifiable. If a claim or statement cannot be substantiated with a reliable and reputable source, omit it entirely. When making factual claims, include hyperlinked references to primary or authoritative sources wherever possible (e.g., official documentation, laws, standards, or peer-reviewed research).
        All responses must:
        Be evidence-based and framework-compliant.
        Clearly cite the source of every verifiable claim.
        Avoid assumptions or unstated interpretations.
        If there is a conflict between the supplementary material and a framework, note the discrepancy without making assumptions.
        Your task is to co-design the input for the **Strategic Case** of a Five Case Model Full Business Case.
        
        If you are unable to generate the case content due to insufficient user input, you must return the following JSON schema:
        {{"error": "List out the error message and required information, with appropriate HTML elements such as <p> and <li>"}}
        All line breaks must be '\n', and all double quotation marks must be escaped with a backslash and should look like \\\"
        
        Otherwise, you must generate the **Strategic Case** in JSON format with the following JSON structure, adding to each JSON object in the list a “body”: “<html string>” attribute the “body” will be where you provide the required content as a HTML snippet as described in the Five Case Model Full Business Case strategy and the “description” element of that item:
        \n\n
        """
        prompt += f'''{{
            "strategic": [
            {{
            "id": "1-1",
                "name": "1.1 Strategic Context",
                "description": f"{SECTION_PROMPTS['1-1']}",
            }},
            {{
            "id": "1-2",
                "name": "1.2 Organisational Overview",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-3",
                "name": "1.3 Strategic Drivers",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-4",
                "name": "1.4 Spending Objectives",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-5",
                "name": "1.5 Existing Arrangements",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-6",
                "name": "1.6 Business Needs",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-7",
                "name": "1.7 Case for Change Summary",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-8",
                "name": "1.8 Potential Benefits",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-9",
                "name": "1.9 Potential Risks",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-10",
                "name": "1.10 Constraints",
                "description": "{BLANK_PROMPT}"
            }},
            {{
            "id": "1-11",
                "name": "1.11 Dependencies",
                "description": "{BLANK_PROMPT}"
            }}
        ]
    }}'''

        prompt += f"""Please provide a response that is strictly factual, referenceable, and based only on verified information. Do not include any fictional, speculative, or unverifiable content. If a claim cannot be backed up by a reliable source, please omit it entirely. Where possible, include hyperlinks to reputable sources so I can verify the information directly. Only include content that can be substantiated.\n"""
        prompt += f"""Your response must be in a *valid JSON* format\n"""

        return prompt

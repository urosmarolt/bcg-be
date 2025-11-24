"""
FastAPI application exposing AI endpoints backed by AWS Bedrock.

Routes include helpers for generating strategic/economic case content, policy
document discovery, section updates, and a generic Bedrock invocation endpoint.
"""

import json

import boto3
import requests
from decouple import config as envconfig
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.cases.economic import EconomicCaseRequest
from models.cases.economic import EconomicCaseResponse
from models.cases.section import SectionGeneration
from models.cases.strategic import StrategicCaseRequest
from models.cases.strategic import StrategicCaseResponse
from models.cases.strategic import SupplementaryInfo
from models.doc import PolicyDocsRequest
from models.doc import PolicyDocsResponse
from models.section import PromptsRequestModel
from services.ai import bedrock_economic_prompt_service
from services.ai import bedrock_prompt_service

# FastAPI application for AWS Bedrock integration
#
# This API provides endpoints to interact with AWS Bedrock foundation models.
#
# Key endpoints:
# - POST /api/bedrock: Invoke AWS Bedrock models with system and user prompts
#   Example request:
#   {
#     "model_id": "anthropic.claude-v2",
#     "system_prompt": "You are a helpful AI assistant.",
#     "user_prompt": "What are the key features of AWS Bedrock?"
#   }
#
# Note: Ensure AWS credentials are properly configured with access to Bedrock.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

bedrock_key = envconfig('BEDROCK_ACCESS_KEY')
bedrock_secret = envconfig('BEDROCK_SECRET_ACCESS_KEY')

iam = boto3.client('iam')
# Initialize Bedrock client with a region where the service is available
# TODO: change region for pilot
bedrock = boto3.client('bedrock-runtime', region_name='eu-west-2')


@app.get("/")
async def root():
    """Simple root endpoint for service liveness.

    Returns a small JSON payload as a quick liveness indicator.

    Returns:
        dict: Greeting message.
    """
    # Check if user exists (placeholder)
    # If user doesn't exist create user in AWS and give bedrock access (placeholder)
    return {"message": "Hello World"}


@app.post("/user/auth/cognito/callback")
async def cognito_auth_callback(request: Request):
    """Handle AWS Cognito auth callback.

    Note: Implementation is currently a placeholder and will be extended to
    validate the callback payload and establish a user session.

    Args:
        request: FastAPI request containing Cognito callback payload.

    Returns:
        None: Placeholder response (to be replaced with auth handling).

    Raises:
        HTTPException: On processing errors.
    """
    try:

        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@app.post("/api/ai/policy-docs")
async def policy_docs(request: PolicyDocsRequest):
    """Determine whether referenced policy documents are known/accessible.

    For each provided document title, asks the AI if it can reference and
    provide a URL to the latest version.

    Args:
        request: Payload containing a list of document titles.

    Returns:
        PolicyDocsResponse: Per-document accessibility info.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    policy_docs_response = []
    for doc in request.documents:
        policy_docs_response.append(service.detect_file_knowledge(doc.title))
    return PolicyDocsResponse(message=policy_docs_response)


@app.post("/api/ai/create/strategic-case")
async def strategic_case(request: StrategicCaseRequest):
    """Generate the Strategic Case content via Bedrock.

    Args:
        request: Structured inputs for strategic case generation.

    Returns:
        StrategicCaseResponse: AI-generated content wrapped in response model.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_strategic_response(request)
    return StrategicCaseResponse(**dict(data=f"{response}"))


@app.post("/api/ai/create/economic-case")
async def economic_case(request: EconomicCaseRequest):
    """Generate the Economic Case content via Bedrock.

    Args:
        request: Structured inputs for economic case generation.

    Returns:
        EconomicCaseResponse: AI-generated content wrapped in response model.
    """
    service = bedrock_economic_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_economic_response(request)
    return EconomicCaseResponse(**dict(data=f"{response}"))


@app.post("/api/ai/create/section")
async def generate_section(request: SectionGeneration):
    """Generate a single section based on the provided configuration.

    Args:
        request: Section generation inputs (section id, context, etc.).

    Returns:
        SectionGenerationResponse: AI-created section content.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_section(request)
    return response


@app.post("/api/ai/update/section/additional")
async def section_additional(request: PromptsRequestModel):
    """Update an existing section with additional user-provided guidance.

    Args:
        request: Contains prior section text, prompts, and user query.

    Returns:
        PromptsResponseModel: Updated section text.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_additional_content(request)
    return response


@app.post("/api/ai/summarise")
async def summarise_info(request: SupplementaryInfo):
    """Summarise supplementary information using Bedrock.

    Args:
        request: Supplementary info payload.

    Returns:
        SupplementaryInfoResponse: Summary of the provided information.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_summary_response(request)
    return response


@app.post("/api/ai/update/section/additional")
async def section_additional(request: PromptsRequestModel):
    """Update an existing section with additional user-provided guidance.

    Duplicate of the earlier route kept for backward compatibility.

    Args:
        request: Contains prior section text, prompts, and user query.

    Returns:
        PromptsResponseModel: Updated section text.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_additional_content(request)
    return response


@app.post("/api/ai/summarise")
async def summarise_info(request: SupplementaryInfo):
    """Summarise supplementary information using Bedrock.

    Duplicate of the earlier route kept for backward compatibility.

    Args:
        request: Supplementary info payload.

    Returns:
        SupplementaryInfoResponse: Summary of the provided information.
    """
    service = bedrock_prompt_service(aws_access_key_id=bedrock_key, aws_secret_access_key=bedrock_secret)
    response = service.generate_summary_response(request)
    return response


@app.post("/api/ai/mocked/create/strategic-case")
async def mocked_strategic_case(request: StrategicCaseRequest):
    """Return a mocked Strategic Case response for UI testing.

    Args:
        request: StrategicCaseRequest (ignored in mocked path).

    Returns:
        StrategicCaseResponse: Pre-baked response for demos/tests.
    """
    mocked = {
        "status": "success",
        "message": None,
        "data": None,
        "date": "2025-07-31T08:05:10.955555Z",
        "business_case": "{\n    \"strategic\": [\n        {\n            \"id\": \"1-1\",\n            \"name\": \"1.1 Strategic Context\",\n            \"description\": \"Project Title apples, Project Budget , Project Sector Environment & Sustainability, Geopgraphic Location:, Project key information: - Description: we're going to plant more trees  and - Key facts: forests\",\n            \"body\": \"<p>This project aims to increase tree planting and forest coverage within the Environment & Sustainability sector. The key details are:</p><ul><li>Project Title: Apples</li><li>Project Sector: Environment & Sustainability</li><li>Project Description: We're going to plant more trees</li><li>Key Facts: Forests</li></ul>\"\n        },\n        {\n            \"id\": \"1-2\",\n            \"name\": \"1.2 Organisational Overview\",\n            \"description\": \"Delivery organisation(s) and their roles\",\n            \"body\": \"<p>Information on the specific organisations involved in delivering this tree planting initiative, and their respective roles and responsibilities, is not provided in the prompt. As this is a key component of the Strategic Case, factual details from relevant stakeholders would need to be gathered and included here.</p>\"\n        },\n        {\n            \"id\": \"1-3\",\n            \"name\": \"1.3 Strategic Drivers\",\n            \"description\": \"National/regional/local policy or legislative alignment\",\n            \"body\": \"<p>Tree planting and increasing forest coverage aligns with several national and international environmental policies and commitments, such as:</p><ul><li>The UK government's <a href='https://www.gov.uk/government/publications/25-year-environment-plan'>25 Year Environment Plan</a> which aims to increase woodland in England</li><li>The <a href='https://www.un.org/sustainabledevelopment/biodiversity/'>United Nations Sustainable Development Goals</a> related to life on land and climate action</li><li>The UK's <a href='https://www.gov.uk/government/publications/net-zero-strategy'>Net Zero Strategy</a> which recognises the importance of tree planting in carbon sequestration</li></ul>\"\n        },\n        {\n            \"id\": \"1-4\",\n            \"name\": \"1.4 Spending Objectives\",\n            \"description\": \"SMART objectives, categorised (Economy, Efficiency, Effectiveness, Statutory compliance, Re-procurement)\",\n            \"body\": \"<p>Specific SMART (Specific, Measurable, Achievable, Relevant, Time-bound) objectives for this tree planting project have not been provided. However, potential objectives aligned with government guidance could include measures related to environmental effectiveness (e.g. increasing hectares of woodland planted), efficiency (e.g. cost per tree planted), and statutory compliance (e.g. meeting regional/national tree planting targets).</p>\"\n        },\n        {\n            \"id\": \"1-5\",\n            \"name\": \"1.5 Existing Arrangements\",\n            \"description\": \"Current service model, costs, delivery, and limitations\",\n            \"body\": \"<p>Details on the existing service model, costs, delivery mechanisms and limitations related to tree planting and forest management in the specified geographic area have not been provided. This factual evidence would need to be gathered from relevant stakeholders and sources to complete this section and establish the basis for the business needs.</p>\"\n        },\n        {\n            \"id\": \"1-6\",\n            \"name\": \"1.6 Business Needs\",\n            \"description\": \"Split into: <br><br>- `problems_with_status_quo`<br><br> - `opportunities_from_investment`\",\n            \"body\": \"<p>The specific business needs driving this investment have not been detailed, but based on the strategic context provided, they could potentially include:</p><h4>Problems with Status Quo</h4><ul><li>Insufficient tree/forest coverage leading to negative environmental impacts</li><li>Failure to meet statutory tree planting obligations or targets</li></ul><h4>Opportunities from Investment</h4><ul><li>Environmental benefits from increased carbon sequestration and improved biodiversity</li><li>Economic opportunities related to forestry, recreation and other ecosystem services</li></ul>\"\n        },\n        {\n            \"id\": \"1-6-1\",\n            \"name\": \"Case for Change Summary\",\n            \"description\": \"Table with three columns:<br><br> - existing_arrangement<br><br> - spending_objective (from section 4)<br><br> - resulting_business_need\",\n            \"body\": \"<p>A summary table mapping the existing arrangements, spending objectives, and resulting business needs cannot be fully populated based on the limited information provided in the prompt. However, an example row could be:</p><table><tr><th>Existing Arrangement</th><th>Spending Objective</th><th>Resulting Business Need</th></tr><tr><td>Low tree planting rates</td><td>Increase hectares of new woodland created annually by 20% by 2025</td><td>Expand tree planting and forest coverage programs</td></tr></table>\"\n        },\n        {\n            \"id\": \"1-7\",\n            \"name\": \"1.7 Potential Benefits\",\n            \"description\": \"High-level list (linked to spending objectives\",\n            \"body\": \"<p>Potential benefits of increasing tree planting and forest coverage could include:</p><ul><li>Environmental benefits like improved air quality, carbon sequestration, soil conservation and increased biodiversity</li><li>Economic benefits from forestry, timber and recreation industries</li><li>Health and social benefits from improved green spaces</li><li>Meeting statutory environmental obligations and targets</li></ul><p>These potential benefits would need to be clearly linked to the defined spending objectives.</p>\"\n        },\n        {\n            \"id\": \"1-8\",\n            \"name\": \"1.8 Potential Risks\",\n            \"description\": \"Known delivery or strategic risks\",\n            \"body\": \"<p>Without additional context, some potential risks associated with this tree planting project could include:</p><ul><li>Availability and suitability of land for planting new forests</li><li>Environmental risks like drought, pests or disease impacting growth of new trees</li><li>Capacity and capability constraints related to nursery production and skilled labour</li><li>Financing and ongoing operational/maintenance costs</li><li>Community acceptance or objections to land use change</li></ul><p>A full risk assessment would be required to identify and analyse all relevant risks.</p>\"\n        },\n        {\n            \"id\": \"1-9\",\n            \"name\": \"1.9 Constraints\",\n            \"description\": \"Legal, financial or delivery constraints\",\n            \"body\": \"<p>Possible key constraints for this type of tree planting and forest expansion project include:</p><ul><li>Legal constraints like land ownership, protected areas, and environmental regulations</li><li>Financial constraints in terms of available budgets and funding mechanisms</li><li>Logistical and delivery constraints such as availability of suitable nursery stock</li><li>Technical constraints related to site conditions, terrain and accessibility</li></ul><p>More details from stakeholders would allow constraints to be identified with greater specificity.</p>\"\n        },\n        {\n            \"id\": \"1-10\",\n            \"name\": \"1.10 Dependencies\",\n            \"description\": \"External factors the case depends on\",\n            \"body\": \"<p>Some potential external dependencies for a tree planting initiative include:</p><ul><li>Government policies, regulations and funding priorities related to forestry and the environment</li><li>Nursery production capacity and supplier availability of suitable tree seedlings/saplings</li><li>Land use planning policies, approvals and vesting of planting sites</li><li>Climate conditions and weather patterns favorable for tree growth</li><li>Community engagement and acceptance of tree planting plans</li></ul>\"\n        }\n    ]\n}"
    }

    return StrategicCaseResponse(**mocked)


@app.post("/api/bedrock")
async def invoke_bedrock(request: Request):
    """Invoke AWS Bedrock with basic system and user prompt inputs.

    Request body JSON fields:
      - model_id (str): Optional Bedrock model ID; defaults to Claude if omitted.
      - system_prompt (str): Optional system context.
      - user_prompt (str): Required user prompt.

    Returns:
        dict: JSON payload with completion text and raw model response.

    Raises:
        HTTPException: If required inputs are missing or invocation fails.
    """
    try:
        # Parse the request body
        data = await request.json()

        # Extract required parameters
        model_id = data.get('model_id', 'anthropic.claude-v2')  # Default to Claude v2 if not specified
        system_prompt = data.get('system_prompt', '')
        user_prompt = data.get('user_prompt', '')

        if not user_prompt:
            raise HTTPException(status_code=400, detail="Missing required parameter: user_prompt")

        # Prepare the prompt based on the model
        if 'anthropic' in model_id:
            # Anthropic models use a specific format
            # For Claude, system instructions should be included at the beginning of the Human message
            if system_prompt:
                prompt = f"\n\nHuman: {system_prompt}\n\n{user_prompt}\n\nAssistant:"
            else:
                prompt = f"\n\nHuman: {user_prompt}\n\nAssistant:"

            # Prepare the request body for Anthropic models via Bedrock
            request_body = {
                "prompt": prompt,
                "max_tokens_to_sample": 2000,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop_sequences": ["\n\nHuman:"]
            }
        else:
            # Generic format for other models
            request_body = {
                "system_prompt": system_prompt,
                "prompt": user_prompt,
                "max_tokens": 2000,
                "temperature": 0.7,
                "top_p": 0.9,
            }

        # Invoke the Bedrock model
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        # Parse the response
        response_body = json.loads(response['body'].read())

        # Extract the completion text based on the model type
        if 'anthropic' in model_id:
            completion_text = response_body.get('completion', '')
        else:
            # For other models, try to extract the generated text
            # This may need to be adjusted based on the specific model's response format
            completion_text = response_body.get(
                'generated_text',
                response_body.get(
                    'text',
                    response_body.get('output', str(response_body))
                )
            )

        return {
            "status": "success",
            "model": model_id,
            "response": {
                "completion": completion_text,
                "raw_response": response_body
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bedrock invocation failed: {str(e)}")


@app.get("/health-check")
def check_url(url: str = Query(..., description="The URL to check")):
    """Health-check an external URL.

    Issues a HEAD request to the provided URL to verify reachability.

    Args:
        url: The URL to check.

    Returns:
        JSONResponse: Status code if reachable, or 404 if not.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/129.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    })

    try:
        response = session.head(url, allow_redirects=True, timeout=5)
        return JSONResponse(content={"status": response.status_code})
    except Exception:
        return JSONResponse(content={"status": 404})

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from models.github_app_request import GitHubAppRequestHeaders, GitHubAppRequest
from services.agent_services import process_agent_request
from common.dependencies import validate_headers

router = APIRouter(prefix="/agents")

@router.post("/blackbeard")
async def agent(
    payload: GitHubAppRequest,
    headers: GitHubAppRequestHeaders = Depends(validate_headers),
):
    """
    Handles the agent endpoint for processing agent requests.

    Args:
        payload (GitHubAppRequest): The request payload containing the necessary data for processing.
        headers (GitHubAppRequestHeaders, optional): The validated headers for the request,
        automatically provided by the `validate_headers` dependency.

    Returns:
        StreamingResponse: A streaming response with the processed agent request data 
        in JSON format.
    """
    response_stream = process_agent_request(headers, payload)
    return StreamingResponse(response_stream, media_type="application/json")

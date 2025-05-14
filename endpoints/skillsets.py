from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
import logging

from models.github_app_request import GitHubAppRequestHeaders, GitHubAppRequest
from services.agent_services import process_skillset_request
from common.dependencies import validate_headers

router = APIRouter(prefix="/skillsets")

@router.post("/random-quote")
async def random_quote(
    request: GitHubAppRequest,
    headers: GitHubAppRequestHeaders = Depends(validate_headers),
):
    """
    Fetches a random quote from the FavQs API.

    Returns:
        StreamingResponse: A streaming response containing the quote in JSON format.
    """
    if request.parameter_name is not None:
        logging.info(f"Parameter name is: {request.parameter_name}")

    return process_skillset_request()

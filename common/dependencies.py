from fastapi import Header, Request, HTTPException
import logging
from models.github_app_request import GitHubAppRequestHeaders

logger = logging.getLogger(__name__)

async def validate_headers(

    request: Request,
    x_github_token: str = Header(..., alias="x-github-token"),
    x_github_public_key_identifier: str = Header(..., alias="x-github-public-key-identifier"),
    x_github_public_key_signature: str = Header(..., alias="x-github-public-key-signature"),
):
    """
    Asynchronous function to validate and verify GitHub-specific headers in an HTTP request.

    This function extracts the required headers from the incoming request, validates their presence, 
    and verifies the signature of the request body using the provided headers. If the validation 
    fails or an unexpected error occurs, appropriate HTTP exceptions are raised.

    Args:
        request (Request): The incoming HTTP request object.
        x_github_token (str): The GitHub token provided in the "x-github-token" header.
        x_github_public_key_identifier (str): The identifier for the public key provided in the 
            "x-github-public-key-identifier" header.
        x_github_public_key_signature (str): The signature of the request body provided in the 
            "x-github-public-key-signature" header.

    Returns:
        GitHubAppRequestHeaders: An object containing the validated headers if the signature verification succeeds.

    Raises:
        HTTPException: If the headers are invalid, the signature verification fails, or an unexpected 
            error occurs. Specific status codes include:
            - 500: Internal server error for unexpected exceptions.
    """
    try:
        headers = GitHubAppRequestHeaders(
            x_github_token=x_github_token,
            x_github_public_key_identifier=x_github_public_key_identifier,
            x_github_public_key_signature=x_github_public_key_signature,
        )
        body = await request.body()
        await headers.verify_signature(body)
        return headers
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error during header validation")
        raise HTTPException(status_code=500, detail="Internal server error")
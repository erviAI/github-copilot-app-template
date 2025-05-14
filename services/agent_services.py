from common.github import call_copilot_chat
from models.github_app_request import GitHubAppRequestHeaders, GitHubAppRequest, Message
import requests
import logging

logger = logging.getLogger(__name__)

def process_agent_request(headers: GitHubAppRequestHeaders, payload: GitHubAppRequest):
    """
    Processes an agent request by modifying the message payload and invoking a chat service.
    Args:
        headers (GitHubAppRequestHeaders): The headers containing metadata, including user authentication information.
        payload (GitHubAppRequest): The request payload containing the list of messages to process.
    Returns:
        Iterator[bytes]: An iterator over the content of the response from the chat service.
    Notes:
        - The function extracts the user information from the token in the headers.
        - It prepends system messages to the payload to set the context for the chat service.
        - The first system message instructs the assistant to start every response with the user's name.
        - The second system message sets the assistant's persona as the Blackbeard Pirate.
        - The modified messages are sent to the `call_copilot_chat` function for processing.
    """
    user = headers.get_user_from_token()

    messages = payload.messages
    messages.insert(0, Message(role="system", content=f"Start every response with the user's name, which is @{user}"))
    messages.insert(0, Message(role="system", content="You are a helpful assistant that replies to user messages as if you were the Blackbeard Pirate."))

    response = call_copilot_chat(messages, headers.x_github_token)
    return response.iter_content()

def process_skillset_request():
    """
    Processes a skillset request by modifying the message payload and invoking a chat service.
    Args:
        headers (GitHubAppRequestHeaders): The headers containing metadata, including user authentication information.
    Returns:
        JsonResponse: A JSON response containing the random quote and author.
    Notes:
        - The function extracts the user information from the token in the headers.
        - It fetches a random quote from the FavQs API.
        - The quote and author are logged for debugging purposes.
        - The function returns a JSON response with the quote and author.
    """
    response = requests.get("https://favqs.com/api/qotd")
    quote_data = response.json()
    author = quote_data["quote"]["author"]
    quote = quote_data["quote"]["body"]
    logger.info(f"Author: {author}")
    return {
        "quote": quote,
        "author": author
    }
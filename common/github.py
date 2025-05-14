import requests
from fastapi import HTTPException
import logging
from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.util import sigdecode_der
from hashlib import sha256
from base64 import b64decode
import threading

logger = logging.getLogger(__name__)

_cache_lock = threading.Lock()
_etag_cache = {}

def fetch_with_etag_cache(url: str, headers: dict = None):
    """
    Fetches a URL using ETag-based caching.
    Returns the JSON-decoded response body.
    Allows passing custom headers.
    """
    if headers is None:
        headers = {}
    key = url
    with _cache_lock:
        cache_entry = _etag_cache.get(key)
        if cache_entry:
            headers["If-None-Match"] = cache_entry["etag"]

    response = requests.get(url, headers=headers)
    if response.status_code == 304 and cache_entry:
        return cache_entry["body"]
    elif response.status_code == 200:
        etag = response.headers.get("ETag")
        body = response.json()
        if etag:
            with _cache_lock:
                _etag_cache[key] = {"etag": etag, "body": body}
        return body
    else:
        response.raise_for_status()

def fetch_public_key(key_identifier: str) -> str:
    """
    Fetches the public key from GitHub's Copilot API based on the provided key identifier.

    This function sends a GET request to the GitHub API to retrieve a list of public keys
    and searches for the key that matches the given key identifier and is marked as current.

    Args:
        key_identifier (str): The identifier of the public key to fetch.

    Returns:
        str: The PEM-encoded public key corresponding to the provided key identifier.

    Raises:
        HTTPException: If the request to GitHub fails or if the key identifier is invalid.
    """
    public_key_url = "https://api.github.com/meta/public_keys/copilot_api"
    try:
        data = fetch_with_etag_cache(public_key_url)
    except Exception:
        logger.error("Failed to fetch public keys from GitHub")
        raise HTTPException(status_code=500, detail="Failed to fetch public keys")
    public_keys = data.get("public_keys", [])
    public_key_pem = None
    for key in public_keys:
        if key["key_identifier"] == key_identifier and key["is_current"]:
            public_key_pem = key["key"]
            break
    if not public_key_pem:
        logger.info("Invalid Github-Public-Key-Identifier header")
        raise HTTPException(status_code=400, detail="Invalid Github-Public-Key-Identifier header")
    return public_key_pem

def verify_github_signature(key_identifier: str, signature_b64: str, data: bytes):
    """
    Verifies the GitHub webhook signature using the provided key identifier, 
    base64-encoded signature, and the original data.

    Args:
        key_identifier (str): The identifier for the public key used to verify the signature.
        signature_b64 (str): The base64-encoded signature to be verified.
        data (bytes): The original data that was signed.

    Raises:
        HTTPException: If the signature is invalid, an HTTP 400 exception is raised.

    Logs:
        Logs a message indicating whether the signature validation was successful or not.
    """
    public_key_pem = fetch_public_key(key_identifier)
    try:
        raw_sig = b64decode(signature_b64)
        verifier = VerifyingKey.from_pem(string=public_key_pem, hashfunc=sha256)
        verifier.verify(signature=raw_sig, data=data, sigdecode=sigdecode_der)
        logger.info("Message validated")
    except (BadSignatureError, ValueError):
        logger.info("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

def verify_github_token_for_user(token: str):
    """
    Verifies the validity of a GitHub personal access token for a user.

    This function sends a GET request to the GitHub API's `/user` endpoint
    using the provided token. If the token is invalid or unauthorized, an
    HTTPException is raised with a 401 status code. If the token is valid,
    the function returns the GitHub username associated with the token.

    Args:
        token (str): The GitHub personal access token to verify.

    Returns:
        str or None: The GitHub username associated with the token if valid,
                     otherwise None.

    Raises:
        HTTPException: If the token is invalid or unauthorized.
    """
    user_response = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {token}"})
    if user_response.status_code != 200:
        logger.info("Invalid GitHub token")
        raise HTTPException(status_code=401, detail="Invalid GitHub token")
    user = user_response.json()
    return user.get("login", None)

def call_copilot_chat(messages, token):
    """
    Calls the GitHub Copilot chat completions API with the given messages and token.
    Returns the requests.Response object.
    """
    response = requests.post(
        "https://api.githubcopilot.com/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "messages": [message.model_dump() for message in messages],
            "stream": True
        }
    )
    response.raise_for_status()
    return response

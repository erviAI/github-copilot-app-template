from pydantic import BaseModel
from typing import List
import logging
from common.github import verify_github_signature, verify_github_token_for_user

logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class GitHubAppRequest(BaseModel):
    # make optional
    messages: List[Message] = None
    parameter_name: str = None

class GitHubAppRequestHeaders(BaseModel):
    x_github_token: str
    x_github_public_key_identifier: str
    x_github_public_key_signature: str

    async def verify_signature(self, request_body: bytes):
        verify_github_signature(
            self.x_github_public_key_identifier,
            self.x_github_public_key_signature,
            request_body,
        )
    
    def get_user_from_token(self):
        return verify_github_token_for_user(self.x_github_token)

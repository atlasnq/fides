"""This module handles finding and parsing fides configuration files."""

# pylint: disable=C0115,C0116, E0213

from typing import Dict, Optional

from pydantic import validator

from fidesctl.ctl.core.utils import generate_request_headers

from .fides_settings import FidesSettings


class FidesctlUserSettings(FidesSettings):
    """Class used to store values from the 'user' section of the config."""

    user_id: str = "1"
    api_key: str = "test_api_key"
    request_headers: Dict[str, str] = dict()
    encryption_key: str = "test_encryption_key"
    analytics_opt_out: Optional[bool]

    # Automatically generate the request_headers on object creation
    @validator("request_headers", pre=True, always=True)
    @classmethod
    def get_request_headers(cls, value: Optional[Dict], values: Dict) -> Dict[str, str]:
        return generate_request_headers(values["user_id"], values["api_key"])

    class Config:
        env_prefix = "FIDESCTL__USER__"

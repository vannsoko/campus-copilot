from auth.providers.base import SSOProvider
from auth.providers.tum import TUMProvider

# Registry of available SSO providers
PROVIDERS: dict[str, type[SSOProvider]] = {
    "tum": TUMProvider
}


def get_provider(name: str) -> type[SSOProvider]:
    """Get an SSO provider class by name."""
    provider = PROVIDERS.get(name.lower())
    if not provider:
        available = ", ".join(PROVIDERS.keys())
        raise ValueError(f"Unknown SSO provider: {name}. Available: {available}")
    return provider

"""Provider-agnostic LLM integration (milestone §1). LLMs propose; the deterministic layer verifies,
calculates and traverses; humans validate.

MockProvider / AnthropicProvider are exposed lazily so importing this package (or `base`) never
pulls in the concrete providers or the Anthropic SDK eagerly (avoids an import cycle with
gridpulse.inference, which imports the proposal schemas from `base`)."""
from .base import (AIInvocation, ChangeLinkProposal, Citation, DependencyProposal,
                   EntityLinkProposal, LLMProvider, MissingConfigError, ProviderError, from_env)

__all__ = ["AIInvocation", "ChangeLinkProposal", "Citation", "DependencyProposal",
           "EntityLinkProposal", "LLMProvider", "MissingConfigError", "ProviderError",
           "from_env", "MockProvider", "AnthropicProvider"]


def __getattr__(name):
    if name == "MockProvider":
        from .mock import MockProvider
        return MockProvider
    if name == "AnthropicProvider":
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider
    raise AttributeError(name)

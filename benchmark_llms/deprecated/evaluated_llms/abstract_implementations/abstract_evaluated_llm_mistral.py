# File: abstract_evaluated_llm_mistral.py

# ==============================================================================
# AbstractEvaluatedLLMMistral
# ------------------------------------------------------------------------------
# This intermediary abstract class exists to separate Mistral-specific logic
# from the provider-specific access layer (e.g., Vultr, Together.ai).
#
# Currently, all Mistral models are accessed via Vultr API and therefore this
# class inherits from AbstractEvaluatedLLMVultr. However, if in the future we
# decide to switch providers (e.g., Lambda, AWS, or run our own instance),
# we only need to update this file — not each concrete model implementation.
#
# This ensures loose coupling between model identity (Mistral) and API provider.
# ==============================================================================

from benchmark_llms.deprecated.evaluated_llms.abstract_implementations.abstract_evaluated_llm_vultr import AbstractEvaluatedLLMVultr

class AbstractEvaluatedLLMMistral(AbstractEvaluatedLLMVultr):
    pass
class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass

class OpenAIAPIError(AIServiceError):
    """Exception for OpenAI API specific errors"""
    pass

class ConfigurationError(AIServiceError):
    """Exception for configuration related errors"""
    pass

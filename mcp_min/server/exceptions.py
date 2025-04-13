"""Custom exceptions for FastMCP."""


class MCPServerError(Exception):
    """Base error for FastMCP."""


class ValidationError(MCPServerError):
    """Error in validating parameters or return values."""


class ResourceError(MCPServerError):
    """Error in resource operations."""


class ToolError(MCPServerError):
    """Error in tool operations."""


class InvalidSignature(Exception):
    """Invalid signature for use with FastMCP."""

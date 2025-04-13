"""Resource manager functionality."""

from collections.abc import Callable
from typing import Any

from pydantic import AnyUrl

from .base import Resource
from .templates import ResourceTemplate


class ResourceManager:
    """Manages FastMCP resources."""

    def __init__(self):
        self._resources: dict[str, Resource] = {}
        self._templates: dict[str, ResourceTemplate] = {}

    def add_resource(self, resource: Resource) -> Resource:
        """Add a resource to the manager.

        Args:
            resource: A Resource instance to add

        Returns:
            The added resource. If a resource with the same URI already exists,
            returns the existing resource.
        """
        existing = self._resources.get(str(resource.uri))
        if existing:
            return existing
        self._resources[str(resource.uri)] = resource
        return resource

    def add_template(
        self,
        fn: Callable[..., Any],
        uri_template: str,
        name: str | None = None,
        description: str | None = None,
        mime_type: str | None = None,
    ) -> ResourceTemplate:
        """Add a template from a function."""
        template = ResourceTemplate.from_function(
            fn,
            uri_template=uri_template,
            name=name,
            description=description,
            mime_type=mime_type,
        )
        self._templates[template.uri_template] = template
        return template

    async def get_resource(self, uri: AnyUrl | str) -> Resource | None:
        """Get resource by URI, checking concrete resources first, then templates."""
        uri_str = str(uri)

        # First check concrete resources
        if resource := self._resources.get(uri_str):
            return resource

        # Then check templates
        for template in self._templates.values():
            if params := template.matches(uri_str):
                try:
                    return await template.create_resource(uri_str, params)
                except Exception as e:
                    raise ValueError(f"Error creating resource from template: {e}")

        raise ValueError(f"Unknown resource: {uri}")

    def list_resources(self) -> list[Resource]:
        """List all registered resources."""
        return list(self._resources.values())

    def list_templates(self) -> list[ResourceTemplate]:
        """List all registered templates."""
        return list(self._templates.values())

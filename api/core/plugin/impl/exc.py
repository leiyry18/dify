from collections.abc import Mapping

from pydantic import TypeAdapter


class PluginDaemonError(Exception):
    """Base class for all plugin daemon errors."""

    def __init__(self, description: str) -> None:
        self.description = description

    def __str__(self) -> str:
        # returns the class name and description
        return f"{self.__class__.__name__}: {self.description}"


class PluginDaemonInternalError(PluginDaemonError):
    pass


class PluginDaemonClientSideError(PluginDaemonError):
    pass


class PluginDaemonInternalServerError(PluginDaemonInternalError):
    description: str = "Internal Server Error"


class PluginDaemonUnauthorizedError(PluginDaemonInternalError):
    description: str = "Unauthorized"


class PluginDaemonNotFoundError(PluginDaemonInternalError):
    description: str = "Not Found"


class PluginDaemonBadRequestError(PluginDaemonClientSideError):
    description: str = "Bad Request"


class PluginInvokeError(PluginDaemonClientSideError):
    description: str = "Invoke Error"

    def _get_error_object(self) -> Mapping:
        try:
            return TypeAdapter(Mapping).validate_json(self.description)
        except Exception:
            return {}

    def get_error_type(self) -> str:
        return self._get_error_object().get("error_type", "unknown")

    def get_error_message(self) -> str:
        try:
            return self._get_error_object().get("message", "unknown")
        except Exception:
            return self.description


class PluginUniqueIdentifierError(PluginDaemonClientSideError):
    description: str = "Unique Identifier Error"


class PluginNotFoundError(PluginDaemonClientSideError):
    description: str = "Plugin Not Found"


class PluginPermissionDeniedError(PluginDaemonClientSideError):
    description: str = "Permission Denied"

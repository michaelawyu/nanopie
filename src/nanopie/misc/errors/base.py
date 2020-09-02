"""This module includes the base classes for nanopie exceptions.
"""

from typing import Any, Optional, Union


class ServiceError(Exception):
    """The base class for all nanopie exceptions."""

    def __init__(self, *args, response: Optional["RPCResponse"] = None):
        """Initializes a service error.

        Args:
            response (RPCResponse, Optional): An RPC response. If one of the
                handlers throws an exception with a response configured
                when processing a request, the nanopie service should return
                the response to the caller instead of reporting the exception.
            *args: Arbitrary positional arguments.
        """
        self.response = response
        super().__init__(*args)


class AuthenticationError(ServiceError):
    """The base class for all authentication related exceptions."""


class SerializationError(ServiceError):
    """The base class for all serialization related exceptions."""


class ValidationError(ServiceError):
    """The base class for all data validation related exceptions."""

    def __init__(
        self,
        *args,
        source: Union["Field", "ModelMetaCls"],
        data: Any,
        response: Optional["RPCResponse"] = None
    ):
        """Initializes a validation error.

        Args:
            source (Union[Field, ModelMetaCls]): The field or the model used
                for data validation.
            data (Any): A piece of data.
            response (RPCResponse, Optional): An RPC Response.
                See `ServiceError`.
            *args: Arbitrary positional arguments.
        """
        self.source = source
        self.data = data

        super().__init__(*args, response=response)


class FoundationError(ServiceError):
    """The base class for all foundation handler related exceptions."""

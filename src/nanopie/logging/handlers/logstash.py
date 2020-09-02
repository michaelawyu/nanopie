"""This module includes the logging handlers for connecting to a Logstash service.

See also https://docs.python.org/3/library/logging.handlers.html.

To-Do: The logging handlers here are for proof-of-concept purposes only; they
are temporary workarounds before a universal interface for service integration
becomes available.
"""

from logging.handlers import DatagramHandler, SocketHandler


class LogstashTCPHandler(SocketHandler):
    """The logging handler for connecting to a Logstash service via TCP."""

    def makePickle(self, record: "LogRecord") -> bytes:
        """See the method `logging.handlers.SocketHandler.makePickle`."""
        return self.formatter.format(record).encode() + b"\n"


class LogstashUDPHandler(DatagramHandler):
    """The logging handler for connecting to a Logstash service via UDP."""

    def makePickle(self, record: "LogRecord") -> bytes:
        """See the method `logging.handlers.SocketHandler.makePickle`."""
        return self.formatter.format(record).encode() + b"\n"

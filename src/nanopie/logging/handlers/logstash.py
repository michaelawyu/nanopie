from logging.handlers import DatagramHandler, SocketHandler


class LogstashTCPHandler(SocketHandler):
    """
    """

    def makePickle(self, record):
        return self.formatter.format(record) + b"\n"


class LogstashUDPHandler(DatagramHandler):
    """
    """

    def makePickle(self, record):
        return self.formatter.format(record) + b"\n"

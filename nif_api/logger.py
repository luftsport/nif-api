from lxml import etree
from zeep import Plugin
import logging
import sys


class LoggingPlugin(Plugin):
    """A simple logging plugin for Zeep
    Will log all received (ingress) and sent (egress) messages
    """

    def __init__(self, file_name):
        self.pretty_print = False
        self.logger = logging.getLogger('nif_integration')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')

        if not len(self.logger.handlers):
            self.fh = logging.FileHandler(file_name)
            self.fh.setLevel(logging.DEBUG)
            self.fh.setFormatter(self.formatter)
            self.logger.addHandler(self.fh)

    # Receive
    def ingress(self, envelope, http_headers, operation):
        self.logger.debug('<<< RECV {}\n{}\n{}'.format(operation,
                                                       http_headers,
                                                       etree.tostring(envelope, pretty_print=self.pretty_print)))

        return envelope, http_headers

    # Send
    def egress(self, envelope, http_headers, operation, binding_options):
        self.logger.debug('SEND >>> {}\n{}\n{}'.format(operation,
                                                       http_headers,
                                                       etree.tostring(envelope, pretty_print=self.pretty_print)))

        return envelope, http_headers

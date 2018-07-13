from osg.base import Configuration
from ftplib import FTP_TLS
import socket

        
class ExplicitTLS(Configuration):
    """
    This class includes methods to allow establishing a secure Explicit FTP secure connection to the One Scotland Gazetteer FTP
    """

    def __init__(self):
        Configuration.__init__(self)
        self.host = self.get_configuration_for('ftp', 'host')
        self.port = int(self.get_configuration_for('ftp', 'port'))
        self.username = self.get_configuration_for('ftp', 'username')
        self.password = self.get_configuration_for('ftp', 'password')

    def setup(self):
        # An FTP subclass which adds TLS support to FTP
        self.client = FTP_TLS(timeout=10)

    def connect(self):

        self.client.connect(host=self.host, port=self.port)

    def login(self):
        self.client.login(user=self.username, passwd=self.password)

        #Make our connection to the server secure (i.e. encrypted)
        self.client.prot_p()

        #This is a hack making 'ftplib' use the EPSV network protocol (i.e. an IPv6 connection) instead of the PASV
        #protocol (i.e. an IPv4). The reason for doing this is that there is a bug in FTP lib which returns the wrong
        #IP address after connection to the FTP if PASV is used. In contrast if the EPSV protocol is used the FTP IP is
        #returned correctly allowing further commands to the FTP connection.
        self.client.af = socket.AF_INET6

        return self.client


import sys

from ftplib import FTP_TLS
import socket


class Conf(configuration.Conf):

    def __init__(self):

        self.host = "213.128.245.37"
        self.user = "your-user"
        self.password = "your-pass"
        self.port = 990


class ExplicitTLS(Conf):

    def __init__(self):

        Conf.__init__(self)

    def setup(self):

        #A FTP subclass which adds TLS support to FTP.
        self.client = FTP_TLS(timeout=10)

        #Set the instance’s debugging level. This controls the amount of debugging output printed.
        #self.client.set_debuglevel(1)

    def connect(self):

        # Connect to the given host and port.
        self.client.connect(host=self.host, port=self.port)

    def login(self):

        # Log in as the given user.
        self.client.login(user=self.user, passwd=self.password)

        #Make our connection to the server secure (i.e. encrypted)
        self.client.prot_p()

        #This is a hack making 'ftplib' use the EPSV network protocol (i.e. an IPv6 connection) instead of the PASV
        #protocol (i.e. an IPv4). The reason for doing this is that there is a bug in FTP lib which returns the wrong
        #IP address after connection to the FTP if PASV is used. In contrast if the EPSV protocol is used the FTP IP is
        #returned correctly allowing further commands to the FTP connection.
        self.client.af = socket.AF_INET6

        return self.client

    def tear_down(self):
        """
        Close the FTP connection unilaterally.
        :return:
        """

        self.client.close()

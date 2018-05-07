from ftplib import FTP_TLS
import socket
import configuration


class Conf(configuration.Ftp):

    def __init__(self):

        configuration.Ftp.__init__(self)

        self.host = self.ftp_host
        self.user = self.ftp_user
        self.password = self.ftp_pass
        self.port = self.ftp_port

        
class ExplicitTLS(Conf):
    """
    This class includes methods to allow establishing a secure Explicit FTP secure connection to the One Scotland Gazetteer FTP
    """

    def __init__(self):

        Conf.__init__(self)

    def setup(self):

        #A FTP subclass which adds TLS support to FTP.
        self.client = FTP_TLS(timeout=10)

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

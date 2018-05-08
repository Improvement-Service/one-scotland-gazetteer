class Ftp:

    usr = 'your-ftp-user'
    pwd = 'your-ftp-pass'

    def __init__(self):

        self.host = '213.128.245.37'
        self.port = 990


class WebServices:

    usr = 'your-web-service-user'
    pwd = 'your-web-service-pass'

    def __init__(self):

        self.host = 'https://osg.scot/services'

        # REST service information - Check documentation for further details for the schema.
        self.rest = {'wadl': '%s/NGSearchServiceRest?_wadl' % self.host,
                     'services': {
                         'list': {'url': self.host + '/NGSearchServiceRest/NGService/sendNGListDataSetsMessage',
                                  'schemas': {"listdatasets": {}}},
                         'search': {'url': self.host + '/NGSearchServiceRest/NGService/sendNGSearchMessage',
                                    'schemas': {}}},
                     'headers': {"Content-Type": "application/json", "Accept": "application/json",
                                 "username": self.usr, "password": self.pwd}}


        # SOAP service information
        self.soap = {'wsdl': '%s/NGSearchService?wsdl' % self.host,
                     'services': {
                         'list': self.host + '',
                         'search': self.host + ''},
                     'post_schemas': '',
                     'headers': {}}


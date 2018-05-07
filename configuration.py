class Ftp:

    def __init__(self):

        self.ftp_host = '213.128.245.37'
        self.ftp_user = 'dimitrios.michelakis'
        self.ftp_pass = 'ROQD20$b'
        self.ftp_port = 990


class WebServices:

    def __init__(self):

        self.services_host = 'https://osg.scot/services'

        # REST service information - Check documentation for further details for the schema.
        self.rest = {'wadl': '%s/NGSearchServiceRest?_wadl' % self.services_host,
                     'services': {
                         'list': {'url': self.services_host + '/NGSearchServiceRest/NGService/sendNGListDataSetsMessage',
                                  'schemas': {"listdatasets": {}}},
                         'search': {'url': self.services_host + '/NGSearchServiceRest/NGService/sendNGSearchMessage',
                                    'schemas': {}}}}

        # SOAP service information
        self.soap = {'wsdl': '%s/NGSearchService?wsdl' % self.services_host,
                     'services': {
                         'list': self.services_host + '',
                         'search': self.services_host + ''},
                     'post_schemas': ''}


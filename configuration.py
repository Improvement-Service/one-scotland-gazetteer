class Conf:

    def __init__(self):

        self.ftp_host = '213.128.245.37'
        self.ftp_user = 'your-user'
        self.ftp_pass = 'your-pass'
        self.ftp_port = 990


class WebServicesConf:

    def __init__(self):

        self.root = 'https://osg.scot/services'

        # REST service information
        self.rest = {'wadl': '%s/NGSearchServiceRest?_wadl' % root,
                     'services': {'list': root + '/NGSearchServiceRest/NGService/sendNGListDataSetsMessage',
                                  'search': root + '/NGSearchServiceRest/NGService/sendNGSearchMessage'}}

        # SOAP service information
        self.soap = {'wsdl': '%s/NGSearchService?wsdl' % root,
                     'services': {'list': root + '',
                                  'search': root + ''}}




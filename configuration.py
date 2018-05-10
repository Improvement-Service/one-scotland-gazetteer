class Ftp:

    usr = 'your-ftp-user'
    pwd = 'your-ftp-pass'

    def __init__(self):

        self.host = '213.128.245.37'
        self.port = 990


class WebServices:

    usr = 'your-service-user'
    pwd = 'your-service-pass'

    def __init__(self):

        self.host = 'https://osg.scot/services'
        #self.host = 'https://test.osg.scot/services'

        self.service = {'list': 'sendNGListDataSetsMessage',
                        'search': 'sendNGSearchMessage'}

        # REST service information - Check documentation for further details for the schema.
        self.rest = {'schema': '%s/NGSearchServiceRest?_wadl' % self.host,
                     'entry_point': {
                         'list': {'url': self.host + '/NGSearchServiceRest/NGService/%s' % self.service['list']},
                         'search': {'url': self.host + '/NGSearchServiceRest/NGService/%s' % self.service['search']}},
                     'headers': {"Content-Type": "application/json",
                                 "Accept": "application/json",
                                 "username": self.usr,
                                 "password": self.pwd}}


        # SOAP service information
        self.soap = {'schema': '%s/NGSearchService?wsdl' % self.host,
                     'entry_point': {
                         'list': self.host + '',
                         'search': self.host + ''},
                     'post_schemas': '',
                     'headers': {}}

        # Result dictionary communicated to user
        self.data_dict = {'message': None, 'data': None}


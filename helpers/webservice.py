import requests
import json
import configuration
from requests.exceptions import SSLError
import sys


class Response(configuration.WebServices):

    def __init__(self):

        configuration.WebServices.__init__(self)

        # This attribute holds the necessary headers to request data from the REST entry points
        self.headers = self.rest['headers']

        # This attribute will hold the response data as returned from the Response workflow. This attribute needs to be
        # initialised as below for the sake of readability since colleagues expect to find all class attributes in
        # the __init__ method.
        self.response = {'request_url': None, 'body': None, 'code': None, 'headers': None, 'time': None}

    def request(self, request_url, data):

        try:
            data = requests.post(url=request_url, data=json.dumps(data), headers=self.headers)
        except SSLError as e:
            if 'test.osg.scot' in request_url:
                data = requests.post(url=request_url, data=json.dumps(data), headers=self.headers, verify=False)
            elif 'test.osg.scot' not in request_url:
                print('SSL Error - SSL certificate verification failed - please contact osg.scot to report this')
                sys.exit(1)

        self.response['request_url'] = request_url
        self.response['body'] = data.content
        self.response['code'] = data.status_code
        self.response['headers'] = data.headers
        self.response['time'] = data.elapsed.total_seconds()


class PreProcess(Response):

    def __init__(self):
        Response.__init__(self)

        # This attribute will hold a message for the user (i.e. 'success' or 'failure') and the data as returned from
        # the PreProcessing workflow. This attribute needs to be initialised as below for the sake of readability since
        # colleagues expect to find all class attributes in the __init__ method.
        self.pre_processed = self.data_dict

    def content(self, request_url, data):
        """(binary str) -> list
        The content returned using the web services is parsed and returned as a list of dictionaries for easier
        post-processing. An example is following using the 'list' functionality (i.e. 'sendNGListDataSetsMessage')
        :param content: b'{"ListDataSetsResponseMessage":{"Header":{"self.pre_processedCount":8,"ReturnCount":8,
        "ErrorCode":0, "ErrorMessage":"Success"},"NGListDataSetsResponseData":[{"DataSet":"EST_STANDARD_SEARCH",
        "Col":["Address_One_Line","Custodian","Easting", "Northing", "Parent_UPRN", "Postcode", "Search_Building_Name",
        "Search_Building_No", "Search_Town", "Status", "UPRN", "USRN"]}
        :return: {'message': 'success', 'data': 'data': [{'DataSet': 'EST_STANDARD_SEARCH', 'Col': ['Address_One_Line',
        'Custodian', 'Easting', 'Northing', 'Parent_UPRN', 'Postcode', 'Search_Building_Name', 'Search_Building_No',
        'Search_Town', 'Status', 'UPRN', 'USRN']},...,{'DataSet': '...', 'Col': [...]}}
        """

        self.request(request_url, data)
        data = json.loads(self.response['body'].decode('utf-8'))

        # OSG services contents are different due to the different schema for each of the services. This is handled
        # below by trying different keys which are expected to be present in the response.
        try:
            # Processing a response from listing available datasets
            data = data['ListDataSetsResponseMessage']
            error = data['Header']['ErrorMessage']
            if error == 'Success':
                self.pre_processed['message'] = 'success'
                self.pre_processed['data'] = [dataset for dataset in data['NGListDataSetsResponseData']]
            else:
                self.pre_processed['message'] = 'failure'
                self.pre_processed['data'] = error
        except KeyError:
            data = data['SearchResponseMessage']
            error = data['NGSearchResponseData']['Header']['ErrorMessage']
            if error == 'Success':
                self.pre_processed['message'] = 'success'
                self.pre_processed['data'] = data['NGSearchResponseData']['Result']['any']
            else:
                self.pre_processed['message'] = 'failure'
                self.pre_processed['data'] = error


class PostProcess(PreProcess):

    def __init__(self):
        PreProcess.__init__(self)
        self.post_processed = self.data_dict

    def dataset_names(self, request_url, data):
        """
        Returns the available dataset names in a list. The data input should be
        :param data: {'message': 'success', 'data': 'data': [{'DataSet': 'EST_STANDARD_SEARCH',
        'Col': ['Address_One_Line', 'Custodian', 'Easting', 'Northing', 'Parent_UPRN', 'Postcode',
        'Search_Building_Name', 'Search_Building_No', 'Search_Town', 'Status', 'UPRN', 'USRN']},...,
        {'DataSet': '...', 'Col': [...]}}
        :return: ['EST_STANDARD_SEARCH',...,'...','...',...]
        """

        self.content(request_url, data)
        data = self.pre_processed
        if data['message'] != 'failure':
            self.post_processed['message'] = 'success'
            self.post_processed['data'] = [item['DataSet'] for item in data['data']]
        else:
            self.post_processed['message'] = ['failure']
            self.post_processed['data'] = data['data']





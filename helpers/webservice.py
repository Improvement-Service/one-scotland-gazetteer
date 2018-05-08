import requests
import json
import configuration


class RawContent(configuration.WebServices):

    def __init__(self):

        configuration.WebServices.__init__(self)

        # This attribute holds the necessary headers to request data from the REST entry points
        self.headers = self.rest['headers']

        # This attribute will hold the content data as returned from the request. This attribute needs to be initialised
        # as None for the sake of readability as colleagues expect to find all class attributes in the __init__ method.
        self.content_data = None

    def get_content_from_request(self, url, data):
        response = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        self.content_data = response.content


class PreProcess(RawContent):

    def __init__(self):
        RawContent.__init__(self)

        # This attribute will hold the response data as returned from the PreProcessing workflow. This attribute needs
        # to be initialised as None for the sake of readability as colleagues expect to find all class attributes in the
        # __init__ method.
        self.response_data = None

    def response(self, url, data):
        """(binary str) -> list
        The content returned using the web services is parsed and returned as a list of dictionaries for easier
        post-processing. An example is following using the 'list' functionality (i.e. 'sendNGListDataSetsMessage')
        :param content: b'{"ListDataSetsResponseMessage":{"Header":{"ResultCount":8,"ReturnCount":8,"ErrorCode":0,
        "ErrorMessage":"Success"},"NGListDataSetsResponseData":[{"DataSet":"EST_STANDARD_SEARCH",
        "Col":["Address_One_Line","Custodian","Easting", "Northing", "Parent_UPRN", "Postcode", "Search_Building_Name",
        "Search_Building_No", "Search_Town", "Status", "UPRN", "USRN"]}
        :return: {'message': 'success', 'data': 'data': [{'DataSet': 'EST_STANDARD_SEARCH', 'Col': ['Address_One_Line',
        'Custodian', 'Easting', 'Northing', 'Parent_UPRN', 'Postcode', 'Search_Building_Name', 'Search_Building_No',
        'Search_Town', 'Status', 'UPRN', 'USRN']},...,{'DataSet': '...', 'Col': [...]}}
        """

        result = {'message': None, 'data': None}

        self.get_content_from_request(url, data)
        data = json.loads(self.content_data.decode('utf-8'))

        # OSG services contents are different due to the different schema for each of the services. This is handled
        # below by trying different keys which are expected to be present in the response.
        try:
            # Processing a response from listing available datasets
            data = data['ListDataSetsResponseMessage']
            error = data['Header']['ErrorMessage']
            if error == 'Success':
                result['message'] = 'success'
                result['data'] = [dataset for dataset in data['NGListDataSetsResponseData']]
            else:
                result['message'] = 'failure'
                result['data'] = error
        except KeyError:
            data = data['SearchResponseMessage']
            error = data['NGSearchResponseData']['Header']['ErrorMessage']
            if error == 'Success':
                result['message'] = 'success'
                result['data'] = data['NGSearchResponseData']['Result']['any']
            else:
                result['message'] = 'failure'
                result['data'] = error

        self.response_data = result
        return self.response_data


class PostProcess(PreProcess):

    def __init__(self):
        PreProcess.__init__(self)

    def dataset_names(self, url, data):
        """
        Returns the available dataset names in a list. The data input should be
        :param data: {'message': 'success', 'data': 'data': [{'DataSet': 'EST_STANDARD_SEARCH',
        'Col': ['Address_One_Line', 'Custodian', 'Easting', 'Northing', 'Parent_UPRN', 'Postcode',
        'Search_Building_Name', 'Search_Building_No', 'Search_Town', 'Status', 'UPRN', 'USRN']},...,
        {'DataSet': '...', 'Col': [...]}}
        :return: ['EST_STANDARD_SEARCH',...,'...','...',...]
        """

        data = self.response(url, data)
        return [item['DataSet'] for item in data['data']]





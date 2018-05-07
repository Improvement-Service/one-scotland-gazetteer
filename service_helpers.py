import requests
import json


class Content:

    def __init__(self, username, password):

        self.headers = {"Content-Type": "application/json",
                        "Accept": "application/json",
                        "username": username,
                        "password": password}

    def test_description_language_availability(self, description_language):
        """(str) -> bool
        The OSG services can be consumed using two different descriptions languages (i.e. the Web application
        Description Language - WADL to support REST, and the Web Services Description Language - WSDL to support SOAP.
        This function checks the availability of the WADL or the WSDL depending the parameter provided by the user.
        :param wadl: 'https://osg.scot/services/NGSearchServiceRest?_wadl'
        :return: True
        """

        response = requests.get(description_language)

        if response.status_code is 200:
            return True
        else:
            return False

    def list_available_datasets(self, service):

        data = {"listdatasets": {}}
        response = requests.post(url=service, data=json.dumps(data), headers=self.headers)

        return response.content

    def query_available_datasets(self, service, data):

        response = requests.post(url=service, data=json.dumps(data), headers=self.headers)

        return response.content


class PreProcess:

    def __init__(self):
        pass

    @staticmethod
    def response(content):
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

        data = json.loads(content.decode('utf8'))

        # OSG services contents are different due to the different schema for each of the services. This is handled
        # below by trying different keys which are expected to be present in the response.
        try:
            # Processing a response from listing available datasets
            data = data['ListDataSetsResponseMessage']
            if data['Header']['ErrorMessage'] == 'Success':
                result['message'] = 'success'
                result['data'] = [dataset for dataset in data['NGListDataSetsResponseData']]
            else:
                result['message'] = 'failure'
                result['data'] = None
        except KeyError:
            data = data['SearchResponseMessage']
            if data['NGSearchResponseData']['Header']['ErrorMessage'] == 'Success':
                result['message'] = 'success'
                result['data'] = data['NGSearchResponseData']['Result']['any']
            else:
                result['message'] = 'failure'
                result['data'] = None

        return result


class PostProcess:

    def __init__(self):
        pass

    @staticmethod
    def dataset_names(data):
        """
        Returns the available dataset names in a list. The data input should be
        :param data: {'message': 'success', 'data': 'data': [{'DataSet': 'EST_STANDARD_SEARCH',
        'Col': ['Address_One_Line', 'Custodian', 'Easting', 'Northing', 'Parent_UPRN', 'Postcode',
        'Search_Building_Name', 'Search_Building_No', 'Search_Town', 'Status', 'UPRN', 'USRN']},...,
        {'DataSet': '...', 'Col': [...]}}
        :return: ['EST_STANDARD_SEARCH',...,'...','...',...]
        """

        return [item['DataSet'] for item in data['data']]





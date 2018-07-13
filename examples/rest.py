import sys
sys.path.insert(0, '../')

from osg.base import Configuration
from osg.service import PreProcess, PostProcess


class Tools(Configuration):

    def __init__(self):
        Configuration.__init__(self)
        self.pre_process = PreProcess()
        self.post_process = PostProcess()


class Rest(Tools):

    def __init__(self):
        Tools.__init__(self)
        self.list = self.get_configuration_for('rest', 'list')
        self.search = self.get_configuration_for('rest', 'search')

    def all_dataset_names_available_in_osg_to_query(self):

        post_data = {"listdatasets": {}}

        self.post_process.dataset_names(self.list, post_data)
        return self.post_process.post_processed

    def all_data_from_a_dataset_filtering_by_attributes(self, dataset=None, attributes=[]):
        """ (str, list) -> list
        Returns the OSG data as a list of dictionaries which is extracted from an OSG dataset for a specific UPRN.
        :param dataset: 'EST_STANDARD_SEARCH'
        :param attributes: [{"name": "UPRN", "value": ["35000001"], 'matchtype': 'equal to'}]
        :return: {'message': 'success', 'data': [{'SEARCH_TOWN': '|ALLOA||ALLOA|', 'POSTCODE': 'FK10 2EA',
        'EASTING': 287561.0, 'STATUS': 1, 'SEARCH_BUILDING_NAME': '|||', 'SEARCH_STREET_NAME': '||ACADEMY STREET|',
        'ADDRESS_ONE_LINE': '1 ACADEMY STREET, ALLOA, FK10 2EA.', 'PARENT_UPRN': '',
        'SEARCH_POSTCODE_NO_SPACE': 'FK102EA', 'NORTHING': 693618.0, 'USRN': '8500253', 'SEARCH_BUILDING_NO': '|1||||',
        'CUSTODIAN': 9056, 'UPRN': 35000001}]}
        """

        post_data = {"query": {"dataset": dataset,
                               "attribute": attributes}}

        self.pre_process.content(self.search, post_data)
        return self.pre_process.pre_processed

    def all_data_from_a_dataset_filtering_by_attributes_and_sorting_results(self, dataset=None, attributes=[], field=None, order=None):

        post_data = {"query": {"dataset": dataset,
                               "attribute": attributes,
                               'sortField': field,
                               'sortOrder': order}}

        self.pre_process.content(self.search, post_data)
        return self.pre_process.pre_processed

    def all_data_from_a_dataset_filtering_by_attributes_and_geometry(self, dataset=None, attributes=[], area=[]):
        """
        Returns the OSG data as a list of dictionaries which is extracted from the defined OSG dataset as specified in
        this function and the specified attributes & area too.
        :param dataset: 'EST_STANDARD_SEARCH'
        :param attributes: [{"name": "UPRN", "value": ["1"], "matchtype": "between"},
        {"name": "USRN", "value": ["8500253"], "matchtype": "equal to"}]
        :param area: [{"value": "Cramond", "matchtype": "in"}]
        :return:
        """

        post_data = {"query": {"dataset": dataset,
                               "attribute": attributes,
                               "area": area}}

        self.pre_process.content(self.search, post_data)
        return self.pre_process.pre_processed

    def all_data_from_a_dataset_filtering_by_radius(self, dataset=None, radius={}):

        post_data = {"query": {"dataset": dataset,
                               "type": "full",
                               "within": radius}}

        self.pre_process.content(self.search, post_data)
        return self.pre_process.pre_processed


def main():

    rest = Rest()

    # Return a list of all the available datasets
    datasets = rest.all_dataset_names_available_in_osg_to_query()
    print(datasets)
    datasets = datasets['data']

    # Attribute query in dataset 'EST_STANDARD_SEARCH' - using one attribute
    attributes = [{"name": "UPRN", "value": ["35000001"], 'matchtype': 'equal to'}]
    b = rest.all_data_from_a_dataset_filtering_by_attributes(dataset=datasets[0],
                                                             attributes=attributes)
    print(b)

    # Attribute query in dataset 'FVGIS_STANDARD_SEARCH' - by a range of values
    attributes = [{"name": "UPRN", "value": ["35000001", "35000010"], "matchtype": "between"}]
    c = rest.all_data_from_a_dataset_filtering_by_attributes(dataset=datasets[4],
                                                             attributes=attributes)
    print(c)

    # Attribute query - sort results by field name & ascending or descending order - default is 'asc' order
    attributes = [{"name": "UPRN", "value": ["35000001", "35000010"], "matchtype": "between"},
                  {"name": "USRN", "value": ["8500253"], "matchtype": "equal to"}]
    d = rest.all_data_from_a_dataset_filtering_by_attributes_and_sorting_results(dataset=datasets[0],
                                                                                 attributes=attributes,
                                                                                 field='UPRN',
                                                                                 order='desc')
    print(d)

    # Combination of attribute and spatial query - assumes polygon stored in the database
    attributes = [{"name": "UPRN", "value": ["35000001", "35000010"], "matchtype": "between"},
                  {"name": "USRN", "value": ["8500253"], "matchtype": "equal to"}]
    area = [{"value": "Cramond", "matchtype": "in"}]
    e = rest.all_data_from_a_dataset_filtering_by_attributes_and_geometry(dataset=datasets[6],
                                                                          attributes=attributes,
                                                                          area=area)
    print(e)

    # Spatial query - buffer area controlled by the user - This type of query works only for the dataset
    # 'STD_ADDRESS_SEARCH'.
    radius = {"easting": 279717.0, "northing": 692958.0, "distance": 10000.0}
    f = rest.all_data_from_a_dataset_filtering_by_radius(dataset=datasets[6],
                                                         radius=radius)
    print(f)


if __name__ == "__main__":
    main()

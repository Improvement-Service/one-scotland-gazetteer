from helpers import webservice as svh
from configuration import WebServices
import sys


def main():

    conf = WebServices()
    raw_content = svh.RawContent()

    # REST tests & examples #
    # Check if the WADL is available
    web_service_availability = raw_content.test_description_language_availability(conf.rest['wadl'])

    if web_service_availability is True:

        pre_process = svh.PreProcess()
        post_process = svh.PostProcess()

        # First return all datasets which you are available for you to query
        data = raw_content.list_all_datasets(conf.rest['entry_point']['list']['url'])
        processed_data = pre_process.response(data)
        # Check if user has access to ask for the list of datasets
        if processed_data['message'] == 'failure':
            print(' %s - Please check your "configuration.py"' % processed_data['data'])
            sys.exit(1)
        else:
            dataset_names = post_process.dataset_names(processed_data)
            print('This is extracting a subset of the data (i.e. available OSG datasets to query) %s ' % dataset_names)

            # Once the datasets are returned use them to run a query
            for dataset_name in dataset_names:
                post_data = {"query": {"dataset": dataset_name, "type": "full"}}
                data = raw_content.query_dataset(conf.rest['entry_point']['search']['url'], post_data)
                processed_data = pre_process.response(data)
                # Check whether user has access to query this dataset
                if processed_data['message'] == 'failure':
                    print(' %s ' % processed_data['data'])
                else:
                    print('This is data in a python structure %s ' % processed_data)


if __name__ == "__main__":
    main()

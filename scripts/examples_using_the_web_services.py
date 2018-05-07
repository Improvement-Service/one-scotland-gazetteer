from helpers import webservice as svh
from configuration import WebServices


def main():

    # Configuration to support OSG web services
    conf = WebServices()
    pre_process = svh.PreProcess()
    post_process = svh.PostProcess()

    content = svh.Content()

    # REST tests & examples #
    web_service_availability = content.test_description_language_availability(conf.rest['wadl'])

    if web_service_availability is True:

        # First return all datasets which you are available for you to query
        raw_data = content.list_all_datasets(conf.rest['services']['list']['url'])
        processed_data = pre_process.response(raw_data)
        dataset_names = post_process.dataset_names(processed_data)
        print('This is extracting a subset of the data (i.e. available OSG datasets to query) %s ' % dataset_names)

        # Once the datasets are returned use them to run a query
        for dataset_name in dataset_names:
            post_data = {"query": {"dataset": dataset_name, "type": "full"}}
            raw_data = content.query_dataset(conf.rest['services']['search']['url'], post_data)
            processed_data = pre_process.response(raw_data)
            print('This is data in a python structure %s ' % processed_data)



if __name__ == "__main__":
    main()

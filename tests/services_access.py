import service_helpers as svh
from configuration import WebServices


def main():

    o = svh.Content('dimitrios.michelakis', 'Hvdb@552')
    pre_process = svh.PreProcess()
    post_process = svh.PostProcess()
    c = WebServices()
    t = o.test_description_language_availability(c.rest['wadl'])

    if t is True:

        # Example - bring back all available datasets
        content = o.query_available_datasets(c.rest['services']['search']['url'],
                                             {"query":
                                                  {"dataset": "EST_STANDARD_SEARCH", "type": "full"}})
        pre_processed = pre_process.response(content)
        print(pre_processed)

        content = o.list_available_datasets(c.rest['services']['list']['url'])
        pre_processed = pre_process.response(content)
        post_processed = post_process.dataset_names(pre_processed)

if __name__ == "__main__":
    main()

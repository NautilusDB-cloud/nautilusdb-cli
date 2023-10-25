import os
import random
import unittest

from nautiluscli.api import delete_collection, create_collection, \
    list_collections, add_web_doc, add_doc


class TestApi(unittest.TestCase):
    def test_e2e_test(self):
        collection_name = "UT" + str(random.randint(1, 10000))
        DEMO_API_ENDPOINT = "https://b487hc1om1.execute-api.us-west-2.amazonaws.com/alpha"
        try:
            _, code, _ = create_collection(DEMO_API_ENDPOINT, collection_name)
            assert code == 200
            list_collections(DEMO_API_ENDPOINT)

            # Test succeess cases
            _, code, _ = add_web_doc(DEMO_API_ENDPOINT, collection_name,
                                     "https://s29.q4cdn.com/175625835/files/doc_downloads/test.pdf")
            assert code == 200
            test_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    "data/test.pdf"))
            _, code, _ = add_doc(DEMO_API_ENDPOINT, collection_name, test_pdf)
            assert code == 200

            # Try uploading a large file
            assert "exceeds size limit" in add_web_doc(DEMO_API_ENDPOINT,
                                                       collection_name,
                                                       "https://courses.csail.mit.edu/6.042/spring17/mcs.pdf")

            too_large = os.path.abspath(os.path.join(os.path.dirname(
                __file__), "data/too_large.pdf"))
            assert "exceeds size limit" in add_doc(DEMO_API_ENDPOINT,
                                                   collection_name,
                                                   too_large)
            # Try uploading invalid pdf
            too_large = os.path.abspath(os.path.join(os.path.dirname(
                __file__), "data/invalid.pdf"))
            _, code, _ = add_doc(DEMO_API_ENDPOINT, collection_name, too_large)
            assert code != 200
        finally:
            delete_collection(DEMO_API_ENDPOINT, collection_name)

import boto3
import logging
from django.conf import settings
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
)
from opensearchpy.helpers import bulk

from opensearch_manager.constants import DEFAULT_BULK_OPS_SETTINGS,DEFAULT_OS_INDEX_ALIAS_NAME

logger = logging.getLogger(__name__)

class OpensearchClient:
    def __init__(self):
        self.client = self.__get_opensearch_client()

    def __get_opensearch_client(self):
        host = settings.OPENSEARCH_HOST
        port = settings.OPENSEARCH_PORT

        if settings.OPENSEARCH_AUTH == "iam":
            region = settings.OPENSEARCH_REGION

            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAuth(credentials, region)

            client = OpenSearch(
                hosts=[f"{host}:{port}"],
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
            )
        else:
            auth = (
                "admin",
                "HappyFox@123"
            )
            client = OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=False,
                ssl_show_warn=False,
            )

        return client

    def create_index_template(self, name, template):
        response = self.client.indices.put_template(name, template)
        return response

    def create_index(self, index_name):
        response = self.client.indices.create(index_name)
        return response

    def delete_index(self, index_name):
        response = self.client.indices.delete(index_name)
        return response

    def close_index(self, index_name):
        response = self.client.indices.close(index=index_name)
        return response

    def open_index(self, index_name):
        response = self.client.indices.open(index_name)
        return response

    def does_index_exist(self, index_name):
        response = self.client.indices.exists(index_name)
        return response

    def create_alias(self, index_name, alias_name):
        response = self.client.indices.put_alias(index=index_name, name=alias_name)
        return response

    def delete_alias(self, index_name, alias_name):
        response = self.client.indices.delete_alias(index=index_name, name=alias_name)
        return response

    def get_alias(self, index_name, alias_name):
        response = self.client.indices.get_alias(index=index_name, name=alias_name)
        return response

    def exists_alias(self, index_name, alias_name):
        response = self.client.indices.exists_alias(index=index_name, name=alias_name)
        return response

    def update_index_for_alias(self, alias_name, old_index_name, new_index_name):
        response = self.client.indices.update_aliases(
            body={
                "actions": [
                    {"remove": {"index": old_index_name, "alias": alias_name}},
                    {"add": {"index": new_index_name, "alias": alias_name}},
                ]
            }
        )
        return response

    def index_document(self, index_name, doc_id, doc):
        response = self.client.index(index=index_name, id=doc_id, body=doc)
        return response

    def delete_document(self, index_name, doc_id):
        response = self.client.delete(index=index_name, id=doc_id)
        return response

    def search(self, index_name, query):
        response = self.client.search(index=index_name, body=query)
        return response

    def bulk_index(self, index_name, docs):
        """
        Bulk indexes multiple docs in an index.

        Parameters:

        index_name: Name of the index
        docs: a dictionary of documents with
        document id as key , and document content to
        be indexed as value.
        """
        actions = []
        for doc_id in docs.keys():
            index_action = {
                "_op_type": "index",
                "_index": index_name,
                "_id": doc_id,
            }
            index_action.update(docs[doc_id])
            actions.append(index_action)

        response = bulk(self.client, actions, **DEFAULT_BULK_OPS_SETTINGS)
        return response

    def bulk_delete(self, index_name: str, doc_ids: list):
        """
        Bulk deletes docs in a given index.
        """
        actions = []
        for doc_id in doc_ids:
            delete_action = {"_op_type": "delete", "_index": index_name, "_id": doc_id}
            actions.append(delete_action)

        response = bulk(self.client, actions, raise_on_error=False, **DEFAULT_BULK_OPS_SETTINGS)
        return response

    def get_document_ids_by_query(self, index_name, key, value):
        """
        Returns a list of document ids that match the given query.
        """
        doc_ids = []
        query = {"query": {"match": {key: value}}, "_source": ["_id"]}
        data = self.client.search(index=index_name, body=query, scroll="1m", size=1000)
        scroll_id = data["_scroll_id"]
        while len(data["hits"]["hits"]):
            doc_ids.extend([hit["_id"] for hit in data["hits"]["hits"]])
            data = self.client.scroll(scroll_id=scroll_id, scroll="1m")
            scroll_id = data["_scroll_id"]
        self.client.clear_scroll(scroll_id=scroll_id)
        return doc_ids

    def get_client(self):
        return self.client

    def get_endpoint(self):
        protocol = "http" if settings.DEBUG else "https"
        return f"{protocol}://{settings.OPENSEARCH_HOST}:{settings.OPENSEARCH_PORT}"

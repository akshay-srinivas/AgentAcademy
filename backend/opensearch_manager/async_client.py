import boto3
from django.conf import settings
from opensearchpy import (
    AsyncHttpConnection,
    AsyncOpenSearch,
    AWSV4SignerAsyncAuth,
)


class AsyncOpensearchClient:
    def __init__(self):
        self.client = self.__get_opensearch_client()

    def __get_opensearch_client(self):
        host = settings.OPENSEARCH_HOST
        port = settings.OPENSEARCH_PORT

        if settings.OPENSEARCH_AUTH == "iam":
            region = settings.OPENSEARCH_REGION

            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAsyncAuth(credentials, region)

            client = AsyncOpenSearch(
                hosts=[f"{host}:{port}"],
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=AsyncHttpConnection,
            )
        else:
            # client = AsyncOpenSearch(hosts=[{"host": host, "port": int(port)}])
            auth = (
                "admin",
                "HappyFox@123"
            )
            client = AsyncOpenSearch(
                hosts=[{"host": 'localhost', "port": 5000}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=False,
                ssl_show_warn=False,
            )

        return client

    def get_client(self):
        return self.client

    async def search(self, index_name, query):
        response = await self.client.search(index=index_name, body=query)
        return response

    async def close(self):
        await self.client.close()

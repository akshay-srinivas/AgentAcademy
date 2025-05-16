import requests
import logging
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Any
)

from bs4 import BeautifulSoup
from django.conf import settings
from llama_index.core import Document
from llama_index.core.readers.base import BasePydanticReader

from data_sources.models import DataSource
from pydantic import Field

from accounts.models import Account, AccountDetail

GET_ARTICLES_URL = "{BASE_URL}api/1.1/json/kb/articles/"
GET_SECTIONS_URL = "{BASE_URL}api/1.1/json/kb/sections/"

# logger = logging.getLogger(__name__)


BATCH_SIZE = 50



class HappyFoxHelpdeskKBReader(BasePydanticReader):
    """
    Custom reader for HappyFox Helpdesk KB Articles and Sections.
    """

    is_remote: bool = True
    headers: Dict[str, str]
    account: Any = Field(default=None, description="HappyFox account")
    base_url: str = Field(default="https://support.happyfox.com/")

    def __init__(
        self,
        account: Account,
        **kwargs,
    ):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        # Get base URL from account details
        base_url = "https://support.happyfox.com/"
        try:
            account_detail = AccountDetail.objects.get(account=account, key='happyfox_base_url')
            if hasattr(account_detail, 'value') and isinstance(account_detail.value, dict):
                base_url = account_detail.value.get('happyfox_base_url', base_url)
        except AccountDetail.DoesNotExist:
            # Use default base_url if account detail doesn't exist
            pass

        # Pass all required fields to the parent class constructor
        super().__init__(
            headers=headers,
            account=account,
            base_url=base_url,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        """Get the name identifier of the class."""
        return "HappyFoxHelpdeskKBReader"

    def _get_logging_context(self):
        return {
            "reader_class": self.class_name(),
        }

    def _get_document_for_article(self, article: dict):
        document_id = f"kb_{article['article_id']}"
        document = Document(
            text=article["article_text"],
            id_=document_id,
            metadata={
                "account_id": self.account.id,
                "article_id": article["article_id"],
                "parent_section_name": article["parent_section_name"],
                "article_tags": article["article_tags"],
                "category_ids": article["category_ids"],
                "article_url": article["article_url"],
                "article_title": article["article_title"],
                "source": "happyfox_helpdesk",
            },
        )
        return document

    def _get_article_text(self, article_html: str) -> str:
        article_text = BeautifulSoup(article_html, "lxml").get_text()
        return article_text

    @cached_property
    def articles_info(self):
        print("asdsaddasd", self.base_url)
        resp = requests.get(GET_SECTIONS_URL.format(BASE_URL=self.base_url))
        resp.raise_for_status()
        sections = resp.json()
        article_attachments = []
        resp = requests.get(GET_ARTICLES_URL.format(BASE_URL=self.base_url))
        resp.raise_for_status()
        articles = resp.json()

        print("sections",sections)

        section_id_section_map = {section["id"]: {"name":section['name'],"parent_section_name":section["parent_section_name"],"categories":section["categories"]} for section in sections}

        articles_info = []
        for article in articles:
            section_info = section_id_section_map.get(article["section_id"])
            article_info = {
                "article_id": article["id"],
                "article_title": article["title"],
                "section_name": section_info["name"],
                "parent_section_name": section_id_section_map[article["section_id"]]["parent_section_name"],
                "article_tags": article["tags"],
                "category_ids": section_info.get("categories", []),
                "article_url": article.get("full_url"), # TODO: FIX THIS
                "article_html": article["contents"],
                "article_text": self._get_article_text(article["contents"]),
            }
            print("article",article)
            articles_info.append(article_info)
        return articles_info, article_attachments

    def load_data(self, *args, **load_kwargs) -> Tuple[List[Document], List[int]]:
        documents = []
        for article_info in self.articles_info[0]:
            document = self._get_document_for_article(article_info)
            documents.append(document)

        return documents
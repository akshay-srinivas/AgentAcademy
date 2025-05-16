import logging

from bs4 import BeautifulSoup
from html2text import HTML2Text
from llama_index.core.schema import (
    Document,
    TransformComponent,
)

from chatbot.models import Bot
from core.llms.claude import get_claude_llm

logger = logging.getLogger(__name__)

ARTICLE_TOPIC_PROMPT = """
You are an AI Assistant working for {company_name} who works in the {domain} domain.

Here is some background information about the company:
<company_info>
{company_info}
</company_info>

You are an expert at understanding knowledge base articles and providing relevant information to the users.

Your task is to assign the most suitable topic(s) to the given article from the list of given topics.
Here are the topics that you can assign:
<topics>
    {topics}
</topics>

If the article does not match any of the topics, you can leave the fields empty.
Here is how you should respond:
<response>
    <topics_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the article</name>
            <id>ID of the topic assigned to the article</id>
        </topic_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the article</name>
            <id>ID of the topic assigned to the article</id>
        </topic_assigned>
    </topics_assigned>
</response>

Here is the KB article that you need to analyze:
<article>
    {article}
</article>

You must respond in the format mentioned above and nothing else.
While assigning topics, make sure to assign the most relevant ones.
If the article is not related to any of the given topics, you can leave the fields empty.
"""

# This will be used for both webpages and documents
CONTENT_TOPIC_PROMPT = """
You are an AI Assistant working for {company_name} who works in the {domain} domain.

Here is some background information about the company:
<company_info>
{company_info}
</company_info>

You are an expert at understanding the given knowledge and providing relevant information to the users.

Your task is to assign the most suitable topic(s) to the given knowledge/content from the list of given topics.
Here are the topics that you can assign:
<topics>
    {topics}
</topics>

If the given knowledge/content does not match any of the topics, you can leave the fields empty.
Here is how you should respond:
<response>
    <topics_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the knowledge/content</name>
            <id>ID of the topic assigned to the knowledge/content</id>
        </topic_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the knowledge/content</name>
            <id>ID of the topic assigned to the knowledge/content</id>
        </topic_assigned>
    </topics_assigned>
</response>

Here is the knowledge/content that you need to analyze:
<knowledge>
    {knowledge}
</knowledge>

You must respond in the format mentioned above and nothing else.
While assigning topics, make sure to assign the most relevant ones.
If the knowledge/content is not related to any of the given topics or products, you can leave the fields empty.
When you decide to assign a topic, make sure you always give the ID of the topic along with the name. Do not leave the ID field empty.
"""

CONTENT_TOPIC_AND_ENTITY_IDENTIFIER_PROMPT = """
You are an AI Assistant working for {company_name} who works in the {domain} domain.

Here is some background information about the company:
<company_info>
{company_info}
</company_info>

You are an expert at understanding the given knowledge and providing relevant information to the users.

Your task is to assign the most suitable topic(s) to the given knowledge/content from the list of given topics.
You also need to extract the {entities_to_extract} from the knowledge/content if any.
Here are the topics that you can assign:
<topics>
    {topics}
</topics>

{entities_available}

If the given knowledge/content does not match any of the topics, you can leave the fields empty.
Here is how you should respond:
<response>
    <topics_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the knowledge/content</name>
            <id>ID of the topic assigned to the knowledge/content</id>
        </topic_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the knowledge/content</name>
            <id>ID of the topic assigned to the knowledge/content</id>
        </topic_assigned>
    </topics_assigned>
    {entities_output}
</response>

Here is the knowledge/content that you need to analyze:
<knowledge>
    {knowledge}
</knowledge>

You must respond in the format mentioned above and nothing else.
While assigning topics, make sure to assign the most relevant ones.
If the article is not related to any of the given topics, you can leave the fields empty.
You should only assign entities if they are mentioned in the knowledge/content.
You should never make up entities. It should be extracted from the knowledge/content.
"""

CONTENT_TOPIC_AND_PRODUCT_METADATA_PROMPT = """
You are an AI Assistant working for {company_name} who works in the {domain} domain.

Here is some background information about the company:
<company_info>
{company_info}
</company_info>

You are an expert at understanding the given knowledge and providing relevant information to the users.

Your task is to assign the most suitable topic(s) to the given knowledge/content from the list of given topics.
You also need to extract the product metadata from the knowledge/content if any.
What do we mean by product metadata?
1. Extract one or more product names mentioned in the content, if any.
2. Identify if the article is talking about a product or an entire product family.
3. If the article is talking about a product family, extract the name of the product family.
4. If the article is generic and not talking about any product or product family, you can leave the fields empty,
and set <does_article_talk_about_product> and <does_article_talk_about_product_family> to "No".
Here are the topics that you can assign:
<topics>
    {topics}
</topics>

If the given knowledge/content does not match any of the topics, you can leave the fields empty.
Here is how you should respond:
<response>
    <topics_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the knowledge/content</name>
            <id>ID of the topic assigned to the knowledge/content</id>
        </topic_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the knowledge/content</name>
            <id>ID of the topic assigned to the knowledge/content</id>
        </topic_assigned>
    </topics_assigned>
    <products_identified>
        <product>Product name</product>
        <product>Product name</product>
    </products_identified>
    <product_families_identified>
        <product_family>Product family name</product_family>
        <product_family>Product family name</product_family>
    </product_families_identified>
    <does_article_talk_about_product>Yes/No</does_article_talk_about_product>
    <does_article_talk_about_product_family>Yes/No</does_article_talk_about_product_family>
</response>

Here is the knowledge/content that you need to analyze:
<knowledge>
    {knowledge}
</knowledge>

You must respond in the format mentioned above and nothing else.
While assigning topics, make sure to assign the most relevant ones.
If the article is not related to any of the given topics, you can leave the fields empty.
You should only assign product names or family if they are mentioned in the knowledge/content.
You should never make up product names or families. It should be extracted from the knowledge/content.
"""

ARTICLE_TOPIC_PRODUCT_METADATA_PROMPT = """
You are an AI Assistant working for {company_name} who works in the {domain} domain.
Here is some background information about the company:
<company_info>
{company_info}
</company_info>
You are an expert at understanding knowledge base articles and providing relevant information to the users.
Your task is to assign the most suitable topic(s) to the given article from the list of given topics.
and also extract the product metadata from the article if any.
What do we mean by product metadata?
1. Extract one or more product names mentioned in the article, if any.
2. Identify if the article is talking about a product or an entire product family.
3. If the article is talking about a product family, extract the name of the product family.
4. If the article is generic and not talking about any product or product family, you can leave the fields empty,
and set <does_article_talk_about_product> and <does_article_talk_about_product_family> to "No".
Here are the topics that you can assign:
<topics>
    {topics}
</topics>
If the article does not match any of the topics, you can leave the fields empty.
Here is how you should respond:
<response>
    <topics_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the article</name>
            <id>ID of the topic assigned to the article</id>
        </topic_assigned>
        <topic_assigned>
            <name>Name of the topic assigned to the article</name>
            <id>ID of the topic assigned to the article</id>
        </topic_assigned>
    </topics_assigned>
    <products_identified>
        <product>Product name</product>
        <product>Product name</product>
    </products_identified>
    <product_families_identified>
        <product_family>Product family name</product_family>
        <product_family>Product family name</product_family>
    </product_families_identified>
    <does_article_talk_about_product>Yes/No</does_article_talk_about_product>
    <does_article_talk_about_product_family>Yes/No</does_article_talk_about_product_family>
</response>
Here is the KB article that you need to analyze:
<article>
    {article}
</article>
You must respond in the format mentioned above and nothing else.
While assigning topics, make sure to assign the most relevant ones.
If the article is not related to any of the given topics, you can leave the fields empty.
You should only assign product names or family if they are mentioned in the article.
You should never make up product names or families. It should be extracted from the article.
"""


class TagTopicsTransformComponent(TransformComponent):
    bot: Bot
    topics: list

    def __init__(self, bot: Bot, **kwargs):
        super().__init__(bot=bot, topics=bot.topics)

    def _get_article_context(self, node: Document) -> str:
        article_context_str = f"""
            <title> {node.metadata["article_title"]} </title>
            <content> {node.text} </content>
            <section_hierarchy> {node.metadata["section_hierarchy"]} </section_hierarchy>
            <article_tags> {node.metadata["article_tags"]} </article_tags>
        """

        return article_context_str

    def _get_topics_context(self) -> str:
        topic_context_str = ""
        for topic in self.topics:
            topic_context_str += f"""
            <topic>
                <topic_id> {topic['id']} </topic_id>
                <topic_name> {topic['name']} </topic_name>
                <description> {topic['description']} </description>
            </topic>
            """
        return topic_context_str

    def _get_topic(self, node: Document) -> tuple:
        topic_context_str = self._get_topics_context()
        article_context_str = self._get_article_context(node)
        company_info = self.bot.settings["company_info"]
        company_name = self.bot.settings["company_name"]

        prompt = ARTICLE_TOPIC_PROMPT.format(
            topics=topic_context_str,
            article=article_context_str,
            company_info=company_info,
            company_name=company_name,
            domain=self.bot.domain,
        )
        claude_llm = get_claude_llm()
        response = claude_llm.complete(prompt)
        soup = BeautifulSoup(response.text, "html.parser")
        topic_ids_assigned = [int(topic.find("id").text) for topic in soup.find_all("topic_assigned")]

        return topic_ids_assigned

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            topic_ids = self._get_topic(node)
            node.metadata[f"{self.bot.embed_token}__topic_ids"] = topic_ids

        return nodes


class TagTopicsForContentTransformComponent(TransformComponent):
    topics: list
    bot: Bot

    def __init__(self, bot: Bot, **kwargs):
        super().__init__(
            bot=bot,
            topics=bot.topics,
        )

    def _get_node_context(self, node: Document) -> str:
        context_str = f"""
            <content> {node.text} </content>
        """

        return context_str

    def _get_topics_context(self) -> str:
        topic_context_str = ""
        for topic in self.topics:
            topic_context_str += f"""
            <topic>
                <topic_id> {topic['id']} </topic_id>
                <topic_name> {topic['name']} </topic_name>
                <description> {topic['description']} </description>
            </topic>
            """
        return topic_context_str

    def _get_topic(self, node: Document) -> tuple:
        topic_context_str = self._get_topics_context()
        context_str = self._get_node_context(node)

        company_info = self.bot.settings["company_info"]
        company_name = self.bot.settings["company_name"]
        prompt = CONTENT_TOPIC_PROMPT.format(
            topics=topic_context_str,
            knowledge=context_str,
            company_info=company_info,
            company_name=company_name,
            domain=self.bot.domain,
        )
        claude_llm = get_claude_llm()
        response = claude_llm.complete(prompt)
        soup = BeautifulSoup(response.text, "html.parser")
        topic_ids_assigned = [int(topic.find("id").text) for topic in soup.find_all("topic_assigned")]

        return topic_ids_assigned

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            topic_ids = self._get_topic(node)
            node.metadata[f"{self.bot.embed_token}__topic_ids"] = topic_ids
        return nodes


class TagTopicsAndEntityTransformComponent(TransformComponent):
    topics: list
    bot: Bot

    def __init__(self, bot: Bot, **kwargs):
        super().__init__(
            bot=bot,
            topics=bot.topics,
        )

    def _get_node_context(self, node: Document) -> str:
        context_str = f"""
            <title> {node.metadata.get("title")} </title>
            <content> {node.text} </content>
        """

        return context_str

    def _get_topics_context(self) -> str:
        topic_context_str = ""
        for topic in self.topics:
            topic_context_str += f"""
            <topic>
                <topic_id> {topic['id']} </topic_id>
                <topic_name> {topic['name']} </topic_name>
                <description> {topic['description']} </description>
            </topic>
            """
        return topic_context_str

    def _get_entities_context(self) -> str:
        entities_to_extract = self.bot.settings.get("entities_to_extract", [])
        entities_available = self.bot.settings.get("entities_available", {})

        entities_to_extract_str = ", ".join([entity_to_extract["name"] for entity_to_extract in entities_to_extract])
        entities_available_str = ""
        for entity, available_entities in entities_available.items():
            entities_available_str += f"""
            Here are the some known {entity} that you can extract:
            <{entity}>
            {"".join([f"<id>{available_entity['id']}</id><name>{available_entity['name']}</name>" for available_entity in available_entities])}
            </{entity}>\n\n
            """

        entities_output = ""
        for entity in entities_to_extract:
            entities_output += f"""
            <{entity["name"]}s>
                <{entity["name"]}>
                    <id>entity_id</id>
                </{entity["name"]}>
                <{entity["name"]}>
                    <id>entity_id</id>
                </{entity["name"]}>
            </{entity["name"]}s>
            """

        return entities_output, entities_to_extract_str, entities_available_str

    def _get_topic_and_entities(self, node: Document) -> tuple:
        topic_context_str = self._get_topics_context()
        context_str = self._get_node_context(node)
        entities_output, entities_to_extract_str, entities_available_str = self._get_entities_context()

        company_info = self.bot.settings["company_info"]
        company_name = self.bot.settings["company_name"]
        prompt = CONTENT_TOPIC_AND_ENTITY_IDENTIFIER_PROMPT.format(
            topics=topic_context_str,
            knowledge=context_str,
            company_info=company_info,
            company_name=company_name,
            domain=self.bot.domain,
            entities_output=entities_output,
            entities_to_extract=entities_to_extract_str,
            entities_available=entities_available_str,
        )
        claude_llm = get_claude_llm()
        response = claude_llm.complete(prompt)
        soup = BeautifulSoup(response.text, "html.parser")
        topic_ids_assigned = (
            [int(topic.find("id").text) for topic in soup.find_all("topic_assigned")]
            if soup.find("topic_assigned")
            else []
        )
        entity_ids = []
        entities_to_extract = self.bot.settings.get("entities_to_extract", [])
        for entity in entities_to_extract:
            entity_ids.extend([entity.find("id").text for entity in soup.find_all(f"{entity['name']}")])

        logger.info(f"Topic IDs assigned: {topic_ids_assigned}")
        logger.info(f"Entity IDs assigned: {entity_ids}")

        return topic_ids_assigned, entity_ids

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            topic_ids, entities = self._get_topic_and_entities(node)
            node.metadata[f"{self.bot.embed_token}__topic_ids"] = topic_ids
            node.metadata["entities"] = entities
        return nodes


class ConvertHTMLToMD(TransformComponent):
    def __get_md(self, node: Document) -> str:
        """
        Convert HTML text to markdown text.
        :param html_text: HTML text to be converted to markdown.
        :return: Markdown text.
        """
        handler = HTML2Text()
        # Refer https://github.com/Alir3z4/html2text/blob/master/docs/usage.md
        # for configurations used below.
        handler.body_width = 0  # To avoid word wrapping
        handler.inline_links = True
        handler.use_automatic_links = False
        return handler.handle(node.text)

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            node.set_content(self.__get_md(node))
        return nodes


class TagTopicsAndProductMetadataTransformComponent(TransformComponent):
    bot: Bot
    topics: list

    def __init__(self, bot: Bot, **kwargs):
        super().__init__(bot=bot, topics=bot.topics)

    def _get_article_context(self, node: Document) -> str:
        article_context_str = f"""
            <title> {node.metadata["article_title"]} </title>
            <content> {node.text} </content>
            <section_hierarchy> {node.metadata["section_hierarchy"]} </section_hierarchy>
            <article_tags> {node.metadata["article_tags"]} </article_tags>
        """

        return article_context_str

    def _get_topics_context(self) -> str:
        topic_context_str = ""
        for topic in self.topics:
            topic_context_str += f"""
            <topic>
                <topic_id> {topic['id']} </topic_id>
                <topic_name> {topic['name']} </topic_name>
                <description> {topic['description']} </description>
            </topic>
            """
        return topic_context_str

    def _get_topics_and_product_metadata(self, node: Document) -> tuple:
        topic_context_str = self._get_topics_context()
        article_context_str = self._get_article_context(node)
        company_info = self.bot.settings["company_info"]
        company_name = self.bot.settings["company_name"]

        prompt = ARTICLE_TOPIC_PRODUCT_METADATA_PROMPT.format(
            topics=topic_context_str,
            article=article_context_str,
            company_info=company_info,
            company_name=company_name,
            domain=self.bot.domain,
        )
        claude_llm = get_claude_llm()
        response = claude_llm.complete(prompt)
        soup = BeautifulSoup(response.text, "lxml")
        topic_ids_assigned = [int(topic.find("id").text) for topic in soup.find_all("topic_assigned")]
        is_article_about_product = soup.find("does_article_talk_about_product").text
        is_article_about_product_family = soup.find("does_article_talk_about_product_family").text
        products = []
        product_families = []
        if is_article_about_product.lower().strip() == "yes":
            products = [product.text for product in soup.find_all("product")]
        if is_article_about_product_family.lower().strip() == "yes":
            product_families = [product_family.text for product_family in soup.find_all("product_family")]

        logger.info(f"Topic IDs assigned: {topic_ids_assigned}")
        logger.info(f"Products identified: {products}")
        logger.info(f"Product families identified: {product_families}")

        return topic_ids_assigned, products, product_families

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            topic_ids, products, product_families = self._get_topics_and_product_metadata(node)
            node.metadata[f"{self.bot.embed_token}__topic_ids"] = topic_ids
            node.metadata["identified_products"] = products
            node.metadata["identified_product_families"] = product_families

        return nodes


class TagTopicsAndProductMetadataForHappyfoxAttachmentTransformComponent(TransformComponent):
    topics: list
    bot: Bot

    def __init__(self, bot: Bot, **kwargs):
        super().__init__(
            bot=bot,
            topics=bot.topics,
        )

    def _get_node_context(self, node: Document) -> str:
        context_str = f"""
            <article_title> {node.metadata["article_title"]} </article_title>
            <section_name> {node.metadata["parent_section_name"]} </section_name>
            <section_hierarchy> {node.metadata["section_hierarchy"]} </section_hierarchy>
            <content> {node.text} </content>
        """

        return context_str

    def _get_topics_context(self) -> str:
        topic_context_str = ""
        for topic in self.topics:
            topic_context_str += f"""
            <topic>
                <topic_id> {topic['id']} </topic_id>
                <topic_name> {topic['name']} </topic_name>
                <description> {topic['description']} </description>
            </topic>
            """
        return topic_context_str

    def _get_topic_and_product_metadata(self, node: Document) -> tuple:
        topic_context_str = self._get_topics_context()
        context_str = self._get_node_context(node)

        company_info = self.bot.settings["company_info"]
        company_name = self.bot.settings["company_name"]
        prompt = CONTENT_TOPIC_AND_PRODUCT_METADATA_PROMPT.format(
            topics=topic_context_str,
            knowledge=context_str,
            company_info=company_info,
            company_name=company_name,
            domain=self.bot.domain,
        )
        claude_llm = get_claude_llm()
        response = claude_llm.complete(prompt)
        soup = BeautifulSoup(response.text, "html.parser")
        topic_ids_assigned = [int(topic.find("id").text) for topic in soup.find_all("topic_assigned")]
        topic_ids_assigned = [int(topic.find("id").text) for topic in soup.find_all("topic_assigned")]
        is_article_about_product = soup.find("does_article_talk_about_product").text
        is_article_about_product_family = soup.find("does_article_talk_about_product_family").text
        products = []
        product_families = []
        if is_article_about_product.lower().strip() == "yes":
            products = [product.text for product in soup.find_all("product")]
        if is_article_about_product_family.lower().strip() == "yes":
            product_families = [product_family.text for product_family in soup.find_all("product_family")]

        logger.info(f"Topic IDs assigned: {topic_ids_assigned}")
        logger.info(f"Products identified: {products}")
        logger.info(f"Product families identified: {product_families}")

        return topic_ids_assigned, products, product_families

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            topic_ids, products, product_families = self._get_topic_and_product_metadata(node)
            node.metadata[f"{self.bot.embed_token}__topic_ids"] = topic_ids
            node.metadata["identified_products"] = products
            node.metadata["identified_product_families"] = product_families
        return nodes

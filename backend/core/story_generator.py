from openai import OpenAI
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from core.prompts import STORY_PROMPT
from core.config import settings
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
from dotenv import load_dotenv
import logging

load_dotenv()
print("Open Router Key:", settings.OPENAI_API_KEY)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(
            model="mistralai/mistral-7b-instruct",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.7,
            max_retries=3,
            timeout=30,
        )

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fabulous") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"create the story with this theme: {theme}"
            ),
        ]).partial(format_instructions=story_parser.get_format_instructions())
        chain = prompt | llm | story_parser
        story_structure = chain.invoke({})

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()
        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        content = node_data.content if isinstance(
            node_data, StoryNodeLLM) else node_data["content"]
        is_ending = node_data.isEnding if isinstance(
            node_data, StoryNodeLLM) else node_data["isEnding"]
        is_winning = node_data.isWinningEnding if isinstance(
            node_data, StoryNodeLLM) else node_data["isWinningEnding"]
        node = StoryNode(
            story_id=story_id,
            content=content,
            is_root=is_root,
            is_ending=is_ending,
            is_winning_ending=is_winning,
            options=[]
        )
        db.add(node)
        db.flush()
        if not node.is_ending:
            options_data = node_data.options if isinstance(
                node_data, StoryNodeLLM) else node_data.get("options", [])
            options_list = []
            for option_data in options_data:
                next_node = option_data.nextNode
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)
                    child_node = cls._process_story_node(
                        db, story_id, next_node)
                    options_list.append({
                        "text": option_data.text,
                        "node_id": child_node.id
                    })
            node.options = options_list
            db.flush()
        return node

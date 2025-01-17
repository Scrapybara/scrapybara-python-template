from scrapybara import Scrapybara
from scrapybara.anthropic import Anthropic
from scrapybara.tools import ComputerTool, BashTool, EditTool, BrowserTool
from scrapybara.prompts import SYSTEM_PROMPT
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def main():
    # Initialize client
    client = Scrapybara(api_key=os.getenv("SCRAPYBARA_API_KEY"))
    instance = client.start()
    instance.browser.start()

    try:
        # Define schema
        class HNSchema(BaseModel):
            class Post(BaseModel):
                title: str
                url: str
                points: int

            posts: List[Post]

        # Execute action
        response = client.act(
            model=Anthropic(),
            tools=[
                BashTool(instance),
                ComputerTool(instance),
                EditTool(instance),
                BrowserTool(instance),
            ],
            system=SYSTEM_PROMPT,
            prompt="Get the top 10 posts on Hacker News",
            schema=HNSchema,
            on_step=lambda step: print(step.text),
        )

        # Access structured output
        posts = response.output.posts
        print(posts)

    finally:
        # Cleanup
        instance.browser.stop()
        instance.stop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")

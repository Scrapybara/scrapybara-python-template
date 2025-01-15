from scrapybara import Scrapybara
from scrapybara.anthropic import Anthropic
from scrapybara.tools import ComputerTool, BashTool, EditTool, BrowserTool
from scrapybara.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
import os
load_dotenv()

client = Scrapybara(api_key=os.getenv("SCRAPYBARA_API_KEY"))
instance = client.start()

try:
    instance.browser.start()
    messages = client.act(
        tools=[
            ComputerTool(instance),
            BashTool(instance),
            EditTool(instance),
            BrowserTool(instance)
        ],
        model=Anthropic(),
        system=SYSTEM_PROMPT,
        prompt=f"There is a browser open on the screen (you can take ss to confirm). Go to scrapybara.com and tell me what you see.",
    )

    print(messages[-1].content[0].text)

except Exception as e:
    print(e)
    instance.stop()

finally:
    instance.stop()
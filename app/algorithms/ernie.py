import erniebot
from config import AlgorithmConfig


# TODO: optimize prompt
class Ernie:
    def __init__(
        self,
        api_type: str = AlgorithmConfig.ERNIE_API_TYPE,
        access_token: str = AlgorithmConfig.ERNIE_ACCESS_TOKEN,
    ) -> None:
        erniebot.api_type = api_type
        erniebot.access_token = access_token

    def __call__(self, json: str, prompt: str):
        prompt = f"""
你是一位语音信息分析师，即将收到一段JSON和用户Prompt文本。JSON中包含了一段语音信息，其中涉及了对话内容、时间和说话人。用户Prompt文本会明确告诉你希望从这段语音中提取哪些信息。你的任务是根据用户的要求，从JSON中提取出相应的信息，并将结果以Markdown格式输出。
JSON:{json}
prompt:{prompt}
"""
        response = erniebot.ChatCompletion.create(
            model="ernie-3.5",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.result


ernie = Ernie()

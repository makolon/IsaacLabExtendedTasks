import json
from typing import Callable, Dict, List


class LLMManager:
    def __init__(self, config):
        self.config = config
        # Initialize openai client
        client = openai.OpenAI(api_key=openapi_key)

        # Generate system & user prompt for action planning
        sys_prompt = create_sys_prompt(sys_prompt_ap_template)
        usr_prompt = create_usr_prompt(prompt=usr_prompt_ap_template)
        print("System Prompt: ", sys_prompt)
        print("User Prompt: ", usr_prompt)
        input("[INFO] Check the prompts and press Enter to Continue...")

    def query(
        self,
        client: Callable,
        engine: str,
        system_prompt: str,
        user_prompt: str,
        verbose: bool = False
    ) -> List[Dict[str, str]]:
        # Query LLM for an plan
        response = client.chat.completions.create(
            model=engine,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            max_tokens=2000,
            temperature=0,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Parse the response
        try:
            response_data = response.choices[0].message.content
            start = response_data.find("```json\n") + len("```json\n")
            end = response_data.find("\n```", start)
            json_text = response_data[start:end]
            results = json.loads(json_text)
        except Exception as e:
            print(f"Failed to parse response: {e}")
            return []
            
        return results
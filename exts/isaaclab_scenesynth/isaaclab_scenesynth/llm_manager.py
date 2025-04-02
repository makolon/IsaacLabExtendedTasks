import openai
import yaml
import json
from pathlib import Path
from omegaconf import DictConfig
from typing import List, Dict, Tuple


class LLMManager:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.api_key = self.load_openai_config(self.cfg.api_key_file)
        self.client = openai.OpenAI(api_key=self.api_key)
        self.engine = self.cfg.engine
        self.prompt_dir = Path(self.cfg.prompt_dir)

    def load_prompt(self, filename: str) -> str:
        lib_path = Path(__file__).resolve().parent
        prompt_path = lib_path / self.prompt_dir / filename
        with prompt_path.open('r', encoding='utf-8') as f:
            return f.read()

    def load_openai_config(self, file_name: str) -> Tuple[str]:
        """
        Load OpenAI configuration from a YAML file.

        Args:
            file_name (str): Name of the configuration file.

        Returns:
            Tuple[str]: OpenAI key from the configuration file.
        """
        # Construct the file path using pathlib
        lib_path = Path(__file__).resolve().parent.parent.parent.parent
        file_path = lib_path / "scripts" / "configs" / file_name
        
        # Load the YAML configuration file
        with file_path.open("r") as f:
            openai_cfg = yaml.safe_load(f)
        
        # Return the OpenAI key
        return openai_cfg.get("key")

    def query_asset_types(self, scene_description: str, available_asset: List[str]) -> List[str]:
        """
        Ask the LLM to determine which asset types are needed in the scene,
        constrained by the available asset types defined in the procedural assets module.
        """
        system_prompt = "You are a helpful assistant for 3D scene understanding."

        # Load prompt template from file
        user_prompt_template = self.load_prompt("asset_types_prompt.txt")

        # Fill in the template with the scene description and available asset types
        user_prompt = user_prompt_template.format(
            scene_description=scene_description,
            available_assets=", ".join(available_asset)
        )

        # Send request to LLM and parse the returned JSON list
        response = self._chat(system_prompt, user_prompt)
        return json.loads(response)

    def query_asset_instances(self, asset_types: List[str], required_args_map: Dict[str, List[str]]) -> List[Dict]:
        system_prompt = "You are a 3D scene asset generator."
        asset_type_str = ", ".join(asset_types)
        type_description_str = "\n".join(
            f'For "{atype}", provide: {", ".join(args)}'
            for atype, args in required_args_map.items()
        )

        user_prompt_template = self.load_prompt("asset_instances_prompt.txt")
        user_prompt = user_prompt_template.format(
            asset_types=asset_type_str,
            type_descriptions=type_description_str,
        )
        response = self._chat(system_prompt, user_prompt)
        print("LLM response:", response)
        return json.loads(response)

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a chat completion request to the LLM and extracts the raw JSON content.
        Supports both plain JSON and responses wrapped in ```json blocks.
        """
        response = self.client.chat.completions.create(
            model=self.engine,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=3000,
            temperature=0,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        content = response.choices[0].message.content.strip()

        # Try to extract just the JSON content
        try:
            # If content is wrapped like ```json\n...\n```, remove it
            if content.startswith("```json"):
                start = content.find("```json") + len("```json")
                end = content.rfind("```")
                json_text = content[start:end].strip()
            else:
                # Find the first and last JSON delimiters
                start = content.find("[") if "[" in content else content.find("{")
                end = content.rfind("]") + 1 if "]" in content else content.rfind("}") + 1
                json_text = content[start:end]
            return json_text
        except Exception as e:
            print(f"Failed to extract JSON from response: {e}")
            raise

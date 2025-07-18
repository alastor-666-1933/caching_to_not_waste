import os
import yaml
import random
import re

class caching_wildcard_list:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "each_line": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "wildcard_file": ("STRING", {"default": "xray.yaml"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("modified_text",)
    FUNCTION     = "replace_lines"
    CATEGORY     = "caching_to_not_wast"

    @staticmethod
    def IS_CHANGED(*args, **kwargs):
        return float("NaN")

    def load_yaml(self, wildcard_file):
        # Sobe para a raiz do ComfyUI
        comfy_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        yaml_path = os.path.join(comfy_path, "wildcards", wildcard_file)
        if not os.path.isfile(yaml_path):
            raise FileNotFoundError(f"File YAML '{wildcard_file}' not found: {yaml_path}")
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_from_yaml(self, path, yaml_data, last_values):
        parts = path.split("/")
        ref = yaml_data

        try:
            for p in parts:
                ref = ref[p]

            if isinstance(ref, list):
                valid_choices = [v for v in ref if v is not None and v != "" and v != "null"]

                if not valid_choices:
                    return ""

                if len(valid_choices) == 1:
                    chosen = valid_choices[0]
                else:
                    previous = last_values.get(path)
                    choices = valid_choices.copy()

                    if previous in choices:
                        choices.remove(previous)

                    chosen = random.choice(choices)

                last_values[path] = chosen
            else:
                chosen = ref
                last_values[path] = chosen

            # 👇 Aqui entra o código novo para tratar {a|b|c}
            if isinstance(chosen, str):
                pattern = r"\{([^{}]+)\}"
                while re.search(pattern, chosen):
                    chosen = re.sub(pattern, lambda m: random.choice(m.group(1).split("|")), chosen)
            elif chosen is None:
                return ""
            else:
                chosen = str(chosen)

            return "" if chosen == "null" else str(chosen)

        except (KeyError, TypeError):
            return f"__{path}__"

    def replace_lines(self, each_line, wildcard_file):
        print(f"[DEBUG] Executando replace_lines com force_random={each_line}")
        yaml_data = self.load_yaml(wildcard_file)

        lines = each_line.strip().splitlines()
        output_lines = []

        pattern = r"__([a-zA-Z0-9_/]+)__"
        last_values = {}
        max_depth = 10  # Limite de segurança para recursividade

        for line in lines:
            depth = 0
            while re.search(pattern, line) and depth < max_depth:
                matches = re.findall(pattern, line)
                for match in matches:
                    replacement = self.get_from_yaml(match, yaml_data, last_values)
                    # Mesmo que o wildcard não seja encontrado, ele será substituído por si mesmo
                    line = line.replace(f"__{match}__", replacement)
                depth += 1
            output_lines.append(line)

        return ("\n".join(output_lines),)


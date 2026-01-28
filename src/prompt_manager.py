class PromptManager:
    def __init__(self, template_path):
        self.template_path = template_path
        self.template = self._load_template()

    def _load_template(self):
        try:
            with open(self.template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Prompt template file not found at {self.template_path}")
            return ""

    def get_prompt(self, **kwargs):
        """
        Returns the formatted prompt string.
        Args:
            **kwargs: Key-value pairs to substitute in the template.
        """
        # Basic substitution logic. Can be extended to use Jinja2 if needed.
        # For now, it just returns the text if no variables are in it.
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            print(f"Warning: Missing key for prompt substitution: {e}")
            return self.template

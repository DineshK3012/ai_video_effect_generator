class ModelRegistry:
    """
    Registry for Gemini "Nano Banana" model aliases and configuration.
    Separates model selection logic from the main application flow.
    """
    
    # Model Constants
    NANO_BANANA = "gemini-2.5-flash-image"          # Optimized for speed/efficiency
    NANO_BANANA_PRO = "gemini-3-pro-image-preview"  # Optimized for professional asset production
    
    @classmethod
    def get_best_model(cls):
        """
        Returns the model ID for the highest quality interactions (Nano Banana Pro).
        Usage: For complex instructions, high fidelity, and reasoning.
        """
        print(f"Selected Best Model: Nano Banana Pro ({cls.NANO_BANANA_PRO})")
        return cls.NANO_BANANA_PRO

    @classmethod
    def get_efficient_model(cls):
        """
        Returns the model ID for high-efficiency interactions (Nano Banana).
        Usage: For high volume, low latency tasks.
        """
        print(f"Selected Efficient Model: Nano Banana ({cls.NANO_BANANA})")
        return cls.NANO_BANANA

    @classmethod
    def resolve_model(cls, choice):
        """
        Resolves a user string to the correct model ID.
        """
        choice = choice.lower().replace(" ", "_")
        if choice in ["nano_banana", "flash"]:
            return cls.NANO_BANANA
        if choice in ["nano_banana_pro", "pro", "best"]:
            return cls.NANO_BANANA_PRO
        return choice

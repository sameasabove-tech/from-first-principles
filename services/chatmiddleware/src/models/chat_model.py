import os

import google.generativeai as genai
from dotenv import load_dotenv  # Import load_dotenv


load_dotenv()  # Load environment variables from .env file


def get_model(
    api_key, model_name="gemini-1.5-flash", safety_settings=None, system_prompt=None
):
    """
    Configures the Generative AI API and returns a GenerativeModel instance.

    Args:
        api_key: Your Google Cloud Generative AI API key.
        model_name: The name of the model to use (default: "gemini-1.5-flash").
        safety_settings: A list of SafetySetting objects to configure content filtering.
        system_prompt: A string containing the system-level prompt for the model.

    Returns:
        A GenerativeModel instance, or None if configuration fails.
        Raises an exception if the model name is invalid or configuration fails.
    """
    try:
        genai.configure(api_key=api_key)
        generation_config = {}
        if system_prompt:
            generation_config["system_instruction"] = system_prompt
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        print(f"Error getting model: {e}")
        raise  # Re-raise the exception
        return None


# Example usage:
if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual API key

    system_prompt = "You are a helpful and harmless AI assistant."

    try:
        model = get_model(api_key)
        if model:
            response = model.generate_content("Tell me a joke.")
            print(response.text)

        # Example without safety settings and system prompt:
        model_no_safety = get_model(api_key)
        if model_no_safety:
            response = model_no_safety.generate_content("Tell me a joke.")
            print("Response without safety settings:", response.text)

        # Example of invalid model name
        invalid_model = get_model(
            api_key, model_name="invalid-model"
        )  # this will raise an exception
    except Exception as e:
        print(f"Main program caught an exception: {e}")

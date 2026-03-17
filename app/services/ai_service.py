from openai import OpenAI
from config.settings import Config

# Initialize client only if API key is provided, else we handle it gracefully below
if Config.OPENROUTER_API_KEY and Config.OPENROUTER_API_KEY != 'your_openrouter_api_key_here':
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=Config.OPENROUTER_API_KEY,
        default_headers={
            "HTTP-Referer": Config.SITE_URL,
            "X-OpenRouter-Title": Config.SITE_NAME,
        }
    )
else:
    client = None

def generate_content(topic, tone, word_count, keywords):
    """Generates content using OpenAI API."""
    keywords_str = ", ".join(keywords) if keywords else "None"
    
    prompt = f"""
    Write a {tone} article or content piece about '{topic}'.
    The length should be approximately {word_count} words.
    Please ensure the following keywords are naturally included: {keywords_str}.
    
    The content should be well-structured and engaging.
    """
    
    if not client:
        # Mock behavior for testing if API key is missing
        return f"[MOCK GPT] Generated {tone} content about '{topic}' (~{word_count} words). Included keywords: {keywords_str}."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional content writer and SEO expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=min(int(word_count * 1.5) + 100, 2000)
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in OpenAI generation: {e}")
        raise e

def summarize_content(text, max_length):
    """Summarizes text using OpenAI API."""
    prompt = f"""
    Please provide a concise summary of the following text.
    The summary should be roughly {max_length} words long.
    
    Original text:
    {text}
    """
    
    if not client:
        return f"[MOCK GPT SUMMARY] Summarized text approximately {max_length} words long."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at summarizing long texts concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=max_length * 2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in OpenAI summarization: {e}")
        raise e

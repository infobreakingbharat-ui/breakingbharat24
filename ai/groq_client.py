from groq import Groq
import config


client = Groq(
    api_key=config.GROQ_API_KEY
)


def ask_groq(prompt, temperature=0.5):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=temperature

    )

    return response.choices[0].message.content.strip()
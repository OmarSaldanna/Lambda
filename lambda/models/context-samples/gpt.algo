from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Eres una IA capaz de extraer información en formato json"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Basado en el siguiente esquema de memoria:\n\n\"members\": {\n\t\t\"servers\": [],\n\t\t\"role\": \"free\",\n\t\t\"usage\": {\n\t\t\t\"budget\": 1,\n\t\t\t\"images\": 10\n\t\t},\n\t\t\"file\": \"\",\n\t\t\"voice\": \"echo\",\n\t\t\"memory\": \"\",\n\t\t\"credentials\": {\n\t\t\t\"hint\": \"\",\n\t\t\t\"hash\": \"\"\n\t\t},\n\t\t\"models\": {\n\t\t\t\"chat\": \"gpt-4o-mini\",\n\t\t\t\"intelligence\": \"claude-3-5-sonnet-20240620\",\n\t\t\t\"research\": \"gemini-1.5-flash\",\n\t\t\t\"vision\": \"gemini-1.5-flash\"\n\t\t},\n\t\t\"devices\": {},\n\t\t\"personality\": \"Eres una IA asistente\",\n\t\t\"context_len\": 0,\n\t\t\"context\": []\n\t}\n\nQuiero que ajustes a que el contexto ya es de 120, cambies la personalidad a Eres una IA capaz de extraer información en formato json, el modelo de chat a gemini-1.5-flash y el rol lo cambies a pro"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "{\"members\":{\"servers\":[],\"role\":\"pro\",\"usage\":{\"budget\":1,\"images\":10},\"file\":\"\",\"voice\":\"echo\",\"memory\":\"\",\"credentials\":{\"hint\":\"\",\"hash\":\"\"},\"models\":{\"chat\":\"gemini-1.5-flash\",\"intelligence\":\"claude-3-5-sonnet-20240620\",\"research\":\"gemini-1.5-flash\",\"vision\":\"gemini-1.5-flash\"},\"devices\":{},\"personality\":\"Eres una IA capaz de extraer información en formato json\",\"context_len\":120,\"context\":[]}}"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw.........AAAASUVORK5CYII="
          }
        },
        {
          "type": "text",
          "text": "Ahora convierte el contenido de esta imagen a un json"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "{\n  \"messages\": [\n    {\n      \"role\": \"system\",\n      \"content\": \"You are a helpful assistant.\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"Hello!\"\n    },\n    {\n      \"role\": \"system\",\n      \"content\": \"What can I help you with?\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": [\n        {\n          \"type\": \"text\",\n          \"text\": \"What's in this image?\"\n        },\n        {\n          \"type\": \"image_url\",\n          \"image_url\": \"https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg\"\n        }\n      ]\n    }\n  ]\n}"
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
    "type": "json_object"
  }
)
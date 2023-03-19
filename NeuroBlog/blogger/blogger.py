import openai
import json
import requests
from PIL import Image
from io import BytesIO

OPENAI_API_KEY = "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"

# Текст, который будет использоваться для генерации изображения
text = 'Knight in the future, digitalart'

# Установка ключа API
openai.api_key = OPENAI_API_KEY

# Определение параметров запроса
prompt = (f"Сгенерируйте среднего размера пост на любую тему для блога в формате JSON:\n"
          f"title: \"\",\n"
          f"description: \"\",\n"
          f"content: \"\",\n"
          f"tags: \n"
          f"Заполните все поля. Тэги должны перечисляться через запятую")
model = "text-davinci-003"
temperature = 0.5
max_tokens = 3880


def create_text():
    # Отправка запроса и получение ответа
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Обработка ответа и вывод результата в формате JSON
    post_text = response.choices[0].text.strip()
    # post_data = json.loads(f"{{ {post_text} }}")
    # json_data = json.dumps(post_data, ensure_ascii=False, indent=4)
    return post_text


def create_picture(text_to_image):
    import requests

    url = "https://img4me.p.rapidapi.com/"

    querystring = {"text": "Test Me", "font": "trebuchet", "size": "12", "fcolor": "000000", "bcolor": "FFFFFF",
                   "type": "png"}

    headers = {
        "X-RapidAPI-Key": "9b95a6308bmsh2ce3dd5ca89920cp111f87jsna396b8fece96",
        "X-RapidAPI-Host": "img4me.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

    # Получение URL изображения из ответа
    # image_url = response.json()['data'][0]['url']
    image_url = response['output_url']

    # Загрузка изображения по URL
    image_response = requests.get(image_url)
    image_data = BytesIO(image_response.content)

    # Открытие изображения с помощью библиотеки PIL
    image = Image.open(image_data)

    # Отображение сгенерированного изображения
    image.show()


text = create_text()
print(text)
# create_picture(text[0])


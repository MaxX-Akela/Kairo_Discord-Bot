import disnake
from disnake.ext import commands
import requests
import json
import base64
import time

API_URL = 'https://api-key.fusionbrain.ai/' # https://fusionbrain.ai Login and get API_KEY and SECRET_KEY
API_KEY = 'API_KEY'
SECRET_KEY = 'SECRET_KEY'

class GenerateCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Генерация изображения при помощи нейросетей")
    async def generate(self, inter: disnake.ApplicationCommandInteraction, prompt: str):
        # Уведомляем о том, что запрос обрабатывается
        await inter.response.defer(ephemeral=True)  # Используем defer для ожидания

        if not prompt:
            await inter.edit_original_message(content='Пожалуйста, предоставьте описание для генерации изображения.')
            return

        model_id = self.get_model()
        uuid = self.generate_image(prompt, model_id)
        images = self.check_generation(uuid)

        if images:
            image_data = images[0]
            with open('generated_image.png', 'wb') as img_file:
                img_file.write(base64.b64decode(image_data))
            with open('generated_image.png', 'rb') as img_file:
                # Изменяем оригинальное сообщение на изображение
                await inter.edit_original_message(content='Вот ваше сгенерированное изображение:', 
                                                   file=disnake.File(img_file, 'generated_image.png'))
        else:
            await inter.edit_original_message(content='Не удалось сгенерировать изображение.')

    def get_model(self):
        response = requests.get(API_URL + 'key/api/v1/models', headers={
            'X-Key': f'Key {API_KEY}',
            'X-Secret': f'Secret {SECRET_KEY}',
        })
        data = response.json()
        return data[0]['id']

    def generate_image(self, prompt, model_id, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt}
        }
        data = {
            'model_id': (None, model_id),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(API_URL + 'key/api/v1/text2image/run', headers={
            'X-Key': f'Key {API_KEY}',
            'X-Secret': f'Secret {SECRET_KEY}',
        }, files=data)
        return response.json()['uuid']

    def check_generation(self, uuid, attempts=10, delay=10):
        for _ in range(attempts):
            response = requests.get(API_URL + f'key/api/v1/text2image/status/{uuid}', headers={
                'X-Key': f'Key {API_KEY}',
                'X-Secret': f'Secret {SECRET_KEY}',
            })
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            time.sleep(delay)
        return None
    
def setup(bot: commands.Bot):
    bot.add_cog(GenerateCommand(bot))

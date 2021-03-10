import logging
import os

import telegram
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest

from recipes.models import Content, Ingredient


def adding_ingredients_to_recipe(recipe, form):
    input_ingredients = form.cleaned_data.get('ingredients')
    try:
        with transaction.atomic():
            recipe.save()
            ingredients_for_recipe = []
            for key in input_ingredients.keys():
                ingredients_for_recipe.append(
                    Content(ingredient=Ingredient.objects.get(title=key),
                            amount=input_ingredients[key], recipe=recipe))
            Content.objects.bulk_create(ingredients_for_recipe)

        form.save_m2m()
        return recipe

    except IntegrityError:
        return HttpResponseBadRequest


class TelegramBotHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.token = os.environ['TELEGRAM_TOKEN']
        self.chat_id = os.environ['CHAT_ID']

    def emit(self, record):
        bot = telegram.Bot(self.token)
        bot.send_message(self.chat_id, self.format(record))


def send_message(request):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = TelegramBotHandler()
    logger.addHandler(handler)
    user_agent = request.META.get('HTTP_USER_AGENT')
    user_ip = request.META.get('REMOTE_ADDR')
    logger.debug(
        f'{request.user} came to the server with {user_agent} from {user_ip}')

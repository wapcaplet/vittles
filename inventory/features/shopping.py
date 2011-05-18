#from django.core.exceptions import ObjectDoesNotExist
from lettuce import step, world
from core.models import Food, Unit
from inventory.models import Place


def get_or_create(model, **attrs):
    obj, created = model.objects.get_or_create(**attrs)
    return obj


@step('I have an empty shopping list')
def have_empty_shopping_list(step):
    world.shopping_list = get_or_create(Place, name='shopping list')
    world.shopping_list.provisions.clear()


@step('I add "(.+)" to my shopping list')
def add_to_shopping_list(step, item):
    food = get_or_create(Food, name=item)
    world.shopping_list.provisions.create(food=food)


@step('I have a pantry containing:')
def have_in_pantry(step):
    world.pantry = get_or_create(Place, name='pantry')
    world.pantry.provisions.clear()

    # Add each item to the pantry
    for item in step.hashes:
        world.pantry.provisions.create(
            food = get_or_create(Food, name=item['food']),
            quantity = float(item['qty']),
            unit = get_or_create(Unit, name=item['unit']),
        )

@step('my shopping list should include:')
def shopping_list_should_include(step):
    for item in step.hashes:


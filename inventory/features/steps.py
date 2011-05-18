#from django.core.exceptions import ObjectDoesNotExist
from lettuce import step, world
from core.models import Food, Unit
from inventory.models import ShoppingList, Provision


def get_or_create(model, **attrs):
    obj, created = model.objects.get_or_create(**attrs)
    return obj


@step('I have an empty shopping list')
def have_empty_shopping_list(step):
    world.shopping_list = get_or_create(ShoppingList, name='groceries')
    world.shopping_list.foods.clear()


@step('I add "(.+)" to my shopping list')
def add_to_shopping_list(step, item):
    food = get_or_create(Food, name=item)
    world.shopping_list.foods.add(food)


@step('I have these provisions:')
def have_provisions(step):
    # Remove all provisions
    Provision.objects.all().delete()

    # Add each provision
    for item in step.hashes:
        Provision.objects.create(
            food = get_or_create(Food, name=item['food']),
            quantity = float(item['qty']),
            unit = get_or_create(Unit, name=item['unit']),
        )

@step('my shopping list should include:')
def shopping_list_should_include(step):
    items = [food.name for food in world.shopping_list.foods.all()]
    for item in step.hashes:
        if item['food'] not in items:
            raise Exception("'%s' not found in '%s'" % (item['food'], str(items)))



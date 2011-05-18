from django.core.exceptions import ObjectDoesNotExist
from lettuce import step, world
from core.models import Food
from inventory.models import Place, Provision

@step('I have an empty shopping list')
def have_empty_shopping_list(step):
    try:
        world.shopping_list = Place.objects.get(name='shopping list')
    except ObjectDoesNotExist:
        world.shopping_list = Place.objects.create(name='shopping list')
    else:
        # TODO: Ensure the shopping list is cleared
        pass



@step('I add "(.+)" to my shopping list')
def add_to_shopping_list(step, item):
    try:
        food = Food.objects.get(name=item)
    except ObjectDoesNotExist:
        food = Food.objects.create(name=item)
    world.shopping_list.provisions.create(food=food)


@step('I have the following in my pantry:')
def have_in_pantry(step):
    # Do something with each row
    for data in step.hashes:
        pass
    raise Exception("Uh oh")


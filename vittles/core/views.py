from core.models import Food, Unit
from django.core import serializers
from django.http import HttpResponse

def foods(request):
    json = serializers.get_serializer('json')()
    items = json.serialize(Food.objects.all(), ensure_ascii=False)
    return HttpResponse(items, mimetype='application/json')


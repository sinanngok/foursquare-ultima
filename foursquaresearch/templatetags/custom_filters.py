from django import template

from foursquaresearch.models import Favorite, Place

from accounts.models import MyUser as User

register = template.Library()

@register.filter(name='is_place_in_favorites')
def is_place_in_favorites(foursquare_id, arg):
    user_id = arg
    user = User.objects.get(id=user_id)
    obj = Place.objects.filter(foursquare_id=foursquare_id)
    print (obj)
    favorite_exist = Favorite.objects.filter(user=user, place=obj).exists()
    if favorite_exist:
        return True
    else:
        return False
    #favorite_exist = Favorite.objects.filter(user=user, place=obj).exists()
    #if favorite_exist:
    #    return True
    #else:
    #    return False
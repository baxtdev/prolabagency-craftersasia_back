from apps.store.models import Item,ItemViews

from django.utils import timezone

class InfoItem:
    def __init__(self,item):
        self.item:Item = item
    @property
    def order_count(self):
        return self.item.orders.count()
    @property
    def favorite_count(self):
        return self.item.favorites.count()
    @property
    def review_count(self):
        return self.item.reviews.filter(quality__gte=2).count()
    @property
    def raiting(self):
        total = [self.order_count,self.favorite_count,self.review_count]
        return {'item':self.item,'raiting':sum(total)}
    


class PopularItem:
    def __init__(self) -> None:
        self.items:set = Item.objects.all()
    @property
    def info_items(self):
        data = [InfoItem(x).raiting for x in self.items]
        return data



class ChekPopularItem:
    def __init__(self) -> None:
        self.items:set = Item.objects.all()
    def average_views_value(self):
        views = [value.views.all().count() for value in self.items]
        
        try :
            return sum(views)/len(views)    
        
        except ZeroDivisionError:
            return 0

    def chek_items_to_popular(self):
        try:
            for item in self.items:
                if item.views.all().filter(timestamp=timezone.now().today()).count() > self.average_views_value():
                    item.is_popular = True
                else:
                    item.is_popular = False
                item.save()
            return "Completed"    
        
        except Exception as e:
            return f"Error: {e}"
            
    def chek_item_to_popular(self,id:int):
        try:
            item:Item = self.items.get(id=id)
            if item.views.all().count() >=self.average_views_value():
                return True
            else:
                return False
        except item.DoesNotExist:
            raise(f"Обьект с такой 'id={id}' не существует ")    
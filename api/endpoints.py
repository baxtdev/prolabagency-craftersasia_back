from rest_framework import routers
from django.urls import include, path

from .yasg import urlpatterns as url_doc
from .auth.endpoints import urlpatterns as auth_urls
from .users.endpoints import urlpatterns as users_urls
from .companies.endpoints import urlpatterns as companies_urls
from .store.endpoints import urlpatterns as store_urls
from .order.endpoints import urlpatterns as order_urls
from .chat.endpoints import urlpatterns as cha_urls
urlpatterns=[
    path('accounts/', include(auth_urls)),
    path('',include(users_urls)),
    path('',include(companies_urls)),
    path('', include(store_urls)),
    path('', include(order_urls)),
    path('chat/',include(cha_urls))
]

urlpatterns+=url_doc
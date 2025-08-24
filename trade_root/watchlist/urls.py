from django.urls import path

# views
from .views import WatchListAPI , WatchListCreateAPI , WatchListAdd , WatchListRemove

urlpatterns = [
    path('', WatchListAPI.as_view(), name="list-watchlist"),
    path('create',WatchListCreateAPI.as_view(), name="create-watchlist"),
    path('<int:id>/add',WatchListAdd.as_view(), name="add-to-watchlist"),
    path('<int:id>/remove',WatchListRemove.as_view(), name="remove-from-watchlist"),
]
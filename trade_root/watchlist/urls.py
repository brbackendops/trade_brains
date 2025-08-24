from django.urls import path

# views
from .views import WatchListAPI , WatchListCreateAPI , WatchListAdd , WatchListRemove

urlpatterns = [
    path('watchlist/', WatchListAPI.as_view(), name="list-watchlist"),
    path('watchlist/create',WatchListCreateAPI.as_view(), name="create-watchlist"),
    path('watchlist/<int:id>/add',WatchListAdd.as_view(), name="add-to-watchlist"),
    path('watchlist/<int:id>/remove',WatchListRemove.as_view(), name="remove-from-watchlist"),
]
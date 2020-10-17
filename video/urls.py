from django.urls import path
from video.views import AddVideo, AllVideosListView, CategoryVideoList, VideoDetailView, UpdateVideoView, \
    VideoDeleteView, MostPopularVideosListView

app_name = 'video'

# todo: ZROBIĆ LINK DLA VIDEO ZE SLUGIEM.

urlpatterns = [

    path('all/', AllVideosListView.as_view(), name='all_videos_list'),
    path('show/<int:pk>/<slug:slug>', VideoDetailView.as_view(), name='video_detail'),
    path('category/<slug:slug>/', CategoryVideoList.as_view(), name='category_videos_list'),
    path('add/', AddVideo.as_view(), name='add_video'),
    path('edit/<int:pk>/<slug:slug>', UpdateVideoView.as_view(), name='update_video'),
    path('delete/<int:pk>/<slug:slug>', VideoDeleteView.as_view(), name='delete_video'),

    path('most_popular/', MostPopularVideosListView.as_view(), name='most_popular_videos'),

    ]

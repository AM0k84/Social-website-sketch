from django.urls import path
from video.views import AddVideo, AllVideosListView, CategoryVideoList, VideoDetailView, UpdateVideoView, \
    VideoDeleteView, MostPopularVideosListView, PromotedVideosView, MostPopularPromotedVideosView

app_name = 'video'

# todo: ZROBIĆ LINK DLA VIDEO ZE SLUGIEM.

urlpatterns = [

    path('add/', AddVideo.as_view(), name='add_video'),
    path('edit/<int:pk>/<slug:slug>', UpdateVideoView.as_view(), name='update_video'),
    path('delete/<int:pk>/<slug:slug>', VideoDeleteView.as_view(), name='delete_video'),

    path('show/<int:pk>/<slug:slug>', VideoDetailView.as_view(), name='video_detail'),

    path('category/<slug:slug>/', CategoryVideoList.as_view(), name='category_videos_list'),
    path('all/', AllVideosListView.as_view(), name='all_videos_list'),
    path('trending/', MostPopularVideosListView.as_view(), name='trending'),

    path('promoted/', PromotedVideosView.as_view(), name='promoted_videos'),
    path('hot/', MostPopularPromotedVideosView.as_view(), name='hot_promoted_videos'),

    ]

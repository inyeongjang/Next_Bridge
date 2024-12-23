from django.urls import path
from django.contrib.auth import views as auth_views
from common.views import account_views, profile_views

app_name = 'common'

urlpatterns = [
    # account_views.py
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('signup/', account_views.signup, name='signup'),

    # profile_views.py
    # 프로필
    path('profile/base/<int:user_id>/', profile_views.profile_base, name='profile_base'),
    path('profile/base/<int:user_id>/edit/', profile_views.profile_edit, name='profile_edit'),
    path('profile/question/<int:user_id>/', profile_views.ProfileQuestionListView.as_view(), name='profile_question'),
    path('profile/answer/<int:user_id>/', profile_views.ProfileAnswerListView.as_view(), name='profile_answer'),
    path('profile/comment/<int:user_id>/', profile_views.ProfileCommentListView.as_view(), name='profile_comment'),
    path('profile/vote/<int:user_id>/', profile_views.ProfileVoteListView.as_view(), name='profile_vote'),
]
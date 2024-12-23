from django.urls import path
from reviews.views import base_views, review_views

app_name = 'reviews'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
    path('list/', base_views.review_list, name='review_list'),
    path('list/<int:review_id>/', base_views.review_detail, name='review_detail'),
    path('company/<int:company_id>/', base_views.company_reviews, name='company_reviews'), # 회사 리뷰 목록
    path('autocomplete/', base_views.company_autocomplete, name='company_autocomplete'), # (리뷰 작성에서) 회사 검색
    path('company_search/', base_views.company_search, name='company_search'),  # (메인화면에서) 회사 검색_검색 API 추가


    # review_views.py
    path('create/', review_views.review_create, name='review_create'),
    path('modify/<int:review_id>/', review_views.review_modify, name='review_modify'),
    path('delete/<int:review_id>/', review_views.review_delete, name='review_delete'),
    path('vote/<int:review_id>/', review_views.review_vote, name='review_vote'),

]
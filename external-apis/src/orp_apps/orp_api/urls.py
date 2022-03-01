"""Urls module for the orp_api app."""

# Third Party
from django.urls import path

# Project
from orp_apps.orp_api import views

urlpatterns = [
    path('', views.APIRoot.as_view(), name='api-root'),
    path('taxonomies/', views.TaxonomyListView.as_view(), name='taxonomy-list'),
    path('taxonomies/<int:id>/', views.TaxonomyDetailView.as_view(), name='taxonomy-detail'),
    path(
        'taxonomies/<int:id>/categories/',
        views.CategoryListView.as_view(),
        name='categories-list'
    ),
    path(
        'taxonomies/<int:id>/categories/<int:category_id>/',
        views.CategoryDetailView.as_view(),
        name='category-detail'
    ),
    path('documents/', views.DocumentListView.as_view(), name='document-list'),
    path(
        'documents_with_outstanding_feedback/',
        views.DocumentOutstandingFeedbackList.as_view(),
        name='document-outstanding-feedback-list'
    ),
    path(
        'documents_with_completed_feedback/',
        views.DocumentCompletedFeedbackList.as_view(),
        name='document-completed-feedback-list'
    ),
    path('documents/<int:id>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path(
        'documents/<int:id>/<str:event_type>/',
        views.RevisionSubscriptionView.as_view(),
        name='document-detail-subscriptions'
    ),
    path(
        'documents/search/<str:id_list>/',
        views.DocumentListSearchView.as_view(),
        name='document-search-list'
    ),
    path('entities/', views.EntityListView.as_view(), name='entity-list'),
    path('entities/<int:id>/', views.EntityDetailView.as_view(), name='entity-detail'),
    path(
        'entities/<int:id>/documents/',
        views.EntityDetailView.as_view(),
        name='entity-documents'
    ),
    path(
        'search/',
        views.DocumentSearch.as_view(),
        name='search-documents'
    ),
    path(
        'graph/',
        views.DocumentGraphSearch.as_view(),
        name='graph-documents'
    ),
    path(
        'subscription_event_types/',
        views.SubscriptionEventTypesView.as_view(),
        name='subscription-event-list'
    ),
]

from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('workspaces', views.WorkspacesViewSet, basename='workspaces')

workspaces_router = routers.NestedDefaultRouter(
    router, 'workspaces', lookup='workspace')
workspaces_router.register('users', views.WorkspacesUsersViewSet,
                          basename='workspace-users')

# URLConf
urlpatterns = router.urls + workspaces_router.urls
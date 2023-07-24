from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .permissions import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status, permissions
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class WorkspacesViewSet(ModelViewSet):
    queryset = Workspaces.objects.all()
    serializer_class = WorkspacesSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Workspaces.objects.all()
        elif user.is_staff:
            return Workspaces.objects.filter(admin=user).all()
        else:
            # Step 1: Retrieve workspaces associated with the user
            workspaces_user_belongs_to = WorkspacesUsers.objects.filter(user=user)

            # Step 2: Get the list of workspace IDs for the user
            workspace_ids = workspaces_user_belongs_to.values_list('workspace__id', flat=True)

            # Step 3: Use the list of workspace IDs to filter the Workspaces queryset
            return Workspaces.objects.filter(id__in=workspace_ids)
    
    def create(self, request, *args, **kwargs):
        serializer = WorkspacesSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(admin=request.user)  # Set the authenticated user as the admin
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, instance, validated_data):
        # Exclude 'admin' from the validated_data during update
        admin = validated_data.pop('admin', None)

        # Perform the regular update
        instance = super().update(instance, validated_data)

        return instance

    def delete(self, request, pk):
        workspaces = get_object_or_404(Workspaces, pk=pk)
        
        # Check if the authenticated user is the admin of the workspace
        if workspaces.admin == self.request.user:
            workspaces.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("you are not admin", status=status.HTTP_400_BAD_REQUEST)



class WorkspacesUsersViewSet(ModelViewSet):
    serializer_class = WorkspacesUsersSerializer
    
    def get_permissions(self):
        return [IsAdminOrReadOnly()]
        
    def get_queryset(self):
         return WorkspacesUsers.objects.filter(workspace_id=self.kwargs['workspace_pk'])
    
    # def create(self, request, *args, **kwargs):
    #     # Get the workspace ID from the URL
    #     workspace_id = self.kwargs['workspace_pk']

    #     # Add the workspace ID to the request data
    #     request.data['workspace'] = workspace_id

    #     # Create the serializer with the modified request data
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

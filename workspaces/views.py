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

# Create your views here.
class WorkspacesViewSet(ModelViewSet):
    queryset = Workspaces.objects.all()
    serializer_class = WorkspacesSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Workspaces.objects.all()
        return Workspaces.objects.filter(admin=user).all()
    
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
            return Response({'error': 'You are not authorized to delete this workspace.'}, status=status.HTTP_403_FORBIDDEN)


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

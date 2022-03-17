from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Publisher, Author, Book
from .serializers import PublisherSerializer, AuthorSerializer, BookSerializer
from .authentication import TokenAuthentication


class PublisherView(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        try:
            publisher = self.get_object(pk=pk)
            serializer = PublisherSerializer(publisher, many=False)
            return Response(serializer.data)
        except Publisher.DoesNotExist:
            raise Http404

    def list(self, request):
        name_param = request.query_params.get('name')
        publishers = []

        if name_param is None:
            publishers = Publisher.objects.all()
        else:
            publishers = Publisher.objects.filter(
                name__icontains=name_param)

        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        publisher = self.get_object(pk=pk)
        serializer = PublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        publisher = self.get_object(pk=pk)
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return Publisher.objects.get(pk=pk)
        except Publisher.DoesNotExist:
            raise Http404

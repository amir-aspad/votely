from rest_framework import views, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

# import from django
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

# import from vote app
from .serializers import(
    ListingPollSerializer, PollActionSerializer,
    DetailPollSerializer
)
from .permissions import IsOwner
from .models import Poll

# import from utils
from utils.pagination import CustomPageNumberPagination


class ListingAllPollView(views.APIView):
    def get(self, request):
        search = request.query_params.get('search')

        all_polls = Poll.config.all()
        if search:
            # Filter polls by matching title and description with the search term.
            all_polls = all_polls.filter(
                Q(title__contains=search) | Q(description__contains=search)
            )

        paginate = CustomPageNumberPagination()
        result_page = paginate.paginate_queryset(all_polls, request)
        data = ListingPollSerializer(result_page, many=True)

        return paginate.get_paginated_response(data.data)


class PollViewSet(viewsets.ViewSet):
    permission_classes = (IsOwner,)
    
    def retrieve(self, request, pk=None):
        poll_found = Poll.config.filter(pk=pk).annotate(count=Count('votes__user')).first()
        if not poll_found:
            raise NotFound(detail='Poll not found')
        
        ser_data = DetailPollSerializer(instance=poll_found)
        return Response(ser_data.data)

    def destroy(self, request, pk=None):
        poll_found = get_object_or_404(Poll.config, pk=pk)

        self.check_object_permissions(request, poll_found)

        poll_found.delete()
        return Response({'detail':'poll deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        ser_data = PollActionSerializer(data=request.data, context={'request': request})

        if ser_data.is_valid():
            ser_data.save()

            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        poll_found = get_object_or_404(Poll.config, pk=pk)
        ser_data = PollActionSerializer(
            data=request.data,
            instance=poll_found,
            partial=True
        )

        if ser_data.is_valid():
            self.check_object_permissions(request, poll_found)
            ser_data.save()

            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

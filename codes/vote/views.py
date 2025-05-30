from rest_framework.response import Response
from rest_framework import views, status
from rest_framework import permissions

# import from django
from django.db.models import Count

# import from vote app
from .serializers import(
    ListingPollSerializer, PollActionSerializer
)
from .models import Poll

# import from utils
from utils.pagination import CustomPageNumberPagination


class ListingAllPollView(views.APIView):
    def get(self, request):
        search = request.query_params.get('search')

        all_polls = Poll.config.all().annotate(count=Count('votes__user'))
        if search:
            # Filter polls by matching title and description with the search term.
            all_polls = all_polls.filter(title__contains=search, description__contains=search)

        paginate = CustomPageNumberPagination()
        result_page = paginate.paginate_queryset(all_polls, request)
        data = ListingPollSerializer(result_page, many=True)

        return paginate.get_paginated_response(data.data)
    

class CreatePollView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser_data = PollActionSerializer(data=request.data, context={'request':request})

        if ser_data.is_valid():
            ser_data.save()

            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
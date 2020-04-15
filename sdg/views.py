from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import EstimatorSerializer, EstimatorResponseSerializer, RequestSerializer,\
    ResponseSerializer
from .lib.estimator_file import estimator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from silk.models import Response as silk_response, Request
import json


class EstimatorView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EstimatorSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs,):
        try:
            output_format = args[0]
            print(output_format)
        except IndexError:
            output_format = 'json'

        serializer = EstimatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        estimator_response = estimator(request.data)

        if output_format == 'json':
            rendered_data = JSONRenderer().render(estimator_response)
        elif output_format == 'xml':
            rendered_data = XMLRenderer().render(estimator_response)
        else:
            rendered_data = {"error": "Unsupported output format"}
        return Response(rendered_data, status=status.HTTP_200_OK)


class LogView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        query_1 = silk_response.objects.all()
        response_serializer = ResponseSerializer(query_1, many=True)

        query_2 = Request.objects.all()
        request_serializer = RequestSerializer(query_2, many=True)

        response_string = ''

        for request, response in zip(request_serializer.data, response_serializer.data):
            if request['time_taken'] is not None:
                response_string += str(request['method']) + '    ' + str(request['path']) + '    ' \
                                   + str(response['status_code']) + '    ' + \
                                   str(request['time_taken']) + '\n'

        print(response_string)
        return Response(response_string, status=status.HTTP_200_OK)

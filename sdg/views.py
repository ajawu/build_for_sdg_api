from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import EstimatorSerializer, RequestSerializer, ResponseSerializer
from .lib.estimator_file import estimator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_xml.renderers import XMLRenderer
from silk.models import Response as silkResponse, Request
from django.http import Http404


class EstimatorView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EstimatorSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs,):
        try:
            output_format = str(args[0])
            print(output_format)
        except IndexError:
            output_format = 'json'

        serializer = EstimatorSerializer(data=request.data)
        if serializer.is_valid():
            estimator_response = estimator(request.data)

            if output_format == 'json':
                return Response(estimator_response, status=status.HTTP_200_OK,
                                content_type='application/json')
            elif output_format == 'xml':
                rendered_data = XMLRenderer().render(estimator_response)
                return Response(rendered_data, status=status.HTTP_200_OK,
                                content_type='text/xml')
            else:
                raise Http404('Unsupported format')
        else:
            return Response({}, status=status.HTTP_200_OK, content_type='application/json')


class LogView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        query_1 = silkResponse.objects.all()
        response_serializer = ResponseSerializer(query_1, many=True).data

        query_2 = Request.objects.all()
        request_serializer = RequestSerializer(query_2, many=True).data

        response_string = "\n".join([str(request["method"]) + "    " + str(request["path"])
                                     + "    "
                                     + str(response["status_code"]) + "    " +
                                     str(request["time_taken"]) + "ms" for request, response in
                                     zip(request_serializer, response_serializer)])

        return Response(response_string, status=status.HTTP_200_OK, content_type='text/plain')

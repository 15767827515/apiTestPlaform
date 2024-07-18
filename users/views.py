from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView


class LoginView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        row_result=serializer.validated_data
        result_dict={}
        result_dict["token"]=row_result["access"]
        result_dict["refresh"]=row_result["refresh"]

        return Response(result_dict, status=status.HTTP_200_OK)

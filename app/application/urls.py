from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI

from app.application.shemas import PingResponseSchema
from app.application.api.urls import router as v1_router

api = NinjaAPI()

@api.get('/ping', response=PingResponseSchema)
def ping(request: HttpRequest) -> PingResponseSchema:
    return PingResponseSchema(result=True)

api.add_router('v1/', v1_router)

urlpatterns = [
    path("", api.urls),
]
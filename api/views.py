from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from . import models, serializers


class HelloWorldView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        return Response({"message": "Hello, World!"})


class CarouselImageView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        carousel_images = models.CarouselImage.objects.all()
        serializer = serializers.CarouselImageSerializer(carousel_images, many=True)
        return Response(serializer.data)

    @classmethod
    def get_serializer_class(cls):
        return serializers.CarouselImageSerializer


class RegionView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        regions = models.Region.objects.all()
        serializer = serializers.RegionSerializer(regions, many=True)
        return Response({"regions": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.RegionSerializer


class DiskView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        disks = models.Disk.objects.all()
        serializer = serializers.DiskSerializer(disks, many=True)
        return Response({"disks": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.DiskSerializer


class BandView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        bands = models.Band.objects.all()
        serializer = serializers.BandSerializer(bands, many=True)
        return Response({"bands": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.BandSerializer


class MoleculeView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        molecules = models.Molecule.objects.all()
        serializer = serializers.MoleculeSerializer(molecules, many=True)
        return Response({"molecules": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.MoleculeSerializer


class DataView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        data = models.Data.objects.all()
        serializer = serializers.DataSerializer(data, many=True)
        return Response({"data": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.DataSerializer

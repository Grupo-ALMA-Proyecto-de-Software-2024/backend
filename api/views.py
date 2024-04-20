from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from . import models
from .serializers import compact_serializers, full_context_serializers


class HelloWorldView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        return Response({"message": "Hello, World!"})


class CarouselImageView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        carousel_images = models.CarouselImage.objects.all()
        serializer = compact_serializers.CarouselImageSerializer(
            carousel_images, many=True
        )
        return Response(serializer.data)

    @classmethod
    def get_serializer_class(cls):
        return compact_serializers.CarouselImageSerializer


class RegionView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        regions = models.Region.objects.all()
        serializer = full_context_serializers.FullContextRegionSerializer(
            regions, many=True
        )
        return Response({"regions": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextRegionSerializer


class DiskView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        disks = models.Disk.objects.select_related("region").all()
        serializer = full_context_serializers.FullContextDiskSerializer(
            disks, many=True
        )
        return Response({"disks": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextDiskSerializer


class BandView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        bands = models.Band.objects.select_related("disk__region").all()
        serializer = full_context_serializers.FullContextBandSerializer(
            bands, many=True
        )
        return Response({"bands": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextBandSerializer


class MoleculeView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        molecules = models.Molecule.objects.select_related("band__disk__region").all()
        serializer = full_context_serializers.FullContextMoleculeSerializer(
            molecules, many=True
        )
        return Response({"molecules": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextMoleculeSerializer


class DataView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        data = models.Data.objects.select_related("molecule__band__disk__region").all()
        serializer = full_context_serializers.FullContextDataSerializer(data, many=True)
        return Response({"data": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextDataSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from . import models
from .serializers import compact_serializers, full_context_serializers


def build_openapi_parameters(names: list[str]) -> list[OpenApiParameter]:
    return [
        OpenApiParameter(
            name=name,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=f"Filter by {name}",
            required=False,
        )
        for name in names
    ]


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
    @extend_schema(
        tags=["API"],
        parameters=build_openapi_parameters(["region"]),
    )
    def get(self, request):
        regions = models.Region.objects.all()
        if region := request.query_params.get("region"):
            regions = regions.filter(name=region)
        serializer = full_context_serializers.FullContextRegionSerializer(
            regions, many=True
        )
        return Response({"regions": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextRegionSerializer


class DiskView(APIView):
    @extend_schema(
        tags=["API"],
        parameters=build_openapi_parameters(["region", "disk"]),
    )
    def get(self, request):
        disks = models.Disk.filter_disks(
            name=request.query_params.get("disk"),
            region=request.query_params.get("region"),
        )
        serializer = full_context_serializers.FullContextDiskSerializer(
            disks, many=True
        )
        return Response({"disks": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextDiskSerializer


class BandView(APIView):
    @extend_schema(
        tags=["API"],
        parameters=build_openapi_parameters(["region", "disk", "band"]),
    )
    def get(self, request):
        bands = models.Band.filter_bands(
            name=request.query_params.get("band"),
            disk=request.query_params.get("disk"),
            region=request.query_params.get("region"),
        )
        serializer = full_context_serializers.FullContextBandSerializer(
            bands, many=True
        )
        return Response({"bands": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextBandSerializer


class MoleculeView(APIView):
    @extend_schema(
        tags=["API"],
        parameters=build_openapi_parameters(["region", "disk", "band", "molecule"]),
    )
    def get(self, request):
        molecules = models.Molecule.filter_molecules(
            name=request.query_params.get("molecule"),
            band=request.query_params.get("band"),
            disk=request.query_params.get("disk"),
            region=request.query_params.get("region"),
        )
        serializer = full_context_serializers.FullContextMoleculeSerializer(
            molecules, many=True
        )
        return Response({"molecules": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextMoleculeSerializer


class DataView(APIView):
    @extend_schema(
        tags=["API"],
        parameters=build_openapi_parameters(
            ["region", "disk", "band", "molecule", "data"]
        ),
    )
    def get(self, request):
        data = models.Data.filter_data(
            name=request.query_params.get("data"),
            molecule=request.query_params.get("molecule"),
            band=request.query_params.get("band"),
            disk=request.query_params.get("disk"),
            region=request.query_params.get("region"),
        )
        serializer = full_context_serializers.FullContextDataSerializer(data, many=True)
        return Response({"data": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextDataSerializer

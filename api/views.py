from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from . import models
from .serializers import full_context_serializers


def build_openapi_parameters(names: list[str]) -> list[OpenApiParameter]:
    return [
        OpenApiParameter(
            name=name,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description=f"Filter by {name}",
            required=False,
            style="form",
            explode=True,
        )
        for name in names
    ]


class RegionView(APIView):
    @extend_schema(
        tags=["API"],
        parameters=build_openapi_parameters(["region"]),
    )
    def get(self, request: Request):
        regions = models.Region.objects.all()
        if region := request.query_params.getlist("region"):
            regions = regions.filter(name__in=region)
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
    def get(self, request: Request):
        disks = models.Disk.filter_disks(
            name=request.query_params.getlist("disk"),
            region=request.query_params.getlist("region"),
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
    def get(self, request: Request):
        bands = models.Band.filter_bands(
            name=request.query_params.getlist("band"),
            disk=request.query_params.getlist("disk"),
            region=request.query_params.getlist("region"),
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
    def get(self, request: Request):
        molecules = models.Molecule.filter_molecules(
            name=request.query_params.getlist("molecule"),
            band=request.query_params.getlist("band"),
            disk=request.query_params.getlist("disk"),
            region=request.query_params.getlist("region"),
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
    def get(self, request: Request):
        data = models.Data.filter_data(
            name=request.query_params.getlist("data"),
            molecule=request.query_params.getlist("molecule"),
            band=request.query_params.getlist("band"),
            disk=request.query_params.getlist("disk"),
            region=request.query_params.getlist("region"),
        )
        serializer = full_context_serializers.FullContextDataSerializer(data, many=True)
        return Response({"data": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return full_context_serializers.FullContextDataSerializer

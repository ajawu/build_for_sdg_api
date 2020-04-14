from rest_framework import serializers
from silk.models import Request, Response


class RegionFieldSerializer(serializers.Serializer):
    name = serializers.CharField()
    avgAge = serializers.FloatField()
    avgDailyIncomeInUSD = serializers.FloatField()
    avgDailyIncomePopulation = serializers.FloatField()


class EstimatorSerializer(serializers.Serializer):
    region = RegionFieldSerializer(source='*')
    periodType = serializers.CharField()
    timeToElapse = serializers.IntegerField()
    reportedCases = serializers.IntegerField()
    population = serializers.IntegerField()
    totalHospitalBeds = serializers.IntegerField()


class ImpactSerializer(serializers.Serializer):
    currentlyInfected = serializers.IntegerField()
    infectionsByRequestedTime = serializers.IntegerField()
    severeCasesByRequestedTime = serializers.IntegerField()
    hospitalBedsByRequestedTime = serializers.IntegerField()
    casesForICUByRequestedTime = serializers.IntegerField()
    casesForVentilatorsByRequestedTime = serializers.IntegerField()
    dollarsInFlight = serializers.FloatField()


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField(allow_null=True, allow_blank=True)


class EstimatorResponseSerializer(serializers.Serializer):
    data = EstimatorSerializer(source='*')
    severeImpact = ImpactSerializer(source='*')
    impact = ImpactSerializer(source='*')
    # error = ErrorSerializer(source='*')


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ('id', 'method', 'path', 'time_taken',)


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('id', 'status_code',)

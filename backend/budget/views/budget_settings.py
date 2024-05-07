from rest_framework import status, serializers
from utils.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from budget.models import BudgetSettings


class BudgetSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetSettings
        fields = '__all__'


@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def handle_compliance(request):
    user = request.user
    data = request.data

    budget_setting, created = BudgetSettings.objects.get_or_create(user=user)

    for key, value in data.items():
        setattr(budget_setting, key, value)

    budget_setting.save()

    if created:
        return Response({"message": "Compliance record created successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Compliance record updated successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_compliance(request):
    try:
        user = request.user

        budget_setting = BudgetSettings.objects.get(user=user)

        setting_serialiser = BudgetSettingsSerializer(budget_setting)
        return Response(setting_serialiser.data, status=status.HTTP_200_OK)

    except BudgetSettings.DoesNotExist:
        return Response({"error": "Message record does not exist for the user"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_compliance(request, setting_item):
    try:
        user = request.user
        budget_settings = BudgetSettings.objects.get(user=user)

        if hasattr(budget_settings, setting_item):
            setattr(budget_settings, setting_item, None)
            budget_settings.save()
            return Response({"message": f"{setting_item} deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"{setting_item} does not exist in the settings record"}, status=status.HTTP_404_NOT_FOUND)

    except BudgetSettings.DoesNotExist:
        return Response({"message": "Settings record does not exist for the user"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

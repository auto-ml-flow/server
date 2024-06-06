import pickle

import numpy as np
from core.viewsets import GenericViewSet
from meta_algo.api.serializers import MetaAlgoFeaturesSerializer, MetaAlgoPredictionsSerializer
from meta_algo.models import MetaAlgoModel
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import APIException

@extend_schema_view(
    predict=extend_schema(
        responses={status.HTTP_200_OK: MetaAlgoPredictionsSerializer},
    )
)
class MetaAlgoViewSet(GenericViewSet):
    queryset = MetaAlgoModel.objects.all()
    serializer_action_classes = {
        'predict': MetaAlgoFeaturesSerializer
    }

    @action(detail=False, methods=['POST'])
    def predict(self, request: Request, *args, **kwargs) -> Response:
        serializer = MetaAlgoFeaturesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            latest_algo = self.queryset.latest('id')
        except MetaAlgoModel.DoesNotExist:
            raise APIException(detail='Meta algo not ready yet')
        
        model = pickle.load(latest_algo.model)
        input_array = np.array([[serializer.data[field] for field in serializer.data]])

        # Make predictions using the loaded model
        prediction = model.predict(input_array)
        response_serializer = MetaAlgoPredictionsSerializer(data={'duration': prediction[0]})
        
        if not response_serializer.is_valid():
            raise APIException(detail='Predictions not valid!')
        
        return Response(response_serializer.data)
    
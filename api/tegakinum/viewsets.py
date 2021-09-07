from rest_framework import (
    generics,
    permissions,
    authentication,
    status,
    viewsets,
    filters
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q

from .models import (
    Num
)

from .serializers import (
    NumSerializer
)

import logging
import base64
import tensorflow as tf
import numpy as np
import json
import os
from tensorflow import keras
from PIL import Image, ImageOps
from django.conf import settings
from io import BytesIO

from django.conf import settings

logger = logging.getLogger(__name__)


class PredictViewSet(viewsets.ModelViewSet):

    queryset = Num.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = NumSerializer

    @action(methods=['POST'], detail=False)
    def getPredict(self, request):
        binary = ''

        for k, v in dict(request.data).items():
            binary = json.loads(k + v[0])['data'].replace(' ', '+')

        binary += '=' * (-len(binary) % 4)
        img_binary = base64.b64decode(binary)
        img = Image.open(BytesIO(img_binary))
        newImg = Image.new("RGB", img.size, (255, 255, 255))
        newImg.paste(img, mask=img.split()[3])

        model_file_path = settings.MODEL_FILE_PATH
        model = keras.models.load_model(model_file_path)

        newImg = ImageOps.invert(
            newImg.resize((28, 28)).convert('RGB')).convert('L')

        # newImg.save('newImg.png')

        ar = (np.array(newImg) / 255.0).reshape(-1, 28, 28, 1)

        result = model.predict(ar).tolist()
        # result = {i:'{:.2f}'.format(v) for i, v in enumerate(result[0])}
        result = ['{:.2f}'.format(i) for i in result[0]]

        return Response({
            'status': 'success',
            'result': result
        })

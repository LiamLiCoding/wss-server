from rest_framework import serializers

from .models import Devices


class DevicesSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Devices
        fields = '__all__'
        read_only_fields = ('id', 'created_time', 'suc_conv_num',
                            'failed_conv_num', 'api_key', 'last_login_time')

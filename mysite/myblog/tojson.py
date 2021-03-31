from rest_framework import serializers
from myblog.models import Classes,Userinfo


class Classes_data(serializers.ModelSerializer):
    #构建序列化元组
    class Meta:
        #深度
        depth = 1 
        #表
        model = Classes
        #字段
        fields = '__all__'

class Userinfo_data(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Userinfo
        fields = '__all__'
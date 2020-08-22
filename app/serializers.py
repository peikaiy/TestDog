from rest_framework import serializers

from app.models import Platform, Users, LotteryHistory, Pay, Share, Lottery


class PlatformSerializer(serializers.ModelSerializer):
    """平台数据序列化器"""

    class Meta:
        model = Platform

        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""

    class Meta:
        model = Users

        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['he_code']:
            data['he_code'] = ""

        return data


class PaySerializer(serializers.ModelSerializer):
    """用户充值记录数据序列化器"""
    t_pay = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Pay

        fields = '__all__'


class LastHistorySerializer(serializers.ModelSerializer):
    """开奖历史数据序列化器"""
    t_lottery = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = LotteryHistory
        ordering = ('-lottery_num',)
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['t_lottery']:
            data['t_lottery'] = ""
        if not data['lottery_number']:
            data['lottery_number'] = ""
        if not data['lottery_num']:
            data['lottery_num'] = ""

        return data


class LotterySerializer(serializers.ModelSerializer):
    """开奖历史数据序列化器"""
    t_lottery = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = LotteryHistory

        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['t_lottery']:
            data['t_lottery'] = ""
        if not data['lottery_number']:
            data['lottery_number'] = ""
        if not data['lottery_num']:
            data['lottery_num'] = ""

        return data


class LastLotterySerializer(serializers.ModelSerializer):
    """上期开奖数据序列化器"""
    t_lottery = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    t_bet = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Lottery

        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['t_lottery']:
            data['t_lottery'] = ""
        if not data['lottery_number']:
            data['lottery_number'] = ""
        if not data['lottery_num']:
            data['lottery_num'] = ""

        return data



class ShareSerializer(serializers.ModelSerializer):
    """推广数据序列化器"""
    u_name = serializers.SerializerMethodField(label='用户账户')

    class Meta:
        model = Share

        fields = ('u_name', 'share_money')

    def get_u_name(self, obj):
        u_name = Users.objects.get(u_id=obj.u_id).name
        return u_name
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if not data['t_lottery']:
    #         data['t_lottery'] = ""
    #     if not data['lottery_number']:
    #         data['lottery_number'] = ""
    #     if not data['lottery_num']:
    #         data['lottery_num'] = ""
    #
    #     return data

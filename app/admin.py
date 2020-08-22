import datetime

from django.contrib import admin

# Register your models here.
from collections import OrderedDict as SortedDict

# 修改模型显示顺序为注册顺序
from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from django.utils.text import capfirst

from app.models import Users, Platform, Pay, UserBet, Share


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        template_response = func(*args, **kwargs)
        for app in template_response.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return template_response

    return inner


registry = SortedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'pt_cost', 'pt_QQ', 'pt_money', 'pt_expel_money', 'pt_total_money')
    list_editable = ['pt_cost', 'pt_QQ', 'pt_money', 'pt_expel_money']

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "u_id", "name", "money", "share_num", 'ashare_money_today', "share_money", "my_code", "he_code", "login_status")
    list_editable = ['money']
    ordering = ("u_id",)
    search_fields = ('phone',)
    def has_add_permission(self, request):
        # 禁用添加按钮
        return False
    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def save_model(self, request, obj, form, change):
        """新增或者更新数据时调用"""
        old_money = Users.objects.get(u_id=obj.u_id).money
        super().save_model(request, obj, form, change)
        new_money = obj.money

        pay = Pay()
        pay.u_id = obj.u_id
        pay.pay_money = (new_money - old_money)
        pay.save()

    def ashare_money_today(self, obj):
        # 当前日期
        date_now = datetime.date.today()
        # # 查询天数
        da = datetime.timedelta(1)
        end = date_now + da
        # 推广人
        # 推广
        # 被推广人id 推广人 推广佣金
        # 当前推广人
        b_share = Share.objects.filter(share_user__u_id=obj.u_id).values('u_id')
        share_money_today = 0

        if b_share:
            u_bets = UserBet.objects.filter(Q(u_id__in=b_share) & Q(t_bet__range=(date_now, end)))

            for u_bet in u_bets:
                if u_bet.bet_money >= 20:
                    share_money_today += 1
            return '{}'.format(share_money_today)
        else:
            return '{}'.format(share_money_today)

    ashare_money_today.short_description = format_html(
        '<a style="color:#409eff;padding:8px 0px">当日推广金额</a>',

    )


# 支付管理
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('id',)
#

admin.site.register(Users, UsersAdmin)
admin.site.register(Platform, PlatformAdmin)

admin.site.site_title = "测试狗后台管理"
admin.site.site_header = "测试狗后台管理"

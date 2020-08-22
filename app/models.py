from django.db import models

# Create your models here.
# 登录 手机号微信号同号
# token 一直存在直至退出

login_status = (
    (0, '在线'),
    (1, '不在线'),
)


# 用户
# 用户名(微信和手机号一样同账号信息否则新账号) 余额 推广人数 赚取推广金 当日赚取推广金 推广人信息  邀请码 上家邀请码
class Users(models.Model):
    u_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=128, verbose_name='账户名')
    money = models.FloatField(default=0, verbose_name='账户余额')

    share_num = models.IntegerField(default=0, verbose_name='推广人数')
    share_money = models.IntegerField(default=0, verbose_name='推广金总额')
    # share_money_today = models.IntegerField(default=0, verbose_name='当日推广金')
    # # 多个
    # share_user = models.CharField(verbose_name='推广人信息')
    my_code = models.IntegerField(verbose_name='我的邀请码')
    he_code = models.IntegerField(null=True, verbose_name='上家邀请码')
    login_status = models.IntegerField(choices=login_status, default=0, verbose_name='登录状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'td_users'
        verbose_name = '账户管理'
        verbose_name_plural = verbose_name


# 短信
class PhoneCode(models.Model):
    phone = models.CharField(max_length=16, unique=True)
    sms_code = models.CharField(max_length=64)
    t_create = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'td_phone_code'


# 开奖历史
# 开奖时间  开奖号码   开奖期号
class LotteryHistory(models.Model):
    t_lottery = models.DateTimeField(auto_now_add=True, verbose_name='开奖时间')
    lottery_number = models.CharField(max_length=128, verbose_name='开奖号码')
    lottery_num = models.IntegerField(verbose_name='开奖期号')

    class Meta:
        db_table = 'td_lottery_history'
        ordering = ('-lottery_num', )
        verbose_name = '开奖历史'
        verbose_name_plural = verbose_name


# 开奖信息
# 期号  开奖号码    中奖金额
class Lottery(models.Model):
    lottery_num = models.IntegerField(verbose_name='开奖期号')
    lottery_number = models.CharField(max_length=128, verbose_name='开奖号码')
    lottery_money = models.FloatField(verbose_name='中奖金额')
    t_lottery = models.DateTimeField(auto_now=True, verbose_name='开奖时间')
    # 下注时间 统计时间 运算
    t_bet = models.DateTimeField(default='2020-06-22 13:45:57', verbose_name='下期开奖时间')
    # t_wait = models.DateTimeField(default='2020-06-22 13:45:57', verbose_name='等待时间')

    class Meta:
        db_table = 'td_lottery'
        verbose_name = '开奖信息'
        verbose_name_plural = verbose_name


bet_type = (
    (0, '小'),
    (1, '大'),
    (2, '双'),
    (3, '单')
)


# 玩家投注
# 玩家id 投注类型 投注金额 投注时间  投注期号
class UserBet(models.Model):
    u_id = models.IntegerField(verbose_name='玩家id')
    bet_type = models.IntegerField(choices=bet_type, verbose_name='投注类型')
    bet_money = models.FloatField(verbose_name='投注金额')
    t_bet = models.DateTimeField(auto_now_add=True, verbose_name='投注时间')
    bet_num = models.IntegerField(verbose_name='投注期号')

    class Meta:
        db_table = 'td_userbet'
        verbose_name = '玩家投注'
        verbose_name_plural = verbose_name


#     投注信息
#         用户  投注期号 投注金额  开奖号码 赚取金额
class BetInfo(models.Model):
    username = models.CharField(max_length=128, verbose_name='投注用户')
    bet_num = models.IntegerField(verbose_name='投注期号')
    bet_money = models.FloatField(verbose_name='投注金额')
    lottery_number = models.FloatField(verbose_name='开奖号码')
    win_money = models.FloatField(verbose_name='赚取金额')

    class Meta:
        db_table = 'td_betinfo'
        verbose_name = '投注信息'
        verbose_name_plural = verbose_name


# 上期平台赚取金额
#     金额  平台抛出奖金(抛出一次金额清零)        抛出状态
# 1w3k   5k                             抛出没抛
# 注：大于1w叠加抛出少于叠加 抛出少于抛出额 金额重置
class PlatformMoney(models.Model):
    pt_money = models.FloatField(verbose_name='金额')
    pt_expel_money = models.FloatField(verbose_name='抛出奖金')

    class Meta:
        db_table = 'td_platformmoney'
        verbose_name = '平台获利抛出'
        verbose_name_plural = verbose_name


# 推广
# 被推广人id 推广人 推广佣金
class Share(models.Model):
    u_id = models.IntegerField()
    # share_user = models.CharField(max_length=64, verbose_name='推广人姓名')
    share_user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='推广人')
    share_money = models.FloatField(default=0, verbose_name='推广佣金')

    class Meta:
        db_table = 'td_share'
        verbose_name = '推广'
        verbose_name_plural = verbose_name


# 充值记录
# 充值时间  充值金额 类型(0充值 1投注)
class Pay(models.Model):
    u_id = models.IntegerField()
    t_pay = models.DateTimeField(auto_now_add=True, verbose_name='充值时间')
    pay_money = models.FloatField(verbose_name='充值金额')


    class Meta:
        db_table = 'td_pay'
        verbose_name = '充值记录'
        verbose_name_plural = verbose_name


# 平台信息
#     平台手续费  客服
class Platform(models.Model):
    pt_cost = models.FloatField(verbose_name='平台手续费')
    pt_QQ = models.CharField(max_length=128, verbose_name='客服信息')

    pt_total_money = models.FloatField(default=0, verbose_name='总金额')
    pt_money = models.FloatField(default=0, verbose_name='赚取金额设定')
    pt_expel_money = models.FloatField(default=0, verbose_name='抛出金额')
    # pt_bet_rule = models.TextField(default='', verbose_name='竞猜规则')

    class Meta:
        db_table = 'td_platform'
        verbose_name = '平台信息'
        verbose_name_plural = verbose_name



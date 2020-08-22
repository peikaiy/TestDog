import datetime
import json
import logging
from random import random

import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import PhoneCode, Platform, Users, LotteryHistory, UserBet, Pay, Share, Lottery
from app.serializers import PlatformSerializer, UsersSerializer, LastHistorySerializer, PaySerializer, \
    ShareSerializer, LastLotterySerializer

logger = logging.getLogger('td_log')


def test(request):
    # 投注信息
    # # 本期全部投注
    usersbetall = UserBet.objects.filter(bet_num=180).values_list('u_id', flat=True)
    print(usersbetall)
    a = list(set(usersbetall))
    print(a)
    users = Users.objects.filter(u_id__in=a)
    print(users)
    #
    # # 用户信息 投注总额
    return HttpResponse('success')


# 验证码
def get_sms_code(num):
    code = ''
    for i in range(num):
        code += str(random.randint(0, 9))
    return code


def send_sms(template, phone):
    client = AcsClient('LTAI4G1ifFzikkSRBEjJ1vmd', '2QjFzxrUCO0RWDnb6buX745admKabn', 'default')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('http')  # https | http 注意当项目发布到服务器上需要修改协议
    request.set_version('2017-05-25')

    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "default")

    request.add_query_param('PhoneNumbers', phone)
    # request.add_query_param('SignName', "对折正品百货")
    # request.add_query_param('TemplateCode', "SMS_189520572")
    request.add_query_param('TemplateParam', f"{template}")
    response = client.do_action_with_exception(request)
    return response


# 发送验证码
class SmsAPIView(APIView):
    def post(self, request):
        response = {'status': 900, 'message': 'Sms Send Success'}
        try:
            phone = request.data.get('phone')

            sms_code = get_sms_code(4)
            template = {
                'code': sms_code
            }
            res = send_sms(template, phone=phone)
            res_dict = json.loads(res)
            if res_dict.get('Message') == 'OK' and res_dict.get('Code') == 'OK':
                phone_obj = PhoneCode.objects.filter(phone=phone).first()
                if phone_obj:
                    phone_obj.sms_code = sms_code
                    phone_obj.save()

                else:
                    PhoneCode.objects.create(phone=phone, sms_code=sms_code)
                response['sms_code'] = sms_code
                return Response(response)
            else:
                response['status'] = 901
                response['message'] = 'Sms Send Fail'
                return Response(response)

        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: sms, ERROR: {}'.format(e))
            return Response(response)


# 过期时间
def get_t_node():
    date_now = datetime.datetime.now()
    t_expiration = datetime.timedelta(minutes=50000)
    t_node = date_now - t_expiration
    return t_node


# 邀请码生成
def get_my_code():
    user = Users.objects.last()
    if user:
        mycode = user.my_code + 1
        return mycode
    else:
        mycode = 12537
        return mycode


class UserAPIView(APIView):
    def get(self, request, pk):
        try:
            response = {'status': 900, 'message': 'Success'}
            user = Users.objects.get(u_id=pk)
            user_class = UsersSerializer(user)
            response['data'] = user_class.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: user/id, ERROR: {}'.format(e))
            return Response(response)


# token
# def get_token():
#     token = uuid.uuid1()
#     return token

# 手机号验证码登录
class LoginAPIView(APIView):
    def post(self, request):

        try:
            response = {'status': 900, 'message': 'Login Success'}
            phone = request.data.get('phone')
            sms_code = request.data.get('sms_code')

            phone_obj = PhoneCode.objects.get(phone=phone)
            t_node = get_t_node()
            if t_node <= phone_obj.t_create:
                if sms_code == phone_obj.sms_code:
                    my_code = get_my_code()

                    user = Users.objects.filter(name=phone).first()
                    # token = str(get_token())
                    if user:
                        # request.session[token] = user.u_id
                        user.login_status = 0
                        user.save()
                    else:
                        user = Users.objects.create(name=phone, my_code=my_code)
                        # request.session[token] = user.u_id
                    user_class = UsersSerializer(user)
                    response['data'] = user_class.data
                    # response['data']['token'] = token
                    return Response(response)
                else:
                    response = {'status': 901, 'message': 'Sms Code Fail'}
                    return Response(response)

            else:
                response = {'status': 901, 'message': 'Verification code invalidation'}
                return Response(response)

        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: user/login, ERROR: {}'.format(e))
            return Response(response)


# 获取openid
class Code2SessionAPIView(APIView):

    def post(self, request, *args, **kwargs):
        appid = 'wx0b757803fc4380c7'
        secret = '1b9ef3807d91898f1645d55806be6c3d'
        # js_code = 'ss'
        try:

            js_code = request.data.get('js_code')

            url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
            response = json.loads(requests.get(url).content)  # 将json数据包转成字典
            # return Response(data={'msg': str(response)})
        except Exception as e:
            return Response(data={'msg': '失败啦', 'data': request.data})

        try:

            # 有错误码
            # 获取成功
            openid = response['openid']
            session_key = response['session_key']
            data = {'openid': openid, 'session_key': session_key, 'status': 900, 'msg': 'ok'}
            return Response(data)

        except Exception as e:
            response = {'status': 901, 'message': 'openid获取失败，error:{}'.format(str(response))}
            return Response(response)


# 微信登录
class WxLoginAPIView(APIView):
    def post(self, request):
        try:
            response = {'status': 900, 'message': 'WxLogin Success'}
            name = request.data.get('name')
            my_code = get_my_code()
            user = Users.objects.filter(name=name).first()
            # token = str(get_token())
            if user:
                # request.session[token] = user.u_id
                user.login_status = 0
                user.save()
            else:
                user = Users.objects.create(name=name, my_code=my_code)
            user_class = UsersSerializer(user)
            response['data'] = user_class.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: user/wxlogin, ERROR: {}'.format(e))
            return Response(response)


# 退出
class LogoutAPIView(APIView):
    def post(self, request):
        try:
            response = {'status': 900, 'message': 'Logout Success'}
            u_id = request.data.get('u_id')
            user = Users.objects.get(u_id=u_id)
            user.login_status = 1
            user.save()
            user_class = UsersSerializer(user)
            response['data'] = user_class.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: user/logout, ERROR: {}'.format(e))
            return Response(response)


# 下注
class BetAPIView(APIView):
    def post(self, request):
        try:
            """
            
            单个 
                "u_id=1,bet_num,bet_type=1,bet_moeny=600"
            多个
                "1,1,1,600&1,2,600"
            bet_info 用户id 投注期号 投注类型 投注金额
            
            u_id=1,bet_num=1,bet_type=1,bet_moeny=600
            """

            bet_infos = request.data.get('bet_info')
            if not bet_infos:
                response = {'status': 903, 'message': 'Fail', 'error': 'Required parameter missing'}
                return Response(response)
            response = {'status': 900, 'message': 'Bet Success'}
            bet_infos_split = bet_infos.split('&')
            userbetlist = []
            u_id = bet_infos_split[0][0]
            # 投注期数
            bet_nums = bet_infos_split[0].split(',')[1]
            # 上期期数
            top_bet_num = Lottery.objects.first().lottery_num
            # 已封盘
            if int(bet_nums) != (top_bet_num + 1):
                response = {'status': 901, 'message': 'Entertained'}
                return Response(response)
            user = Users.objects.get(u_id=u_id)

            for bet_info in bet_infos_split:
                if bet_info:
                    bet = bet_info.split(',')

                    bet_money = int(bet[-1])
                    if user.money <= bet_money:
                        response = {'status': 901, 'message': 'Money Not Enough'}
                        return Response(response)
                    user.money -= bet_money

                    if bet_money >= 20:
                        try:
                            share_user = Share.objects.get(u_id=u_id).share_user
                            share = Share.objects.filter(u_id=u_id).first()

                            # 推广总额增加
                            share_user.share_money += 1
                            # 推广人金额增加
                            share_user.money += 1
                            share_user.save()
                            # 推广信息增加
                            share.share_money += 1
                            share.save()
                        except Exception as e:
                            pass
                    userbetlist.append(UserBet(u_id=bet[0], bet_type=bet[2], bet_money=bet[3], bet_num=bet[1]))
            user.save()
            UserBet.objects.bulk_create(userbetlist)
            user_class = UsersSerializer(user)
            response['data'] = user_class.data
            return Response(response)

        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: user/bet, ERROR: {}'.format(e))
            return Response(response)


# 填写邀请码
class InvitationCodeAPIView(APIView):
    def post(self, request):
        try:
            response = {'status': 900, 'message': 'Success'}
            u_id = request.data.get("u_id")
            he_code = request.data.get("he_code")
            user = Users.objects.get(u_id=u_id)
            user.he_code = he_code
            user.save()

            he_user = Users.objects.filter(my_code=he_code).first()
            he_user.share_num += 1
            he_user.save()
            Share.objects.create(u_id=u_id, share_user=he_user)
            response['data'] = UsersSerializer(user).data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('POST: user/invitation-code, ERROR: {}'.format(e))
            return Response(response)


# 充值记录
class PayAPIView(APIView):
    def get(self, request):
        try:
            response = {'status': 900, 'message': 'Success'}
            u_id = request.query_params.get('u_id')
            userpay = Pay.objects.filter(u_id=u_id)
            userpay_class = PaySerializer(instance=userpay, many=True)
            response['data'] = userpay_class.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('GET: user/pay, ERROR: {}'.format(e))
            return Response(response)


# 个人推广信息
class ShareAPIView(APIView):
    def get(self, request):
        try:
            response = {'status': 900, 'message': 'Success'}
            u_id = request.query_params.get("u_id")
            user = Users.objects.get(u_id=u_id)
            share = Share.objects.filter(share_user_id=u_id)
            share_class = ShareSerializer(instance=share, many=True)

            # 当前日期
            date_now = datetime.date.today()
            # # 查询天数
            da = datetime.timedelta(1)
            end = date_now + da
            # 推广人
            # 推广
            # 被推广人id 推广人 推广佣金
            # 当前推广人
            b_share = Share.objects.filter(share_user__u_id=u_id).values('u_id')
            share_money_today = 0

            if b_share:
                u_bets = UserBet.objects.filter(Q(u_id__in=b_share) & Q(t_bet__range=(date_now, end)))

                for u_bet in u_bets:
                    if u_bet.bet_money >= 20:
                        share_money_today += 1

            """
            推广总金额
            推广人数
            当日推广金额
            下级信息
            """
            data = {
                "share_money": user.share_money,
                "share_num": user.share_num,
                "share_money_today": share_money_today,
                "share_user": share_class.data,
            }
            response['data'] = data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('GET: share, ERROR: {}'.format(e))
            return Response(response)


# 平台信息
class PlatformAPIView(APIView):
    def get(self, request):
        try:

            response = {'status': 900, 'message': 'Success'}

            pt = Platform.objects.first()
            pt_class = PlatformSerializer(pt)
            response['data'] = pt_class.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('GET: platform, ERROR: {}'.format(e))
            return Response(response)


# 开奖历史
class LotteryHistoryAPIView(APIView):
    def get(self, request):
        try:
            response = {'status': 900, 'message': 'Success'}
            lastlottery = LotteryHistory.objects.all()
            if not lastlottery:
                response['data'] = ""
                return Response(response)
            lastlottery_class = LastHistorySerializer(instance=lastlottery, many=True)
            response['data'] = lastlottery_class.data

            return Response(response)

        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('GET: lotteryhistory, ERROR: {}'.format(e))
            return Response(response)


# 上期开奖
class LastLotteryAPIView(APIView):
    def get(self, request):
        try:
            response = {'status': 900, 'message': 'Success'}
            lottery = Lottery.objects.first()
            if not lottery:
                response['data'] = ""
                return Response(response)
            lottery_class = LastLotterySerializer(lottery)
            response['data'] = lottery_class.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': 'Fail', 'error': str(e)}
            logger.error('GET: lastlottery, ERROR: {}'.format(e))
            return Response(response)

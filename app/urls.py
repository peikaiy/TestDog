from django.urls import path, re_path

from app import api
app_name = 'app'
urlpatterns = [
    path('test', api.test),
    # sms
    # re_path(r'^sms$', api.SmsAPIView.as_view()),
    # 短信登录
    re_path(r'^user/login$', api.LoginAPIView.as_view()),
    # 获取 openid  session_key
    re_path(r'^code2session$', api.Code2SessionAPIView.as_view()),
    # 微信登录
    re_path(r'^user/wxlogin$', api.WxLoginAPIView.as_view()),
    # 个人信息
    re_path(r'^user/(?P<pk>\d+)$', api.UserAPIView.as_view()),
    # 退出
    re_path(r'^user/logout$', api.LogoutAPIView.as_view()),
    # 下注
    re_path(r'^user/bet', api.BetAPIView.as_view()),
    # 充值记录
    re_path(r'^user/pay', api.PayAPIView.as_view()),
    # 填写邀请码
    re_path(r'^user/invitation-code', api.InvitationCodeAPIView.as_view()),
    # 推广信息
    re_path(r'^user/share', api.ShareAPIView.as_view()),
    # 平台信息
    re_path(r'^platform', api.PlatformAPIView.as_view()),
    # 开奖历史
    re_path(r'^lotteryhistory', api.LotteryHistoryAPIView.as_view()),
    # 上期开奖
    re_path(r'^lastlottery', api.LastLotteryAPIView.as_view()),




]

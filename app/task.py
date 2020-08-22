import datetime
import logging
import random

from celery.task import task
from django.db.models import Q, Sum

from app.models import LotteryHistory, UserBet, PlatformMoney, Platform, Lottery, Users

logger = logging.getLogger('td_log')


# 投注结果排序 小-大
def ret_money_sort(ret_money):
    for i in range(len(ret_money) - 1):
        for j in range(i, len(ret_money) - 1 - i):
            if ret_money[j] > ret_money[j + 1]:
                ret_money[j], ret_money[j + 1] = ret_money[j + 1], ret_money[j]
    return ret_money


@task
def lottery(*args):
    try:
        logger.debug('开奖及统计执行中')
        t = args[0]

        # 当前期号 历史期号
        # 投注信息  投注的金额 赔钱金额
        # 期号
        bet_num = LotteryHistory.objects.last()
        if not bet_num:
                bet_num = 1

        else:
            bet_num = LotteryHistory.objects.last().lottery_num + 1

        # 投注金额
        userbets = UserBet.objects.filter(bet_num=bet_num)
        # 大 小  单 双
        """
        bet_type = (
            (0, '小'),
            (1, '大'),
            (2, '双'),
            (3, '单')
        )
        """
        # 大
        big = userbets.filter(bet_type=1).aggregate(total_money=Sum('bet_money'))['total_money']
        # 小
        small = userbets.filter(bet_type=0).aggregate(total_money=Sum('bet_money'))['total_money']
        # 单
        single = userbets.filter(bet_type=3).aggregate(total_money=Sum('bet_money'))['total_money']
        # 双
        double = userbets.filter(bet_type=2).aggregate(total_money=Sum('bet_money'))['total_money']
        # big_singular大单 大双 小单 小双
        if not big:
            big = 0
        if not small:
            small = 0
        if not single:
            single = 0
        if not double:
            double = 0

        bigsingle = big + single
        bigdouble = big + double
        smallsingle = small + single
        smalldouble = small + double
        total_bet = big + single + small + double
        # 3小单 4小双 5大单 6大双
        ret_money = [{'name': 5, 'money': bigsingle}, {'name': 6, 'money': bigdouble},
                     {'name': 3, 'money': smallsingle}, {'name': 4, 'money': smalldouble}]
        ret_sort = sorted(ret_money, key=lambda keys: keys['money'])
        single = [1, 3, 5, 7, 9]
        double = [0, 2, 4, 6, 8]
        big = [5, 6, 7, 8, 9]
        small = [0, 1, 2, 3, 4]

        d = {
            3: [str(random.choice(small)), str(random.randint(0, 9)), str(random.randint(0, 9)),
                str(random.choice(single))],
            4: [str(random.choice(small)), str(random.randint(0, 9)), str(random.randint(0, 9)),
                str(random.choice(double))],
            5: [str(random.choice(big)), str(random.randint(0, 9)), str(random.randint(0, 9)),
                str(random.choice(single))],
            6: [str(random.choice(big)), str(random.randint(0, 9)), str(random.randint(0, 9)),
                str(random.choice(double))],
        }
        # ptm 赚取奖金  pt平台给出的条件
        ptm = PlatformMoney.objects.first()
        pt = Platform.objects.first()

        # 开奖号码
        lottery = Lottery.objects.first()
        # 历史开奖
        lotteryhistory = LotteryHistory()
        if not lottery:
            lottery = Lottery.objects.create(lottery_num=bet_num, lottery_number=0, lottery_money=0)
        lottery.lottery_num = bet_num
        lotteryhistory.lottery_num = bet_num

        if not ptm:
            ptm = PlatformMoney.objects.create(pt_money=0, pt_expel_money=0)
        #  不满足抛出条件
        if ptm.pt_money < pt.pt_money:

            # 金额没达到 累加 抛最少
            u_win_money = ret_sort[0]['money'] + (ret_sort[0]['money'] - ret_sort[0]['money'] * pt.pt_cost)
            lottery.lottery_money = u_win_money

            list_bet_number = d[ret_sort[0]['name']]

            # 开奖结果
            lottery_ret = ret_sort[0]['name']

            bet_number = ",".join(list_bet_number)
            lottery.lottery_number = bet_number
            lottery.save()

            total_money = total_bet - u_win_money
            pt.pt_total_money += total_money
            pt.save()
            ptm.pt_money += total_money
            ptm.save()

        # 满足抛出条件
        else:
            # 抛出成功 清零
            # 不成功 金额累加  保留

            expel_money = pt.pt_expel_money
            kaijiang = {}
            for bet in ret_sort:
                u_win_money = bet['money'] + (bet['money'] - (bet['money'] * pt.pt_cost))
                bet['money'] = u_win_money
                if expel_money >= u_win_money:
                    kaijiang['bet'] = bet
            if not kaijiang:

                list_bet_number = d[ret_sort[0]['name']]

                # 开奖结果
                lottery_ret = ret_sort[0]['name']

                bet_number = ",".join(list_bet_number)
                lottery.lottery_money = ret_sort[0]['money']
                lottery.lottery_number = bet_number
                lottery.save()

                total_money = total_bet - ret_sort[0]['money']

                pt.pt_total_money += total_money
                pt.save()
                ptm.pt_money += total_money
                ptm.save()

            else:
                list_bet_number = d[kaijiang['bet']['name']]

                # 开奖结果
                lottery_ret = ret_sort[0]['name']

                bet_number = ",".join(list_bet_number)
                lottery.lottery_money = kaijiang['bet']['money']
                lottery.lottery_number = bet_number
                lottery.save()

                total_money = total_bet - kaijiang['bet']['money']
                pt.pt_total_money += total_money
                pt.save()
                ptm.pt_money = 0
                ptm.save()

        lotteryhistory.lottery_num = bet_num
        lotteryhistory.lottery_number = bet_number

        lotteryhistory.save()
        # 给中奖用户分钱
        # 3小单 4小双 5大单 6大双

        # bet_type = (
        #     (0, '小'),
        #     (1, '大'),
        #     (2, '双'),
        #     (3, '单')
        # )

        lottery_num = lotteryhistory.lottery_num
        if lottery_ret == 3:
            usersbet = UserBet.objects.filter(bet_num=lottery_num).filter((Q(bet_type=0) | Q(bet_type=3)))

        elif lottery_ret == 4:
            usersbet = UserBet.objects.filter(bet_num=lottery_num).filter(Q(bet_type=0) | Q(bet_type=2))
        elif lottery_ret == 5:
            usersbet = UserBet.objects.filter(bet_num=lottery_num).filter(Q(bet_type=1) | Q(bet_type=3))
        else:
            # lottery_ret == 6:
            usersbet = UserBet.objects.filter(bet_num=lottery_num).filter(Q(bet_type=1) | Q(bet_type=2))
        for userbet in usersbet:
            # 赢的钱
            u_win = userbet.bet_money + (userbet.bet_money - userbet.bet_money * pt.pt_cost)
            user = Users.objects.get(u_id=userbet.u_id)
            user.money += u_win
            user.save()
        # 投注信息
        # # 本期全部投注
        # usersbetall = UserBet.objects.filter(bet_num=bet_num).values_list('u_id')
        #
        # # 用户信息 投注总额
        #

        logger.debug('开奖及统计成功')
        # 下期开奖时间
        t_lottery = lottery.t_lottery
        t_wait = datetime.timedelta(minutes=t)
        t_bet = t_lottery + t_wait
        lottery.t_bet = t_bet
        lottery.save()




    except Exception as e:
        logger.error('开奖及统计出错了%s' % (str(e)))

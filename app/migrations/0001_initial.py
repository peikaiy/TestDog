# Generated by Django 2.2 on 2020-06-19 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lottery_num', models.IntegerField(verbose_name='开奖期号')),
                ('lottery_number', models.IntegerField(verbose_name='开奖号码')),
                ('lottery_moeny', models.FloatField(verbose_name='中奖金额')),
            ],
            options={
                'verbose_name': '开奖信息',
                'verbose_name_plural': '开奖信息',
                'db_table': 'td_lottery',
            },
        ),
        migrations.CreateModel(
            name='LotteryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_lottery', models.DateTimeField(verbose_name='开奖时间')),
                ('lottery_number', models.IntegerField(verbose_name='开奖号码')),
                ('lottery_num', models.IntegerField(verbose_name='开奖期号')),
            ],
            options={
                'verbose_name': '开奖历史',
                'verbose_name_plural': '开奖历史',
                'db_table': 'td_lottery_history',
            },
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_pay', models.FloatField(verbose_name='充值时间')),
                ('pay_money', models.FloatField(verbose_name='充值金额')),
            ],
            options={
                'verbose_name': '充值记录',
                'verbose_name_plural': '充值记录',
                'db_table': 'td_pay',
            },
        ),
        migrations.CreateModel(
            name='PhoneCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=16, unique=True)),
                ('sms_code', models.CharField(max_length=64)),
                ('t_create', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'td_phone_code',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_cost', models.FloatField(verbose_name='平台手续费')),
                ('pt_QQ', models.CharField(max_length=128, verbose_name='客服信息')),
            ],
            options={
                'verbose_name': '平台信息',
                'verbose_name_plural': '平台信息',
                'db_table': 'td_platform',
            },
        ),
        migrations.CreateModel(
            name='PlatformMoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_moeny', models.FloatField(verbose_name='金额')),
                ('pt_expel_moeny', models.FloatField(verbose_name='抛出奖金')),
            ],
            options={
                'verbose_name': '平台获利抛出',
                'verbose_name_plural': '平台获利抛出',
                'db_table': 'td_platformmoney',
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.IntegerField()),
                ('share_user', models.CharField(max_length=64, verbose_name='推广人姓名')),
                ('share_moeny', models.FloatField(verbose_name='推广佣金')),
            ],
            options={
                'verbose_name': '推广',
                'verbose_name_plural': '推广',
                'db_table': 'td_share',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='账户名')),
                ('money', models.FloatField(default=0, verbose_name='账户余额')),
                ('share_num', models.IntegerField(default=0, verbose_name='推广人数')),
                ('share_moeny', models.IntegerField(default=0, verbose_name='推广金总额')),
                ('share_moeny_today', models.IntegerField(null=True, verbose_name='当日推广金')),
                ('my_code', models.IntegerField(verbose_name='我的邀请码')),
                ('he_code', models.IntegerField(null=True, verbose_name='上家邀请码')),
                ('login_status', models.IntegerField(choices=[(0, '在线'), (1, '不在线')], default=0, verbose_name='登录状态')),
            ],
            options={
                'verbose_name': '账户管理',
                'verbose_name_plural': '账户管理',
                'db_table': 'td_users',
            },
        ),
        migrations.CreateModel(
            name='UserBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet_type', models.IntegerField(choices=[(0, '小'), (1, '大'), (2, '双'), (3, '单')], verbose_name='投注类型')),
                ('bet_moeny', models.FloatField(verbose_name='投注金额')),
                ('t_bet', models.DateTimeField(auto_now_add=True, verbose_name='投注时间')),
                ('bet_num', models.FloatField(verbose_name='投注期号')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='玩家')),
            ],
            options={
                'verbose_name': '玩家投注',
                'verbose_name_plural': '玩家投注',
                'db_table': 'td_userbet',
            },
        ),
    ]

from django.db import models

# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=20,null=False,unique=True,verbose_name='账号')
    password = models.CharField(max_length=20,null=False,verbose_name='密码')
    name=models.CharField(max_length=20,unique=True,verbose_name='姓名')
    idnum=models.CharField(max_length=40,null=False,unique=True,verbose_name='身份证号')
    telnum=models.CharField(max_length=20,null=False,unique=True,verbose_name='联系电话')
    email = models.CharField(max_length=40,verbose_name='邮箱')

    def __str__(self):
        return self.userid

class Passenger(models.Model):
    name=models.CharField(max_length=20,verbose_name='乘机人姓名')
    idnum=models.CharField(max_length=20,verbose_name='乘机人身份证号')
    telnum=models.CharField(max_length=40,verbose_name='乘机人联系电话')
    user = models.ManyToManyField(to='User',verbose_name='乘机人对应用户')

    def __str__(self):
        return self.name

class Flight(models.Model):
    """航班票务信息表"""
    flight_id = models.CharField(verbose_name="航班号", max_length=20)
    departure_day = models.DateField(verbose_name="出发日期")
    departure_time = models.TimeField(verbose_name="出发时刻")
    arrival_day = models.DateField(verbose_name='到达日期')
    arrival_time = models.TimeField(verbose_name="到达时刻")
    departure_airport = models.CharField(verbose_name="出发机场", max_length=20)
    arrival_airport = models.CharField(verbose_name="到达机场", max_length=20)
    stopover_airport = models.CharField(verbose_name="经停机场", max_length=20)
    first_class_num = models.IntegerField(verbose_name="头等舱数")
    first_class_price = models.IntegerField(verbose_name="头等舱价格")
    economy_class_num = models.IntegerField(verbose_name="经济舱数")
    economy_class_price = models.IntegerField(verbose_name="经济舱价格")
    aircraft_type = models.CharField(verbose_name="飞机型号", max_length=20, blank=True)
    voyage = models.IntegerField(verbose_name="航程", blank="True")
    company = models.CharField(verbose_name="航空公司", max_length=40, blank=True)
    # 联合主键
    class Meta:
        unique_together = (("flight_id", "departure_day"),)

    def __str__(self):
        return self.flight_id

class Airport(models.Model):
    """机场表"""
    airport_id = models.CharField(verbose_name="机场代码", max_length=20, primary_key=True, unique=True)
    airport_name = models.CharField(verbose_name="机场名称", max_length=20, unique=True)
    city = models.CharField(verbose_name="城市", max_length=20)

    def __str__(self):
        return self.airport_name

class Order(models.Model):
    userid=models.CharField(verbose_name="账号",max_length=20,null=False)
    flightnum=models.CharField(verbose_name="航班号",max_length=20,null=False)
    departure_day=models.DateField(verbose_name="出发日期",null=False)
    passid=models.CharField(verbose_name="乘机人身份证号",max_length=20,null=False)
    classtype=models.CharField(verbose_name="舱位",max_length=20,null=False)
    ordertime=models.DateTimeField(verbose_name="订票时间")
    class Meta:
        indexes = [models.Index(fields=['userid']), ]



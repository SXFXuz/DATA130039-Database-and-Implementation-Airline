from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from app02 import models
from time import strftime

# Create your views here.

def welcome(request):
    return render(request,'welcome.html')

def login(request):
    #这是登陆函数
    if request.method == 'POST':
        #获取表单提交的内容，分别是账号和密码
        login_userid = request.POST.get("userid")
        login_password = request.POST.get("password")
        if not login_userid:
            return render(request, 'login.html', {'error1': '用户名不能为空'})
        if not login_password:
            return render(request, 'login.html', {'error2': '密码不能为空'})
        #这是在查找数据库中有无此账号和密码
        result = models.User.objects.filter(userid=login_userid,password=login_password).first()
        if not models.User.objects.filter(userid=login_userid).first():
            return render(request, 'login.html', {'error1': '用户名不存在'})
        if not models.User.objects.filter(password=login_password).first():
            return render(request, 'login.html', {'error2': '密码错误'})

        #如果存在，就会返回对像，否则为空
        #session可以保存当前的状态，用request.session['is_login'] = True表示当前处于登录状态，下面一行储存了当前用户的账号。
        #这样，在跳转到其他页面时，通过session,就可以知道用户是否登录。
        if result:
            request.session['is_login'] = True
            request.session['userid'] = login_userid
            request.session['error_info'] = ''
            request.session.set_expiry(0)
            return redirect("/app02/index/")
        else:
            return render(request,'login.html')

    #如果没有登陆失败，就跳转回登陆界面
    return render(request,'login.html')

#这是注册函数
def register(request):
    if request.method == 'POST':
        #获取表单提交的内容
        register_userid = request.POST.get("userid")
        register_password = request.POST.get("password")
        register_name = request.POST.get("name")
        register_idnum = request.POST.get("idnum")
        register_telnum = request.POST.get("telnum")
        register_email = request.POST.get("email")
        #保存到数据库
        if not register_userid:
            return render(request, 'register.html', {'error1': '用户名不能为空'})
        if not register_password:
            return render(request, 'register.html', {'error3': '密码不能为空'})
        if not register_name:
            return render(request, 'register.html', {'error4': '姓名不能为空'})
        if not register_idnum:
            return render(request, 'register.html', {'error2': '身份证号不能为空'})
        if models.User.objects.filter(userid=register_userid).first():
            return render(request,'register.html',{'error1':'用户名已存在'})
        if models.User.objects.filter(idnum=register_idnum).first():
            return render(request, 'register.html', {'error2' : '该身份证已注册'})
        models.User.objects.create(userid =register_userid, password=register_password,name=register_name,idnum=register_idnum,telnum=register_telnum,email=register_email)
        return redirect("/app02/login/")

    #这个语句是返回注册界面，访问注册界面时执行该语句。而提交注册信息时执行上面部分的语句。
    return render(request,'register.html')

#这是主界面函数
def index(request):
    #访问时，首先判断是否登录，若没有，则返回登陆界面，下同。
    is_login = request.session.get("is_login",False)
    if is_login:
        userid = request.session.get("userid")
        return render(request,"index.html",context={"userid":userid})
    else:
        return redirect("login")


def logout(request):
    request.session.flush()
    return redirect("/app02/welcome")

#这是个人信息界面修改界面
def information(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        if request.method == 'GET':
            #如果用户访问了这个网页，就返回个人信息修改的界面。需要通过session获取当前用户的账号，并搜索出该用户的个人信息并返回。
            userid = request.session.get("userid")
            user_information = models.User.objects.filter(userid=userid).first()
            #这里返回了information模板，最后{}表式还将变量user_infromation传递给了模板
            return render(request,'information.html',{'user_information':user_information,'error1':request.session['error_info'],'error2':request.session['error_info'],'error3':request.session['error_info']})
        else:
            #用户点击了更改按钮，将更改后提交过来的信息保存到数据库。
            id = request.POST.get('id')
            password = request.POST.get('password')
            name = request.POST.get('name')
            idnum = request.POST.get('idnum')
            telnum = request.POST.get('telnum')
            email = request.POST.get('email')
            if not password:
                request.session['error_info']='密码不能为空'
                return redirect('/app02/information/')
            else:
                request.session['error_info'] = ''
            if not name:
                request.session['error_info'] = '姓名不能为空'
                return redirect('/app02/information/')
            else:
                request.session['error_info'] = ''
            if not idnum:
                request.session['error_info']='身份证号不能为空'
                return redirect('/app02/information/')
            else:
                request.session['error_info'] = ''
            if models.User.objects.filter(name=name).first() and models.User.objects.filter(name=name).first().name != name:
                request.session['error_info'] = '姓名重复'
                return redirect('/app02/information/')
            else:
                request.session['error_info'] = ''
            if models.User.objects.filter(idnum=idnum).first() and models.User.objects.filter(name=name).first().idnum != idnum:
                request.session['error_info'] = '身份证号已注册'
                return redirect('/app02/information/')
            else:
                request.session['error_info'] = ''
            models.User.objects.filter(id=id).update(password=password,name=name,idnum=idnum,telnum=telnum,email=email)
            return redirect("/app02/index")

    else:
        return redirect('login')

#这是乘机人界面。核心是通过session的当前用户信息，搜索并返回与该用户关联的所有乘机人信息。
def passenger(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        userid = request.session.get("userid")
        user_obj = models.User.objects.filter(userid=userid).first()
        passenger_list = user_obj.passenger_set.all()
        return render(request, 'passenger.html', {'passenger_list': passenger_list, 'userid': userid})

    return redirect('/app02/login/')


#这是添加乘机人界面，原理和上面一样。GET表示用户只是访问了改界面。否则为POST，是提交了新设置的乘机人信息
def add_passenger(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        if request.method == 'GET':
            return render(request,'add_passenger.html')
        else:
            userid = request.session.get("userid")
            user_obj = models.User.objects.get(userid=userid)
            name = request.POST.get('name')
            telnum = request.POST.get('telnum')
            idnum = request.POST.get('idnum')
            if not name:
                return render(request,'add_passenger.html',{'error1':'乘机人姓名不能为空'})
            if not idnum:
                return render(request,'add_passenger.html',{'error2':'乘机人身份证号不能为空'})
            passenger_obj = models.Passenger.objects.create(name=name, idnum=idnum, telnum=telnum)
            user_id = user_obj.id
            passenger_id = passenger_obj.id
            #这里在将新设置的乘机人信息保存到数据库中后，还要通过以下语句来建立改用户和乘机人之间的联系。
            passenger_obj.user.add(user_obj)

            return redirect('/app02/passenger/')
    return redirect('/app02/login/')

#这是删除乘机人的函数。
def delete_passenger(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        id = request.GET.get('id')
        passengerid = models.Passenger.objects.filter(id=id).first().idnum
        userid = request.session.get("userid")
        order = models.Order.objects.filter(userid = userid,passid = passengerid)
        if order:
            return redirect('/app02/passenger/')
        models.Passenger.objects.filter(id=id).delete()
        return redirect('/app02/passenger/')
    return redirect('/app02/login/')


# 获取今日时间，以便搜索航班时限定出发日期
today=strftime("%Y-%m-%d")

# 对搜索结果排序时的，参考字典
OrderBy_Dict={"ByTime":"departure_time","ByFirstPrice":"first_class_price","ByEconoPrice":"economy_class_price"}

# 查询航班的网页
def flights_search(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        if request.method=="POST":
            input_dep_city=request.POST.get("dep_city")
            input_arr_city=request.POST.get("arr_city")
            #根据输入的城市在Airport表里搜索(只选出第一个)
            find_dep_city=models.Airport.objects.filter(city__icontains=input_dep_city).first()
            find_arr_city=models.Airport.objects.filter(city__icontains=input_arr_city).first()
            # 确认找得到城市时才传参到session
            if not find_dep_city or not find_arr_city:
                return render(request,"flights_view.html",{"cur_time":strftime("%Y-%m-%d"),"typeinerror":True})
            request.session["dep_city"]=find_dep_city.city
            request.session["arr_city"]=find_arr_city.city
            request.session["dep_day"] = request.POST.get("dep_day")
            request.session["OrderBy"]=OrderBy_Dict[request.POST.get("InWhatOrder")]
            return redirect("/app02/search_result")
        return render(request,"flights_view.html",{"cur_time":strftime("%Y-%m-%d"),"typeinerror":False})
    return redirect('/app02/login/')


# 查询结果的网页
def search_result(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        search_dep_day =request.session.get("dep_day")
        search_dep_city =request.session.get("dep_city")
        search_arr_city =request.session.get("arr_city")
        orderByWhat =request.session.get("OrderBy")
        # 根据城市搜索机场
        dep_airport_list = models.Airport.objects.filter(city=search_dep_city)
        arr_airport_list = models.Airport.objects.filter(city=search_arr_city)
        # 根据出发日期、出发机场、到达机场找到所有，并排序。
        # list里每一项都是数据库中的一行记录，在django中是一个实例化的class
        flight_list = models.Flight.objects.filter(
            departure_day=search_dep_day,
            departure_airport__in=[each.airport_name for each in dep_airport_list],
            arrival_airport__in = [each.airport_name for each in arr_airport_list]
        ).order_by(orderByWhat)
        firstclass=[]
        econoclass=[]
        for flightobj in flight_list:
            first=-models.Order.objects.filter(flightnum=flightobj.flight_id,departure_day=flightobj.departure_day,classtype="firstclass").count() or 0
            econo=-models.Order.objects.filter(flightnum=flightobj.flight_id,departure_day=flightobj.departure_day,classtype="econoclass").count() or 0
            # 无票可订的航班，直接移出列表
            if first==flightobj.first_class_num and econo==flightobj.economy_class_num:
                flight_list.remove(flightobj)
            else:
                firstclass.append(first)
                econoclass.append(econo)
        return render(request,"search_result.html",{"combined_list":zip(flight_list,firstclass,econoclass)})
    return redirect('/app02/login/')

# 订票的网页
def book(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        # url中获取传递的航班号
        flight_num = request.GET.get("flightid")
        # gyz写的登录系统中在session中确定了参数 用户账号
        user_id = request.session.get("userid")
        # 这里给出乘机人的列表返回给网站
        passenger_list = models.Passenger.objects.filter(user__userid=user_id)
        # 找到对应的航班号，按理来说只会找到一个，以防万一用了first
        flight_object = models.Flight.objects.filter(flight_id=flight_num).first()
        timerange=(flight_object.departure_time,flight_object.arrival_time)
        first=models.Order.objects.filter(flightnum=flight_object.flight_id,departure_day=flight_object.departure_day,classtype="firstclass").count()
        firstremain = flight_object.first_class_num -first
        econo=models.Order.objects.filter(flightnum=flight_object.flight_id,departure_day=flight_object.departure_day,classtype="econoclass").count()
        econoremain = flight_object.economy_class_num-econo
        error_info=""
        if request.method == "POST":
            # 获取时间，传递给订单系统中的“订票时间”
            cur_time = strftime("%Y-%m-%d %H:%M:%S")
            # 舱位
            class_type = request.POST.getlist("classtypes")
            # 这是乘机人复选框的返回结果，list中每一项都是选中的那一行的复选框value属性，这里我传递的value是作为主键的乘机人身份证号
            checkbox_list = request.POST.getlist("check_box_list")


            # 票数与时间冲突检查：

            bookfail=False
            for i, pass_idnum in enumerate(checkbox_list):
                # 票数
                if class_type[i]=="firstclass":
                    firstremain-=1
                    if firstremain<0:
                        error_info="头等舱数量不足"
                        bookfail=True
                        break
                elif class_type[i]=="econmclass":
                    econoremain-=1
                    if econoremain<0:
                        error_info = "经济舱数量不足"
                        bookfail = True
                        break
                else :
                    # 正常情况下不可能到达这里
                    error_info = "舱位类型有误"
                    bookfail = True
                    break

                # 时间
                # 根据乘机人身份证找到其相应订单列表
                ordered_list=models.Order.objects.filter(passid=pass_idnum,departure_day=flight_object.departure_day)
                for ordered in ordered_list:
                    # 根据订单的航班号找到相应航班(可能多个)
                    # Q所在一行表示查询条件包括：出发时刻在range内的 或 到达时刻在range内的
                    orderedflight_list=models.Flight.objects.filter(
                        Q(departure_time__range=timerange)|Q(arrival_time__range=timerange),
                        flight_id=ordered.flightnum,
                        departure_day=ordered.departure_day)
                    # 如果找到了就是时间冲突了
                    if orderedflight_list:
                        error_info = "身份证号为 %s 的乘客在该次航班时间段内已经有航行计划了"%pass_idnum
                        bookfail = True
                        break
                if bookfail:
                    break

            if bookfail:
                return render(request,"booking.html",{"passenger_list": passenger_list,"error_info":error_info})


            # 订票成功保存到数据库
            for i, pass_idnum in enumerate(checkbox_list):
                models.Order.objects.create(
                    userid=user_id,
                    flightnum=flight_num,
                    departure_day=flight_object.departure_day,
                    passid=pass_idnum,
                    classtype=class_type[i],
                    ordertime=cur_time
                )
            # 订票成功后转到订单列表
            return render(request, "booking_success.html")
        return render(request, "booking.html", {"passenger_list": passenger_list,"error_info":error_info})
    return redirect('/app02/login/')

# 订单列表网页
def order_list(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        user_id=request.session.get("userid")
        user_obj = models.User.objects.filter(userid=user_id).first()
        order_list=models.Order.objects.filter(userid=user_id).order_by('-ordertime')
        passenger_list = user_obj.passenger_set.all()
        passenger_id_list = [item.idnum for item in passenger_list]
        passenger_object_list = []
        for order_item in order_list:
            if order_item.passid in passenger_id_list:
                passenger_object_list.append(passenger_list[passenger_id_list.index(order_item.passid)])
        flight_list = []
        for order_item in order_list:
            flight_list.append(models.Flight.objects.filter(flight_id=order_item.flightnum,departure_day=order_item.departure_day).first())

        return render(request,"order_list.html",{'combined_list': zip(order_list,passenger_object_list,flight_list)})
    return redirect('/app02/login/')

def booking_success(request):
    return render(request,"booking_success.html")
# 退票网页
def refund(request):
    is_login = request.session.get("is_login", False)
    if is_login:
        order_id=request.GET.get("orderid")
        # 直接按订单号删除(?)数据库中用户订的票
        models.Order.objects.filter(id=order_id).delete()
        return render(request,"refunding.html")


def home_not(request):
    return render(request,"home_not.html")

def help(request):
    return render(request,"help.html")

def help_not(request):
    return render(request,"help_not.html")



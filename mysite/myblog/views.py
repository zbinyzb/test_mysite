from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from myblog.models import SiteInfo,Classes,Userinfo
# Create your views here.
#执行视图函数
def index(request):
    #在这里写入业务逻辑
    #获取所有数据并赋值变量,返回一个数据列表
    #站点基础信息
    siteinfo = SiteInfo.objects.all()[0]
    #菜单分类
    classes = Classes.objects.all()
    #用户列表
    userless = Userinfo.objects.all()

    #打包成字典(对象) "键名": 变量
    data = {
        "siteinfo":siteinfo,
        "classes":classes,
        "userless":userless
    }
    #render(请求头，模板，数据)
    return render(request,'index.html',data)

def classes(request):
    siteinfo = SiteInfo.objects.all()[0]
    classes = Classes.objects.all()
    #用户筛选列表
    try:
        choosed_id = request.GET['id']
        print(choosed_id)
        choosed = Classes.objects.filter(id=choosed_id)
        print(choosed)
    except:
        return redirect('/')
    
    if choosed:
        userless = Userinfo.objects.filter(belong=choosed[0])
    else:
        #保持代码的健康性
        userless = []
        #将错误搜索重定向回首页路由
        # return redirect('/')
        # data = {
        #     "value":"无结果"
        # }
        # return JsonResponse(data)
        # return HttpResponse('<h1>无结果</h1>')

    #键名保持一致，是为了契合for循环
    data = {
        "siteinfo":siteinfo,
        "classes":classes,
        "userless":userless
    }
    return render(request,'classes.html',data)
from django.shortcuts import render
from django.views import View


# Create your views here.
#注册视图
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

from  django.http.response import HttpResponseBadRequest
from  libs.captcha.captcha import captcha
from  django_redis import get_redis_connection
from  django.http import HttpResponse
class ImageCodeView(View):
    def get(self,request):
        # 1.接受前端传递过来的uuid
        uuid=request.GET.get('uuid')
        # 2.判断uuid是否获取到
        if uuid is None:
            return HttpResponseBadRequest('没有传递uuid')
        # 3.通过调用captcha 来生成图片验证码
        text,image=captcha.generate_captcha()
        # 4.将 图片内容保存到redis中
        #      uuid作为一个key，图片内容作为一个value同时我们还需要设置一个实效
        redis_conn = get_redis_connection('default')
        # key 设置为uuid
        # seconds 过期秒数  300（5分钟过期）
        # value  text
        redis_conn.setex('img:%s'%uuid,300,text)
        # 5.返回图片二进制
        return HttpResponse(image,content_type='image/jpeg')


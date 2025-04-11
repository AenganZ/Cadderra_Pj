from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'  # 홈 페이지 템플릿

class ChangePlanView(TemplateView):
    template_name = 'change_phone_plan.html'   # 요금제 가입하기 버튼

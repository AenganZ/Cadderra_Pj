from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

import openai
import requests
import logging
import random

logger = logging.getLogger(__name__)
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def service1(request):
    return render(request, 'ourservices/service1.html')

def chatbot(request):
    return render(request, 'ourservices/service2.html')

@csrf_exempt
def get_bot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        bot_response = generate_response(user_message)
        return JsonResponse({'message': bot_response})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_response(user_input):
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 CADDERRA라는 통신사의 요금제 추천 상담원입니다. 고객의 질문에 대해 간결, 정확하고 친절하게 답변하세요. 특정 분야 요금제에 대해 말하는 동안에는 다른 분야 요금제에 대한 문의가 오기 전까지 절대 언급하지 마. 타 통신사를 절대 언급하지 마세요. 요금제 목록은 휴대폰 요금제, IPTV 요금제, 인터넷 요금제 등이며, 그 내용은 다음과 같습니다. 뭐라카더라 플러스 알파: 특별 모바일 서비스(통화녹음 포함), 11,000원, SMS 알림 + CADDERRA 앱,웹 관리 / 뭐라카더라 베이직: 기본 서비스(미수신 발신번호 정보), 8,800원, SMS 알림 제공 / 5GX 플래티넘: 무제한, 무제한, 기본 제공, 125,000원, 5G 최고 속도, 해외 로밍 데이터 무제한, 클라우드 100GB, 콘텐츠 이용권, Netflix 광고형 스탠다드와 Wavve 콘텐츠 팩 모두 이용, C 멤버십 VIP 혜택, 스마트기기 2회선 이용요금 무료 / 5GX 프리미엄: 무제한, 무제한, 기본 제공, 109,000원, 5G 고속, 해외 로밍 데이터 20GB, 클라우드 50GB, 콘텐츠 이용권, Netflix 광고형 스탠다드와 Wavve 콘텐츠 팩 모두 이용, C 멤버십 VIP 혜택, 스마트기기 1회선 이용요금 무료 / 5GX 프라임플러스: 무제한, 무제한, 기본 제공, 99,000원, 5G 고속, 해외 로밍 데이터 15GB, 클라우드 30GB, Netflix 광고형 스탠다드 또는 Wavve 콘텐츠 팩 중 1개 선택 이용, C 멤버십 VIP 혜택 / 5GX 프라임: 무제한, 무제한, 기본 제공, 89,000원, 5G 고속, 해외 로밍 데이터 10GB, 클라우드 30GB, C 멤버십 VIP 혜택 / 5GX 레귤러플러스: 250GB, 무제한, 기본 제공, 79,000원, 5G 고속, 해외 로밍 데이터 5GB, 클라우드 30GB, C 멤버십 혜택 / 5GX 레귤러: 110GB, 무제한, 기본 제공, 69,000원, 5G 고속, 해외 로밍 데이터 3GB, 클라우드 30GB, C 멤버십 혜택 / 베이직플러스 75GB업: 99GB, 무제한, 기본 제공, 68,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 베이직플러스 50GB업: 74GB, 무제한, 기본 제공, 66,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 베이직플러스 30GB업: 54GB, 무제한, 기본 제공, 64,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 베이직플러스 13GB업: 37GB, 무제한, 기본 제공, 62,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 베이직플러스: 24GB, 무제한, 기본 제공, 59,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 베이직: 11GB, 무제한, 기본 제공, 49,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택 / 슬림: 15GB, 무제한, 기본 제공, 55,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택 / 컴팩트플러스: 8GB, 무제한, 기본 제공, 45,000원, LTE 속도, C 멤버십 혜택 / 컴팩트: 6GB, 무제한, 기본 제공, 39,000원, LTE 속도, C 멤버십 혜택 / 0 청년 109: 무제한, 무제한, 기본 제공, 109,000원, 5G 고속, 해외 로밍 데이터 20GB, 클라우드 50GB, 콘텐츠 이용권, Netflix 광고형 스탠다드와 Wavve 콘텐츠 팩 모두 이용, C 멤버십 VIP 혜택, 스마트기기 1회선 이용요금 무료 / 0 청년 99: 무제한, 무제한, 기본 제공, 99,000원, 5G 고속, 해외 로밍 데이터 15GB, 클라우드 30GB, Netflix 광고형 스탠다드 또는 Wavve 콘텐츠 팩 중 1개 선택 이용, C 멤버십 VIP 혜택 / 0 청년 89: 무제한, 무제한, 기본 제공, 89,000원, 5G 고속, 해외 로밍 데이터 10GB, 클라우드 30GB, C 멤버십 VIP 혜택 / 0 청년 79: 300GB, 무제한, 기본 제공, 79,000원, 5G 고속, 해외 로밍 데이터 5GB, 클라우드 30GB, C 멤버십 혜택 / 0 청년 69: 160GB, 무제한, 기본 제공, 69,000원, 5G 고속, 해외 로밍 데이터 3GB, 클라우드 30GB, C 멤버십 혜택 / 0 청년 59 100GB업: 136GB, 무제한, 기본 제공, 68,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 0 청년 59 60GB업: 96GB, 무제한, 기본 제공, 66,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 0 청년 59 36GB업: 72GB, 무제한, 기본 제공, 64,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 0 청년 59 15GB업: 51GB, 무제한, 기본 제공, 62,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 0 청년 59: 36GB, 무제한, 기본 제공, 59,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 0 청년 49: 15GB, 무제한, 기본 제공, 49,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택 / 0 청년 43: 8GB, 무제한, 기본 제공, 43,000원, LTE 속도, C 멤버십 혜택 / 0 청년 37: 6GB, 무제한, 기본 제공, 37,000원, LTE 속도, C 멤버십 혜택 / 0틴 5G: 9GB, 무제한, 기본 제공, 45,000원, 5G 속도, 청소년 전용 혜택, C 멤버십 혜택 / 5G ZEM플랜 퍼펙트: 4GB, 무제한, 기본 제공, 36,000원, 5G 속도, 청소년 전용 혜택, C 멤버십 혜택 / 5G ZEM플랜 베스트: 2GB, 무제한, 기본 제공, 26,000원, 5G 속도, 청소년 전용 혜택, C 멤버십 혜택 / 5G 시니어 A형: 10GB, 무제한, 기본 제공, 45,000원, 5G 속도, 시니어 전용 혜택, C 멤버십 혜택 / 5G 시니어 B형: 9GB, 무제한, 기본 제공, 44,000원, 5G 속도, 시니어 전용 혜택, C 멤버십 혜택 / 5G 시니어 C형: 8GB, 무제한, 기본 제공, 42,000원, 5G 속도, 시니어 전용 혜택, C 멤버십 혜택 / 5G 행복누리 레귤러: 110GB, 무제한, 기본 제공, 69,000원, 5G 고속, 복지 요금제 혜택, C 멤버십 혜택 / 5G 행복누리 슬림: 11GB, 무제한, 기본 제공, 55,000원, 5G 속도, 복지 요금제 혜택, C 멤버십 혜택 / LTEData함께쓰기1G: 1GB, -, -, 26,400원, 데이터 공유 / LTEData함께쓰기Basic: 함께쓰기, -, -, 9,900원, 데이터 공유 / ZEM플랜 라이트: 300MB, CADDERRA 지정 회선 무제한, 기본 제공, 15,400원, 청소년 전용 혜택, C 멤버십 혜택 / C플랜 맥스: 무제한, 무제한, 기본 제공, 100,000원, 5G 최고 속도, 해외 로밍 데이터 무제한, 클라우드 100GB, Netflix 광고형 스탠다드와 Wavve 콘텐츠 팩 모두 이용, C 멤버십 VIP 혜택, 스마트기기 2회선 이용요금 무료 / C플랜 스페셜: 150GB, 무제한, 기본 제공, 79,000원, 5G 고속, 해외 로밍 데이터 10GB, 클라우드 50GB, Netflix 광고형 스탠다드 또는 Wavve 콘텐츠 팩 중 1개 선택 이용, C 멤버십 VIP 혜택 / C플랜 에센스: 100GB, 무제한, 기본 제공, 69,000원, 5G 고속, 해외 로밍 데이터 5GB, 클라우드 30GB, C 멤버십 혜택 / C플랜 안심4G: 4GB, 무제한, 기본 제공, 50,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택 / C플랜 안심2.5G: 2.5GB, 무제한, 기본 제공, 43,000원, LTE 속도, C 멤버십 혜택 / C플랜 세이브: 1.5GB, 무제한, 기본 제공, 33,000원, LTE 속도, C 멤버십 혜택 / 0플랜 라지: 100GB, 무제한, 기본 제공, 69,000원, 5G 고속, 해외 로밍 데이터 5GB, 클라우드 30GB, C 멤버십 혜택 / 0플랜 미디엄: 6GB, 무제한, 기본제공, 50,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택 / 0플랜 스몰: 2GB, 무제한, 기본제공, 33,000원, LTE 속도, C 멤버십 혜택 / 0플랜 슈퍼히어로: 100GB, 무제한, 기본제공, 55,000원, 5G 고속, 해외 로밍 데이터 3GB, 클라우드 30GB, C 멤버십 혜택 / 0플랜 히어로: 6GB, 무제한, 기본제공, 33,000원, LTE 속도, C 멤버십 혜택 / 0티플랜 라지: 100GB, 무제한, 기본제공, 69,000원, 5G 고속, 해외 로밍 데이터 5GB, 클라우드 30GB, C 멤버십 혜택 / 0티플랜 미디엄플러스: 12GB, 무제한, 기본제공, 59,000원, LTE 속도, 해외 로밍 데이터 2GB, C 멤버십 혜택 / 0티플랜 미디엄: 6GB, 무제한, 기본제공, 45,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택 / 0티플랜 스몰: 2.5GB, 무제한, 기본제공, 33,000원, LTE 속도, C 멤버십 혜택 / ZEM플랜 베스트: 2GB, 무제한, 기본제공, 26,000원, LTE 속도, 청소년 전용 혜택, C 멤버십 혜택 / 다이렉트LTE 35: 5GB, 무제한, 기본제공, 35,000원, LTE 속도, C 멤버십 혜택 / 다이렉트LTE 30: 2.5GB, 무제한, 기본제공, 30,000원, LTE 속도, C 멤버십 혜택 / 다이렉트LTE 22: 1.8GB, 무제한, 기본제공, 22,000원, LTE 속도, C 멤버십 혜택 / C플랜 시니어 스페셜: 160GB, 무제한, 기본제공, 79,000원, 5G 고속, 해외 로밍 데이터 10GB, 클라우드 50GB, Netflix 광고형 스탠다드 또는 Wavve 콘텐츠 팩 중 1개 선택 이용, C 멤버십 VIP 혜택, 시니어 전용 혜택 / C플랜 시니어 에센스: 110GB, 무제한, 기본제공, 69,000원, 5G 고속, 해외 로밍 데이터 5GB, 클라우드 30GB, C 멤버십 혜택, 시니어 전용 혜택 / C플랜 시니어 완심4.5G: 4.5GB, 무제한, 기본제공, 50,000원, LTE 속도, 해외 로밍 데이터 1GB, C 멤버십 혜택, 시니어 전용 혜택 / C플랜 시니어 안심2.8G: 2.8GB, 무제한, 기본제공, 43,000원, LTE 속도, C 멤버십 혜택, 시니어 전용 혜택 / C플랜 시니어 세이브: 1.7GB, 무제한, 기본제공, 33,000원, LTE 속도, C 멤버십 혜택, 시니어 전용 혜택 / band 데이터 퍼펙트S: 16GB, 무제한, 기본제공, 75,900원, LTE 속도, 해외 로밍 데이터 3GB, 클라우드 30GB, C 멤버십 혜택 / band 데이터 퍼펙트: 11GB, 무제한, 기본제공, 65,890원, LTE 속도, 해외 로밍 데이터 2GB, 클라우드 30GB, C 멤버십 혜택 || IPTV 요금제 // C tv All: 모든 채널, 16,500원, HAEJU 음성 리모컨 무료 / C tv 스탠다드: 인기 채널, 13,200원, 무료 VOD 쿠폰 제공 / C tv 이코노미: 드라마·예능 중심, 9,900원, 월 1회 영화 VOD 무료 / 넷플릭스 조합상품: C tv+넷플릭스, 31,000원, 넷플릭스 스탠다드 HD 포함 / C tv pop: 저렴한 IPTV, 7,700원, 무료 실시간 채널 제공 / C tv 미니: 지상파·종편 기본, 6,600원, 월 1회 VOD 할인 쿠폰 / AI 스피커형 셋톱박스: 음성인식 기능, 6,600원, HAEJU 서비스 무료 이용 / Smart 3 셋톱박스: HAEJU·유튜브·구글 어시스턴트, 4,400원, 유튜브 프리미엄 3개월 무료 / Apple TV 4K: Apple TV+C tv, 6,600원, Apple TV+ 3개월 무료 / C tv air: 태블릿용 C tv, 8,800원, 모바일 데이터 1GB 추가 제공 / AI Sound Max: B&O 사운드, 8,800원, 고음질 음원 서비스 3개월 무료 / Smart 3 mini 셋톱박스: WiFi 연결 미니 셋톱박스, 4,400원, 클라우드 저장공간 50GB 제공 / 친환경 스마트 리모컨: C tv·스마트TV 통합 리모컨, 450원, 배터리 교체 서비스 1년 무료 || 인터넷 요금제 // 광랜인터넷 와이파이: 100M, Giga WiFi, 23,100원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가라이트인터넷 와이파이: 500M, Giga WiFi, 34,100원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가인터넷 와이파이: 1G, Giga WiFi, 39,600원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가인터넷멀티 와이파이 1.7G: 2.5G(최대 1G/기기), Giga WiFi, 44,000원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 광랜인터넷: 100M, 22,000원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가라이트인터넷: 500M, 33,000원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가인터넷: 1G, 38,500원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가인터넷멀티: 2.5G(최대 1G/기기), 44,000원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 기가프리미엄X2.5: 2.5G, 44,000원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB, 프리미엄 와이파이 / 기가프리미엄X5: 5G, 55,000원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB, 프리미엄 와이파이 / 기가프리미엄X10: 10G, 82,500원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB, 프리미엄 와이파이 / 원격케어 광랜: 100M, Giga WiFi, PC/스마트폰 원격점검, 24,750원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 원격케어 기가라이트: 500M, Giga WiFi, PC/스마트폰 원격점검, 35,750원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 원격케어 기가: 1G, Giga WiFi, PC/스마트폰 원격점검, 41,250원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 모두안심 광랜: 100M, Giga WiFi, 모두안심 서비스, 24,750원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 모두안심 기가라이트: 500M, Giga WiFi, 모두안심 서비스, 35,750원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 모두안심 기가: 1G, Giga WiFi, 모두안심 서비스, 41,250원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 파워백신 광랜: 100M, Giga WiFi, 백신, 단말 자동 최적화, 24,750원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 파워백신 기가라이트: 500M, Giga WiFi, 백신, 단말 자동 최적화, 35,750원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 파워백신 기가: 1G, Giga WiFi, 백신, 단말 자동 최적화, 41,250원, 3년 약정+초고속 결합, C멤버십 혜택, 클라우드 100GB / 가디언: 유해사이트 차단, 3,300원, 3년 약정+초고속 결합, C멤버십 혜택 / 세이퍼 플러스: 백신, 기기 자동 최적화, 3,300원, 3년 약정+초고속 결합, C멤버십 혜택 / 원스톱: PC/스마트폰 원격 관리, 3,300원, 3년 약정+초고속 결합, C멤버십 혜택 / IP공유서비스: 다중 PC 인터넷 접속, 5,500원, 3년 약정+초고속 결합, C멤버십 혜택 / 외국인 인터넷 요금할인: 1년 약정 시 추가 할인, 상세참조, 3년 약정+초고속 결합, C멤버십 혜택"},
                {"role": "user", "content": user_input}
            ]
        )
        
        bot_response = response.choices[0].message.content
        return bot_response.strip()
    except Exception as e:
        logger.error(f"Error in generate_response: {e}")
        return get_fallback_response()


def get_fallback_response():
    fallback_responses = [
        "죄송합니다. 귀하의 질문을 정확히 이해하지 못했습니다. 요금제에 대해 더 자세히 물어보시겠습니까?",
        "요금제 추천을 원하시나요? 어떤 종류의 요금제에 관심이 있으신지 말씀해 주세요.",
        "고객님의 사용 패턴에 대해 좀 더 자세히 알려주시면 적합한 요금제를 추천해 드릴 수 있습니다.",
        "특정 기능이나 서비스에 대해 궁금하신 점이 있으신가요?",
        "CADDERRA의 다양한 요금제 중 어떤 것에 관심이 있으신가요? 데이터, 통화, 또는 특별 혜택 등에 대해 물어보실 수 있습니다.",
    ]
    return random.choice(fallback_responses)

def service3(request):
    return render(request, 'ourservices/service3.html')

def service4(request):
    return render(request, 'ourservices/service4.html')

def service5(request):
    return render(request, 'ourservices/service5.html')

def service6(request):
    return render(request, 'ourservices/service6.html')

def terms(request):
    return render(request, 'law/이용약관.html')

def privacy(request):
    return render(request, 'law/개인정보처리방침.html')

def privacy_details(request):
    return render(request, 'law/개인정보이용내역.html')

def check_login(request):
    if request.user.is_authenticated:
        return redirect('user_usage_history')
    else:
        return render(request, 'common/login.html')

@login_required
def user_usage_history(request):
    # 실제 환경에서는 이 부분을 API 호출이나 다른 데이터 소스에서 데이터를 가져오는 로직으로 대체해야 합니다.
    # 여기서는 예시 데이터를 생성합니다.
    current_time = timezone.now()
    usage_history = [
        {
            'date': current_time - timedelta(days=i),
            'service': f"서비스 {i+1}",
            'details': f"서비스 {i+1}에 대한 상세 내용입니다."
        } for i in range(5)  # 최근 5개의 가상 이용 내역
    ]
    
    context = {
        'usage_history': usage_history,
    }
    return render(request, 'law/user_usage_history.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # 이메일 전송
        try:
            send_mail(
                subject,
                f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                email,  # 발신자 이메일
                ['recipient@example.com'],  # 수신자 이메일
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent. Thank you!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        
        return redirect('contact')  # 'index'는 메인 페이지의 URL 이름입니다.
    
    return render(request, 'index.html')
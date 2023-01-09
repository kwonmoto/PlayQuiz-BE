from rest_framework_simplejwt.tokens import RefreshToken

import urllib.request
import requests
import tempfile
from datetime import datetime
from playquiz.settings import get_secret


class Util:

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    
    def find_ip_country(user_ip):
        serviceKey = get_secret("WHOIS_KEY")
        url = "http://apis.data.go.kr/B551505/whois/ip_address?serviceKey=" + serviceKey + "&query=" + user_ip + "&answer=json"
        request = urllib.request.urlopen(url).read().decode("utf-8")
        return dict(eval(request))["response"]["whois"]["countryCode"]
    
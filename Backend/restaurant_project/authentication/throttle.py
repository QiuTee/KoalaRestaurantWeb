from rest_framework.throttling import UserRateThrottle
from .helpers.helpers import verify_recaptcha


class UserLoginRateThrottle(UserRateThrottle):
    scope = "loginAttempts"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}

    def check_captcha(self, request):
        recaptcha_token = request.data.get("recaptcha")
        if recaptcha_token:
            return verify_recaptcha(recaptcha_token)
        else:
            return False

    def allow_request(self, request, view):
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if self.check_captcha(request):
            return True

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()

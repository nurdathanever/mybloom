from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return "/"

    def get_template_names(self, request):
        return ["account/socialaccount/login.html"]
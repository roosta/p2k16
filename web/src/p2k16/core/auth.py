import flask_login
from p2k16.core import account_management
from p2k16.core.models import Account

login_manager = flask_login.LoginManager()


class AuthenticatedAccount(flask_login.UserMixin):
    def __init__(self, account, circles):
        self.id = account.id
        self.account = account
        self.circles = circles


@login_manager.user_loader
def account_loader(account_id):
    import flask
    flask.current_app.logger.info("Loading account")

    try:
        account = Account.find_account_by_id(account_id)

        if account is None:
            return

        circles = account_management.get_circles_for_account(account.id)

        return AuthenticatedAccount(account, circles)
    finally:
        flask.current_app.logger.info("account loaded")


@login_manager.request_loader
def request_loader(request):
    account_id = request.form.get("account")

    if account_id is None:
        return

    return account_loader(account_id)

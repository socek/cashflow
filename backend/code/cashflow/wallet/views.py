from sapp.decorators import WithContext
from sapp.plugins.pyramid.controller import RestfulController

from cashflow import app
from cashflow.application.forms import FormSerializer
from cashflow.auth.view_mixins import AuthMixin
from cashflow.wallet.drivers import WalletReadDriver
from cashflow.wallet.drivers import WalletWriteDriver
from cashflow.wallet.schemas import CreateWalletSchema
from cashflow.wallet.schemas import WalletSchema


class WalletListView(RestfulController, AuthMixin):
    permission = 'edit'

    @WithContext(app, args=['dbsession'])
    def get(self, dbsession):
        schema = WalletSchema()
        driver = WalletReadDriver(dbsession)
        wallets = driver.list_for_user(user_id=self.get_user_id())
        data = schema.dump(wallets, many=True).data

        return dict(elements=data)

    @WithContext(app, args=['dbsession'])
    def post(self, dbsession):
        wallet_wd = WalletWriteDriver(dbsession)
        form = FormSerializer(CreateWalletSchema())
        form.parse_json(self.request.json_body)

        result = {}

        if form.validate():
            data = form.fields()
            data['user_id'] = self.get_user().id

            wallet = wallet_wd.create(**data)
            result['uuid'] = wallet.uuid
        else:
            self.request.response.status_code = 400

        result['form'] = form.fullform
        return result



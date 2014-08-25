from pecan import make_app, conf
from pecan.hooks import TransactionHook
from model import model


def setup_app(config):

    model.init_model()
    app_conf = dict(config.app)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks = [
        TransactionHook(
            model.start,
            model.start_read_only,
            model.commit,
            model.rollback,
            model.clear)],
        **app_conf
    )
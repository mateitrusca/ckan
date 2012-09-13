from ckan.new_authz import is_authorized
from ckan.logic import NotAuthorized
from ckan.authz import Authorizer

class MockDeprecatedAuth(object):
    """
    MockDeprecatedAuth
    """

    def __init__(self):
        self.functions = {}
        self._load()

    def _load(self):
        for auth_module_name in ['get', 'create', 'update','delete']:
            module_path = 'ckan.logic.auth.deprecated.%s' % (auth_module_name,)
            try:
                module = __import__(module_path)
            except ImportError,e:
                continue

            for part in module_path.split('.')[1:]:
                module = getattr(module, part)

            for key, v in module.__dict__.items():
                if not key.startswith('_'):
                    self.functions[key] = v


    def check_access(self,action, context, data_dict):

        if Authorizer.is_sysadmin(unicode(context['user'])):
            return {'success': True}

        logic_authorization = self.functions[action](context, data_dict)
        if not logic_authorization['success']:
            msg = logic_authorization.get('msg','')
            raise NotAuthorized(msg)
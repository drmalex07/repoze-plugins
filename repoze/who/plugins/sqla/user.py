import logging
import sqlalchemy
from zope.interface import implementer
from repoze.who.interfaces import (IAuthenticator, IMetadataProvider)
from repoze.who.utils import resolveDotted
from sqlalchemy import orm

from .interfaces import IUserPassword

@implementer(IAuthenticator)
@implementer(IMetadataProvider)
class UserPlugin(object):

    @classmethod
    def make_plugin(plugin_cls, **kwargs):
       '''Instantiate a plugin

       Example configuration:

       [plugin:modeled_user]
       use = repoze.who.plugins.sqla.user:make_plugin
       user_cls = helloworld.model:User
       session_factory = helloworld.model:Session
       login_attribute = email

       '''
        
       user_cls = resolveDotted(kwargs['user_cls'])
       if not IUserPassword.implementedBy(user_cls):
           raise ValueError('%s does not implement IUserPassword' % (user_cls))

       session_factory = resolveDotted(kwargs['session_factory'])
       if not callable(session_factory):
           raise ValueError('The session factory should be callable!')

       login_attribute = kwargs.get('login_attribute')
       
       return plugin_cls(user_cls, session_factory, login_attribute)
    
    def __init__(self, user_cls, session_factory, login_attribute='login'):
        self.user_cls = user_cls
        self.session_factory = session_factory
        self.login_attribute = str(login_attribute)
        
        self.log = logging.getLogger(__name__)
        return

    #
    # IAuthenticator interface
    #

    def authenticate(self, environ, identity):
        '''Check supplied credentials
        
        Expects param `identity` to be a dict of posted values for ('login', 'password')
        Return a non-empty username if credentials are valid.
        '''
        
        try:
            login = identity['login']
            password = identity['password']
        except KeyError:
            return None
        
        login_attribute = self.login_attribute

        session = self.session_factory()
        q = session.query(self.user_cls)
        qf = {login_attribute: login}
        try:
            matched_user = q.filter_by(**qf).one()
        except orm.exc.NoResultFound:
            return None

        if matched_user.check_password(password):
            return getattr(matched_user, login_attribute)

        return None

    #
    # IMetadataProvider interface
    #

    def add_metadata(self, environ, identity):
        '''
        Provides arbitrary dict-based metadata for every authenticated request
        '''

        login_attribute = self.login_attribute
        
        session = self.session_factory()
        q = session.query(self.user_cls)
        qf = {login_attribute: identity['repoze.who.userid']}
        user = q.filter_by(**qf).one()
        
        identity['user'] = user
        
        return          

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))

def make_plugin(**kwargs):
    return UserPlugin.make_plugin(**kwargs)


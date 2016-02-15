from zope.interface import Interface

class IUserPassword(Interface):

    def check_password(password):
        '''Check if the supplied password matches with user's one.'''


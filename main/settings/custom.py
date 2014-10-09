import sys


DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mainiti',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}


# You can set test environment specific settings as above
if 'test' in sys.argv:
    # forces the usage of sqlite3 in-memory
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

    # speed up tests by using syncdb instead of migrate to create tables
    SOUTH_TESTS_MIGRATE = False

    # speed up tests by ignoring external ref calls (static outside project)
    IGNORE_EXTERNAL_REFS = True

    # manage.py help test to know which args are available
    #NOSE_ARGS = ['--stop', '--nocapture']

EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
MASTER_PASSWORD = 'admin'

CEDENTE_CARTEIRA = '02'
CEDENTE_CONTA = '468426-5'
CEDENTE_AGENCIA = '0373'
CEDENTE = 'TURBOSYS SOLUCOES PARA INTERNET LTDA'
CEDENTE_DOCUMENTO = '11675270000119'
CEDENTE_CIDADE = 'Curitiba'
CEDENTE_UF = 'PR'
CEDENTE_LOGRADOURO = 'Reynaldo Contin 214'
CEDENTE_BAIRRO = 'Umbara'
CEDENTE_CEP = '81930557'
BILLET_PREFIX = '2'

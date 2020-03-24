HS256_SECRET = 'my-secret'
with open('tests/rs256_public.pem') as f:
    RS256_PUBLIC_KEY = f.read()
with open('tests/es256_public.pem') as f:
    ES256_PUBLIC_KEY = f.read()

ISSUER = 'my-issuer'
AUDIENCE = 'my-audience'

SIMPLE_TOKEN = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3OD'
                'kwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.EpM5XB'
                'zTJZ4J8AfoJEcJrjth8pfH28LWdjLo90sYb9g')
#
HS256_TOKEN = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw'
               'IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJteS'
               '1pc3N1ZXIiLCJhdWQiOiJteS1hdWRpZW5jZSJ9.3tdUmN0CHJtzPGftyIyI7_V'
               'nf0UjGJOrHrJgvaLnM50')
#
RS256_TOKEN = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw'
               'IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJte'
               'S1pc3N1ZXIiLCJhdWQiOiJteS1hdWRpZW5jZSJ9.BOsqxog3rBgwnGZZMf6vH'
               'LsrHvSbnWlYrtfxitL_MsU6isNl0Jex6smVP_PQbnOtQztEhjXM0KM7FQj9w1'
               '4likwr3sOs6Za0CLnF5R81KFgTkiZ6ky0QhK_00qyNUzyJwoZnfbk9N5zkwE9'
               'aRGWIKmS_q8h_jCHvmm0_3NGrzZJKuu3Gpd_zzn3ZdsJoH7yp-MYHQgM9fcJf'
               'OBsJMpSySGewZgRVKzNlwUDITsf08wh8uwyAL2usLqaLzbZgSmwPX3IRxNnBX'
               'EStkSVVXT-7t6O7EgIKSCL14ekv3QA_FVC2nG68mU_GsJX1-U1DKMarIvliqT'
               'gOf9y-Mfe565TClQ')
#
ES256_TOKEN = ('eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw'
               'IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJte'
               'S1pc3N1ZXIiLCJhdWQiOiJteS1hdWRpZW5jZSJ9.nHfsY_oIyLOZSLZiwGiqZ'
               'B3KAWJpgNJVYmqMWlF0S9mxd3u1LeNxXYzyzR184NQ7PWJ1_JOQGUIBd7czaR'
               'kBlQ')

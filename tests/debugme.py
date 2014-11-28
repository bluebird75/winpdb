import sys, os, atexit

def is_py3k():
    return sys.version_info[0] >= 3

if is_py3k():
    def u(s): return s
else:
    def u(s): return unicode(s)

prefix = 'DEBUGME: '
pathprefix = os.path.join( os.path.dirname( __file__) )

def step(t):
    print( prefix + u(t) )
    f = open( '%s/%s' % (pathprefix, t ), 'w' )
    f.write(t+'\n')
    f.close()

def f1( t ):
    step( 'f1' )
    v = f4( f2('a'), f3('b'), 'titi' )
    v = f2( '33' )
    v += f3( 'abcd' )  # BP1
    return v

def f2( t ):
    step( 'f2' )
    t += '33'
    return t

def f3( t ):
    step( 'f3' )
    t += '17'
    return t

def f4( a, b, t ):
    t += '2'
    return t

def atexit_handler():
    step('atexit')

if __name__ == '__main__':
    atexit.register( atexit_handler )
    step('start')
    f1( 'toto' )
    step('done')

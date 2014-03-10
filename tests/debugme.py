import sys

def is_py3k():
    return sys.version_info[0] >= 3

if is_py3k():
    def u(s): return s
else:
    def u(s): return unicode(s)

prefix = 'DEBUGME: '

def step(t):
    print( prefix + u(t) )
    open( t, 'w' ).write(t+'\n')

def f1( t ):
    step( 'f1' )
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

if __name__ == '__main__':
    step('start')
    f1( 'toto' )
    step('done')

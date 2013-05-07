
prefix = 'DEBUGME: '

def step(t):
    print( prefix + unicode(t) )
    open( t, 'w' ).write(t+'\n')

def f1( t ):
    step( 'f1' )
    f2( 33 )
    f3( 'abcd' )

def f2( t ):
    step( 'f2' )

def f3( t ):
    step( 'f3' )

if __name__ == '__main__':
    f1( 'toto' )
    step('done')

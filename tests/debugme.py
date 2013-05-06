
prefix = 'DEBUGME: '
def disp(t):
    print( prefix + unicode(t) )

def f1( t ):
    disp(t)
    f2( 33 )
    f3( 'abcd' )

def f2( t ):
    disp(t)

def f3( t ):
    disp(t)

if __name__ == '__main__':
    f1( 'toto' )
    disp('Done')

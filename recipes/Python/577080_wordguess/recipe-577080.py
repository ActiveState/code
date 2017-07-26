import easygui
easygui.msgbox('"think of a word"')
n=easygui.choicebox("how many letters does it have?",
                  choices=['7',,'3','4','5','6'])
if n=='3':
    easygui.msgbox('in which row is your first letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your first letter this time?')
    #a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                               choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])

 
    easygui.msgbox('in which row  is your first letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m=x+z
    if m=='row 1row 1':
        m='A'
    if m=='row 1row 2':
        m='B'
    if m=='row 1row 3':
        m='C'
    if m=='row 1row 4':
        m='D'
    if m=='row 2row 1':
        m='E'
    if m=='row 2row 2':
        m='F'
    if m=='row 2row 3':
        m='G'
    if m=='row 2row 4':
        m='H'
    if m=='row 3row 1':
        m='I'
    if m=='row 3row 2':
        m='J'
    if m=='row 3row 3':
        m='K'
    if m=='row 3row 4':
        m='L'
    if m=='row 4row 1':
        m='M'
    if m=='row 4row 2':
        m='N'
    if m=='row 4row 3':
        m='O'
    if m=='row 4row 4':
        m='P'
    if m=='row 5row 1':
        m='Q'
    if m=='row 5row 2':
        m='R'
    if m=='row 5row 3':
        m='S'
    if m=='row 5row 4':
        m='T'
    if m=='row 6row 1':
        m='U'
    if m=='row 6row 2':
        m='V'
    if m=='row 6row 3':
        m='W'
    if m=='row 6row 4':
        m='X'

    easygui.msgbox('in which row is your second letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your second letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M" ,                                                                choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your second letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m_=x+z
    if m_=='row 1row 1':
        m_='A'
    if m_=='row 1row 2':
        m_='B'
    if m_=='row 1row 3':
        m_='C'
    if m_=='row 1row 4':
        m_='D'
    if m_=='row 2row 1':
        m_='E'
    if m_=='row 2row 2':
        m_='F'
    if m_=='row 2row 3':
        m_='G'
    if m_=='row 2row 4':
        m_='H'
    if m_=='row 3row 1':
        m_='I'
    if m_=='row 3row 2':
        m_='J'
    if m_=='row 3row 3':
        m_='K'
    if m_=='row 3row 4':
        m_='L'
    if m_=='row 4row 1':
        m_='M'
    if m_=='row 4row 2':
        m_='N'
    if m_=='row 4row 3':
        m_='O'
    if m_=='row 4row 4':
        m_='P'
    if m_=='row 5row 1':
        m_='Q'
    if m_=='row 5row 2':
        m_='R'
    if m_=='row 5row 3':
        m_='S'
    if m_=='row 5row 4':
        m_='T'
    if m_=='row 6row 1':
        m_='U'
    if m_=='row 6row 2':
        m_='V'
    if m_=='row 6row 3':
        m_='W'
    if m_=='row 6row 4':
        m_='X'
    easygui.msgbox('in which row is your third letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your third letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M"  ,                                                               choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your third letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__=x+z
    if m__=='row 1row 1':
        m__='A'
    if m__=='row 1row 2':
        m__='B'
    if m__=='row 1row 3':
        m__='C'
    if m__=='row 1row 4':
        m__='D'
    if m__=='row 2row 1':
        m__='E'
    if m__=='row 2row 2':
        m__='F'
    if m__=='row 2row 3':
        m__='G'
    if m__=='row 2row 4':
        m__='H'
    if m__=='row 3row 1':
        m__='I'
    if m__=='row 3row 2':
        m__='J'
    if m__=='row 3row 3':
        m__='K'
    if m__=='row 3row 4':
        m__='L'
    if m__=='row 4row 1':
        m__='M'
    if m__=='row 4row 2':
        m__='N'
    if m__=='row 4row 3':
        m__='O'
    if m__=='row 4row 4':
        m__='P'
    if m__=='row 5row 1':
        m__='Q'
    if m__=='row 5row 2':
        m__='R'
    if m__=='row 5row 3':
        m__='S'
    if m__=='row 5row 4':
        m__='T'
    if m__=='row 6row 1':
        m__='U'
    if m__=='row 6row 2':
        m__='V'
    if m__=='row 6row 3':
        m__='W'
    if m__=='row 6row 4':
        m__='X'
    easygui.msgbox('HERE COMES THE MAGIC,PRESS OK')
    easygui.msgbox('YOUR WORD IS')
    print m+m_+m__

if n=='4':
    easygui.msgbox('in which row is your first letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your first letter this time')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                              choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your first letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m=x+z
    if m=='row 1row 1':
        m='A'
    if m=='row 1row 2':
        m='B'
    if m=='row 1row 3':
        m='C'
    if m=='row 1row 4':
        m='D'
    if m=='row 2row 1':
        m='E'
    if m=='row 2row 2':
        m='F'
    if m=='row 2row 3':
        m='G'
    if m=='row 2row 4':
        m='H'
    if m=='row 3row 1':
        m='I'
    if m=='row 3row 2':
        m='J'
    if m=='row 3row 3':
        m='K'
    if m=='row 3row 4':
        m='L'
    if m=='row 4row 1':
        m='M'
    if m=='row 4row 2':
        m='N'
    if m=='row 4row 3':
        m='O'
    if m=='row 4row 4':
        m='P'
    if m=='row 5row 1':
        m='Q'
    if m=='row 5row 2':
        m='R'
    if m=='row 5row 3':
        m='S'
    if m=='row 5row 4':
        m='T'
    if m=='row 6row 1':
        m='U'
    if m=='row 6row 2':
        m='V'
    if m=='row 6row 3':
        m='W'
    if m=='row 6row 4':
        m='X'

    easygui.msgbox('in which row is your second letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your second letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your second letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m_=x+z
    if m_=='row 1row 1':
        m_='A'
    if m_=='row 1row 2':
        m_='B'
    if m_=='row 1row 3':
        m_='C'
    if m_=='row 1row 4':
        m_='D'
    if m_=='row 2row 1':
        m_='E'
    if m_=='row 2row 2':
        m_='F'
    if m_=='row 2row 3':
        m_='G'
    if m_=='row 2row 4':
        m_='H'
    if m_=='row 3row 1':
        m_='I'
    if m_=='row 3row 2':
        m_='J'
    if m_=='row 3row 3':
        m_='K'
    if m_=='row 3row 4':
        m_='L'
    if m_=='row 4row 1':
        m_='M'
    if m_=='row 4row 2':
        m_='N'
    if m_=='row 4row 3':
        m_='O'
    if m_=='row 4row 4':
        m_='P'
    if m_=='row 5row 1':
        m_='Q'
    if m_=='row 5row 2':
        m_='R'
    if m_=='row 5row 3':
        m_='S'
    if m_=='row 5row 4':
        m_='T'
    if m_=='row 6row 1':
        m_='U'
    if m_=='row 6row 2':
        m_='V'
    if m_=='row 6row 3':
        m_='W'
    if m_=='row 6row 4':
        m_='X'
    easygui.msgbox('in which row is your third letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your third letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M',                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your third letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__=x+z
    if m__=='row 1row 1':
        m__='A'
    if m__=='row 1row 2':
        m__='B'
    if m__=='row 1row 3':
        m__='C'
    if m__=='row 1row 4':
        m__='D'
    if m__=='row 2row 1':
        m__='E'
    if m__=='row 2row 2':
        m__='F'
    if m__=='row 2row 3':
        m__='G'
    if m__=='row 2row 4':
        m__='H'
    if m__=='row 3row 1':
        m__='I'
    if m__=='row 3row 2':
        m__='J'
    if m__=='row 3row 3':
        m__='K'
    if m__=='row 3row 4':
        m__='L'
    if m__=='row 4row 1':
        m__='M'
    if m__=='row 4row 2':
        m__='N'
    if m__=='row 4row 3':
        m__='O'
    if m__=='row 4row 4':
        m__='P'
    if m__=='row 5row 1':
        m__='Q'
    if m__=='row 5row 2':
        m__='R'
    if m__=='row 5row 3':
        m__='S'
    if m__=='row 5row 4':
        m__='T'
    if m__=='row 6row 1':
        m__='U'
    if m__=='row 6row 2':
        m__='V'
    if m__=='row 6row 3':
        m__='W'
    if m__=='row 6row 4':
        m__='X'
    easygui.msgbox('in which row is your fourth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fourth letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fourth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__q=x+z
    if m__q=='row 1row 1':
        m__q='A'
    if m__q=='row 1row 2':
        m__q='B'
    if m__q=='row 1row 3':
        m__q='C'
    if m__q=='row 1row 4':
        m__q='D'
    if m__q=='row 2row 1':
        m__q='E'
    if m__q=='row 2row 2':
        m__q='F'
    if m__q=='row 2row 3':
        m__q='G'
    if m__q=='row 2row 4':
        m__q='H'
    if m__q=='row 3row 1':
        m__q='I'
    if m__q=='row 3row 2':
        m__q='J'
    if m__q=='row 3row 3':
        m__q='K'
    if m__q=='row 3row 4':
        m__q='L'
    if m__q=='row 4row 1':
        m__q='M'
    if m__q=='row 4row 2':
        m__q='N'
    if m__q=='row 4row 3':
        m__q='O'
    if m__q=='row 4row 4':
        m__q='P'
    if m__q=='row 5row 1':
        m__q='Q'
    if m__q=='row 5row 2':
        m__q='R'
    if m__q=='row 5row 3':
        m__q='S'
    if m__q=='row 5row 4':
        m__q='T'
    if m__q=='row 6row 1':
        m__q='U'
    if m__q=='row 6row 2':
        m__q='V'
    if m__q=='row 6row 3':
        m__q='W'
    if m__q=='row 6row 4':
        m__q='X'
    easygui.msgbox('HERE COMES THE MAGIC,PRESS OK')
    easygui.msgbox('YOUR WORD IS')
    print m+m_+m__+m__q

if n=='5':
    easygui.msgbox('in which row is your first letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your first letter this time')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your first letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m=x+z
    if m=='row 1row 1':
        m='A'
    if m=='row 1row 2':
        m='B'
    if m=='row 1row 3':
        m='C'
    if m=='row 1row 4':
        m='D'
    if m=='row 2row 1':
        m='E'
    if m=='row 2row 2':
        m='F'
    if m=='row 2row 3':
        m='G'
    if m=='row 2row 4':
        m='H'
    if m=='row 3row 1':
        m='I'
    if m=='row 3row 2':
        m='J'
    if m=='row 3row 3':
        m='K'
    if m=='row 3row 4':
        m='L'
    if m=='row 4row 1':
        m='M'
    if m=='row 4row 2':
        m='N'
    if m=='row 4row 3':
        m='O'
    if m=='row 4row 4':
        m='P'
    if m=='row 5row 1':
        m='Q'
    if m=='row 5row 2':
        m='R'
    if m=='row 5row 3':
        m='S'
    if m=='row 5row 4':
        m='T'
    if m=='row 6row 1':
        m='U'
    if m=='row 6row 2':
        m='V'
    if m=='row 6row 3':
        m='W'
    if m=='row 6row 4':
        m='X'

    easygui.msgbox('in which row is your second letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your second letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your second letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m_=x+z
    if m_=='row 1row 1':
        m_='A'
    if m_=='row 1row 2':
        m_='B'
    if m_=='row 1row 3':
        m_='C'
    if m_=='row 1row 4':
        m_='D'
    if m_=='row 2row 1':
        m_='E'
    if m_=='row 2row 2':
        m_='F'
    if m_=='row 2row 3':
        m_='G'
    if m_=='row 2row 4':
        m_='H'
    if m_=='row 3row 1':
        m_='I'
    if m_=='row 3row 2':
        m_='J'
    if m_=='row 3row 3':
        m_='K'
    if m_=='row 3row 4':
        m_='L'
    if m_=='row 4row 1':
        m_='M'
    if m_=='row 4row 2':
        m_='N'
    if m_=='row 4row 3':
        m_='O'
    if m_=='row 4row 4':
        m_='P'
    if m_=='row 5row 1':
        m_='Q'
    if m_=='row 5row 2':
        m_='R'
    if m_=='row 5row 3':
        m_='S'
    if m_=='row 5row 4':
        m_='T'
    if m_=='row 6row 1':
        m_='U'
    if m_=='row 6row 2':
        m_='V'
    if m_=='row 6row 3':
        m_='W'
    if m_=='row 6row 4':
        m_='X'
    easygui.msgbox('in which row is your third letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your third letter this time?')
   # a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your third letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__=x+z
    if m__=='row 1row 1':
        m__='A'
    if m__=='row 1row 2':
        m__='B'
    if m__=='row 1row 3':
        m__='C'
    if m__=='row 1row 4':
        m__='D'
    if m__=='row 2row 1':
        m__='E'
    if m__=='row 2row 2':
        m__='F'
    if m__=='row 2row 3':
        m__='G'
    if m__=='row 2row 4':
        m__='H'
    if m__=='row 3row 1':
        m__='I'
    if m__=='row 3row 2':
        m__='J'
    if m__=='row 3row 3':
        m__='K'
    if m__=='row 3row 4':
        m__='L'
    if m__=='row 4row 1':
        m__='M'
    if m__=='row 4row 2':
        m__='N'
    if m__=='row 4row 3':
        m__='O'
    if m__=='row 4row 4':
        m__='P'
    if m__=='row 5row 1':
        m__='Q'
    if m__=='row 5row 2':
        m__='R'
    if m__=='row 5row 3':
        m__='S'
    if m__=='row 5row 4':
        m__='T'
    if m__=='row 6row 1':
        m__='U'
    if m__=='row 6row 2':
        m__='V'
    if m__=='row 6row 3':
         m__='W'
    if m__=='row 6row 4':
        m__='X'
    easygui.msgbox('in which row is your fourth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fourth letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M" ,                                                                choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fourth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__q=x+z
    if m__q=='row 1row 1':
        m__q='A'
    if m__q=='row 1row 2':
        m__q='B'
    if m__q=='row 1row 3':
        m__q='C'
    if m__q=='row 1row 4':
        m__q='D'
    if m__q=='row 2row 1':
        m__q='E'
    if m__q=='row 2row 2':
        m__q='F'
    if m__q=='row 2row 3':
        m__q='G'
    if m__q=='row 2row 4':
        m__q='H'
    if m__q=='row 3row 1':
        m__q='I'
    if m__q=='row 3row 2':
        m__q='J'
    if m__q=='row 3row 3':
        m__q='K'
    if m__q=='row 3row 4':
        m__q='L'
    if m__q=='row 4row 1':
        m__q='M'
    if m__q=='row 4row 2':
        m__q='N'
    if m__q=='row 4row 3':
        m__q='O'
    if m__q=='row 4row 4':
        m__q='P'
    if m__q=='row 5row 1':
        m__q='Q'
    if m__q=='row 5row 2':
        m__q='R'
    if m__q=='row 5row 3':
        m__q='S'
    if m__q=='row 5row 4':
        m__q='T'
    if m__q=='row 6row 1':
        m__q='U'
    if m__q=='row 6row 2':
        m__q='V'
    if m__q=='row 6row 3':
        m__q='W'
    if m__q=='row 6row 4':
        m__q='X'
    easygui.msgbox('in which row is your fifth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fifth letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fifth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__qq=x+z
    if m__qq=='row 1row 1':
        m__qq='A'
    if m__qq=='row 1row 2':
        m__qq='B'
    if m__qq=='row 1row 3':
        m__qq='C'
    if m__qq=='row 1row 4':
        m__qq='D'
    if m__qq=='row 2row 1':
        m__qq='E'
    if m__qq=='row 2row 2':
        m__qq='F'
    if m__qq=='row 2row 3':
        m__qq='G'
    if m__qq=='row 2row 4':
        m__qq='H'
    if m__qq=='row 3row 1':
        m__qq='I'
    if m__qq=='row 3row 2':
        m__qq='J'
    if m__qq=='row 3row 3':
        m__qq='K'
    if m__qq=='row 3row 4':
        m__qq='L'
    if m__qq=='row 4row 1':
        m__qq='M'
    if m__qq=='row 4row 2':
        m__qq='N'
    if m__qq=='row 4row 3':
        m__qq='O'
    if m__qq=='row 4row 4':
        m__qq='P'
    if m__qq=='row 5row 1':
        m__qq='Q'
    if m__qq=='row 5row 2':
        m__qq='R'
    if m__qq=='row 5row 3':
        m__qq='S'
    if m__qq=='row 5row 4':
        m__qq='T'
    if m__qq=='row 6row 1':
        m__qq='U'
    if m__qq=='row 6row 2':
        m__qq='V'
    if m__qq=='row 6row 3':
        m__qq='W'
    if m__qq=='row 6row 4':
        m__qq='X'
    easygui.msgbox('HERE COMES THE MAGIC,PRESS OK')
    easygui.msgbox('YOUR WORD IS')
    print m+m_+m__+m__q+m__qq

        
if n=='6':
    easygui.msgbox('in which row is your first letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your first letter this time')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M" ,                                                                choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your first letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m=x+z
    if m=='row 1row 1':
        m='A'
    if m=='row 1row 2':
        m='B'
    if m=='row 1row 3':
        m='C'
    if m=='row 1row 4':
        m='D'
    if m=='row 2row 1':
        m='E'
    if m=='row 2row 2':
        m='F'
    if m=='row 2row 3':
        m='G'
    if m=='row 2row 4':
        m='H'
    if m=='row 3row 1':
        m='I'
    if m=='row 3row 2':
        m='J'
    if m=='row 3row 3':
        m='K'
    if m=='row 3row 4':
        m='L'
    if m=='row 4row 1':
        m='M'
    if m=='row 4row 2':
        m='N'
    if m=='row 4row 3':
        m='O'
    if m=='row 4row 4':
        m='P'
    if m=='row 5row 1':
        m='Q'
    if m=='row 5row 2':
        m='R'
    if m=='row 5row 3':
        m='S'
    if m=='row 5row 4':
        m='T'
    if m=='row 6row 1':
        m='U'
    if m=='row 6row 2':
        m='V'
    if m=='row 6row 3':
        m='W'
    if m=='row 6row 4':
        m='X'

    easygui.msgbox('in which row is your second letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your second letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your second letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m_=x+z
    if m_=='row 1row 1':
        m_='A'
    if m_=='row 1row 2':
        m_='B'
    if m_=='row 1row 3':
        m_='C'
    if m_=='row 1row 4':
        m_='D'
    if m_=='row 2row 1':
        m_='E'
    if m_=='row 2row 2':
        m_='F'
    if m_=='row 2row 3':
        m_='G'
    if m_=='row 2row 4':
        m_='H'
    if m_=='row 3row 1':
        m_='I'
    if m_=='row 3row 2':
        m_='J'
    if m_=='row 3row 3':
        m_='K'
    if m_=='row 3row 4':
        m_='L'
    if m_=='row 4row 1':
        m_='M'
    if m_=='row 4row 2':
        m_='N'
    if m_=='row 4row 3':
        m_='O'
    if m_=='row 4row 4':
        m_='P'
    if m_=='row 5row 1':
        m_='Q'
    if m_=='row 5row 2':
        m_='R'
    if m_=='row 5row 3':
        m_='S'
    if m_=='row 5row 4':
        m_='T'
    if m_=='row 6row 1':
        m_='U'
    if m_=='row 6row 2':
        m_='V'
    if m_=='row 6row 3':
        m_='W'
    if m_=='row 6row 4':
        m_='X'
    easygui.msgbox('in which row is your third letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your third letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your third letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__=x+z
    if m__=='row 1row 1':
        m__='A'
    if m__=='row 1row 2':
        m__='B'
    if m__=='row 1row 3':
        m__='C'
    if m__=='row 1row 4':
        m__='D'
    if m__=='row 2row 1':
        m__='E'
    if m__=='row 2row 2':
        m__='F'
    if m__=='row 2row 3':
        m__='G'
    if m__=='row 2row 4':
        m__='H'
    if m__=='row 3row 1':
        m__='I'
    if m__=='row 3row 2':
        m__='J'
    if m__=='row 3row 3':
        m__='K'
    if m__=='row 3row 4':
        m__='L'
    if m__=='row 4row 1':
        m__='M'
    if m__=='row 4row 2':
        m__='N'
    if m__=='row 4row 3':
        m__='O'
    if m__=='row 4row 4':
        m__='P'
    if m__=='row 5row 1':
        m__='Q'
    if m__=='row 5row 2':
        m__='R'
    if m__=='row 5row 3':
        m__='S'
    if m__=='row 5row 4':
        m__='T'
    if m__=='row 6row 1':
        m__='U'
    if m__=='row 6row 2':
        m__='V'
    if m__=='row 6row 3':
         m__='W'
    if m__=='row 6row 4':
        m__='X'
    easygui.msgbox('in which row is your fourth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fourth letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fourth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__q=x+z
    if m__q=='row 1row 1':
        m__q='A'
    if m__q=='row 1row 2':
        m__q='B'
    if m__q=='row 1row 3':
        m__q='C'
    if m__q=='row 1row 4':
        m__q='D'
    if m__q=='row 2row 1':
        m__q='E'
    if m__q=='row 2row 2':
        m__q='F'
    if m__q=='row 2row 3':
        m__q='G'
    if m__q=='row 2row 4':
        m__q='H'
    if m__q=='row 3row 1':
        m__q='I'
    if m__q=='row 3row 2':
        m__q='J'
    if m__q=='row 3row 3':
        m__q='K'
    if m__q=='row 3row 4':
        m__q='L'
    if m__q=='row 4row 1':
        m__q='M'
    if m__q=='row 4row 2':
        m__q='N'
    if m__q=='row 4row 3':
        m__q='O'
    if m__q=='row 4row 4':
        m__q='P'
    if m__q=='row 5row 1':
        m__q='Q'
    if m__q=='row 5row 2':
        m__q='R'
    if m__q=='row 5row 3':
        m__q='S'
    if m__q=='row 5row 4':
        m__q='T'
    if m__q=='row 6row 1':
        m__q='U'
    if m__q=='row 6row 2':
        m__q='V'
    if m__q=='row 6row 3':
        m__q='W'
    if m__q=='row 6row 4':
        m__q='X'
    easygui.msgbox('in which row is your fifth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fifth letter this time?')

    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fifth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__qq=x+z
    if m__qq=='row 1row 1':
        m__qq='A'
    if m__qq=='row 1row 2':
        m__qq='B'
    if m__qq=='row 1row 3':
        m__qq='C'
    if m__qq=='row 1row 4':
        m__qq='D'
    if m__qq=='row 2row 1':
        m__qq='E'
    if m__qq=='row 2row 2':
        m__qq='F'
    if m__qq=='row 2row 3':
        m__qq='G'
    if m__qq=='row 2row 4':
        m__qq='H'
    if m__qq=='row 3row 1':
        m__qq='I'
    if m__qq=='row 3row 2':
        m__qq='J'
    if m__qq=='row 3row 3':
        m__qq='K'
    if m__qq=='row 3row 4':
        m__qq='L'
    if m__qq=='row 4row 1':
        m__qq='M'
    if m__qq=='row 4row 2':
        m__qq='N'
    if m__qq=='row 4row 3':
        m__qq='O'
    if m__qq=='row 4row 4':
        m__qq='P'
    if m__qq=='row 5row 1':
        m__qq='Q'
    if m__qq=='row 5row 2':
        m__qq='R'
    if m__qq=='row 5row 3':
        m__qq='S'
    if m__qq=='row 5row 4':
        m__qq='T'
    if m__qq=='row 6row 1':
        m__qq='U'
    if m__qq=='row 6row 2':
        m__qq='V'
    if m__qq=='row 6row 3':
        m__qq='W'
    if m__qq=='row 6row 4':
        m__qq='X'

    easygui.msgbox('in which row is your sixth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your sixth letter this time')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your sixth letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__qq_=x+z
    if m__qq_=='row 1row 1':
        m__qq_='A'
    if m__qq_=='row 1row 2':
        m__qq_='B'
    if m__qq_=='row 1row 3':
        m__qq_='C'
    if m__qq_=='row 1row 4':
        m__qq_='D'
    if m__qq_=='row 2row 1':
        m__qq_='E'
    if m__qq_=='row 2row 2':
        m__qq_='F'
    if m__qq_=='row 2row 3':
        m__qq_='G'
    if m__qq_=='row 2row 4':
        m__qq_='H'
    if m__qq_=='row 3row 1':
        m__qq_='I'
    if m__qq_=='row 3row 2':
        m__qq_='J'
    if m__qq_=='row 3row 3':
        m__qq_='K'
    if m__qq_=='row 3row 4':
        m__qq_='L'
    if m__qq_=='row 4row 1':
        m__qq_='M'
    if m__qq_=='row 4row 2':
        m__qq_='N'
    if m__qq_=='row 4row 3':
        m__qq_='O'
    if m__qq_=='row 4row 4':
        m__qq_='P'
    if m__qq_=='row 5row 1':
        m__qq_='Q'
    if m__qq_=='row 5row 2':
        m__qq_='R'
    if m__qq_=='row 5row 3':
        m__qq_='S'
    if m__qq_=='row 5row 4':
        m__qq_='T'
    if m__qq_=='row 6row 1':
        m__qq_='U'
    if m__qq_=='row 6row 2':
        m__qq_='V'
    if m__qq_=='row 6row 3':
        m__qq_='W'
    if m__qq_=='row 6row 4':
        m__qq_='X'
    easygui.msgbox('HERE COMES THE MAGIC,PRESS OK')
    easygui.msgbox('YOUR WORD IS')
    print m+m_+m__+m__q+m__qq+m__qq_

if n=='7':
    easygui.msgbox('in which row is your first letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your first letter this time')
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your first letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m=x+z
    if m=='row 1row 1':
        m='A'
    if m=='row 1row 2':
        m='B'
    if m=='row 1row 3':
        m='C'
    if m=='row 1row 4':
        m='D'
    if m=='row 2row 1':
        m='E'
    if m=='row 2row 2':
        m='F'
    if m=='row 2row 3':
        m='G'
    if m=='row 2row 4':
        m='H'
    if m=='row 3row 1':
        m='I'
    if m=='row 3row 2':
        m='J'
    if m=='row 3row 3':
        m='K'
    if m=='row 3row 4':
        m='L'
    if m=='row 4row 1':
        m='M'
    if m=='row 4row 2':
        m='N'
    if m=='row 4row 3':
        m='O'
    if m=='row 4row 4':
        m='P'
    if m=='row 5row 1':
        m='Q'
    if m=='row 5row 2':
        m='R'
    if m=='row 5row 3':
        m='S'
    if m=='row 5row 4':
        m='T'
    if m=='row 6row 1':
        m='U'
    if m=='row 6row 2':
        m='V'
    if m=='row 6row 3':
        m='W'
    if m=='row 6row 4':
        m='X'

    easygui.msgbox('in which row is your second letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your second letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M" ,                                                                choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your second letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m_=x+z
    if m_=='row 1row 1':
        m_='A'
    if m_=='row 1row 2':
        m_='B'
    if m_=='row 1row 3':
        m_='C'
    if m_=='row 1row 4':
        m_='D'
    if m_=='row 2row 1':
        m_='E'
    if m_=='row 2row 2':
        m_='F'
    if m_=='row 2row 3':
        m_='G'
    if m_=='row 2row 4':
        m_='H'
    if m_=='row 3row 1':
        m_='I'
    if m_=='row 3row 2':
        m_='J'
    if m_=='row 3row 3':
        m_='K'
    if m_=='row 3row 4':
        m_='L'
    if m_=='row 4row 1':
        m_='M'
    if m_=='row 4row 2':
        m_='N'
    if m_=='row 4row 3':
        m_='O'
    if m_=='row 4row 4':
        m_='P'
    if m_=='row 5row 1':
        m_='Q'
    if m_=='row 5row 2':
        m_='R'
    if m_=='row 5row 3':
        m_='S'
    if m_=='row 5row 4':
        m_='T'
    if m_=='row 6row 1':
        m_='U'
    if m_=='row 6row 2':
        m_='V'
    if m_=='row 6row 3':
        m_='W'
    if m_=='row 6row 4':
        m_='X'
    easygui.msgbox('in which row is your third letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your third letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your third letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__=x+z
    if m__=='row 1row 1':
        m__='A'
    if m__=='row 1row 2':
        m__='B'
    if m__=='row 1row 3':
        m__='C'
    if m__=='row 1row 4':
        m__='D'
    if m__=='row 2row 1':
        m__='E'
    if m__=='row 2row 2':
        m__='F'
    if m__=='row 2row 3':
        m__='G'
    if m__=='row 2row 4':
        m__='H'
    if m__=='row 3row 1':
        m__='I'
    if m__=='row 3row 2':
        m__='J'
    if m__=='row 3row 3':
        m__='K'
    if m__=='row 3row 4':
        m__='L'
    if m__=='row 4row 1':
        m__='M'
    if m__=='row 4row 2':
        m__='N'
    if m__=='row 4row 3':
        m__='O'
    if m__=='row 4row 4':
        m__='P'
    if m__=='row 5row 1':
        m__='Q'
    if m__=='row 5row 2':
        m__='R'
    if m__=='row 5row 3':
        m__='S'
    if m__=='row 5row 4':
        m__='T'
    if m__=='row 6row 1':
        m__='U'
    if m__=='row 6row 2':
        m__='V'
    if m__=='row 6row 3':
         m__='W'
    if m__=='row 6row 4':
        m__='X'
    easygui.msgbox('in which row is your fourth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fourth letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fourth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__q=x+z
    if m__q=='row 1row 1':
        m__q='A'
    if m__q=='row 1row 2':
        m__q='B'
    if m__q=='row 1row 3':
        m__q='C'
    if m__q=='row 1row 4':
        m__q='D'
    if m__q=='row 2row 1':
        m__q='E'
    if m__q=='row 2row 2':
        m__q='F'
    if m__q=='row 2row 3':
        m__q='G'
    if m__q=='row 2row 4':
        m__q='H'
    if m__q=='row 3row 1':
        m__q='I'
    if m__q=='row 3row 2':
        m__q='J'
    if m__q=='row 3row 3':
        m__q='K'
    if m__q=='row 3row 4':
        m__q='L'
    if m__q=='row 4row 1':
        m__q='M'
    if m__q=='row 4row 2':
        m__q='N'
    if m__q=='row 4row 3':
        m__q='O'
    if m__q=='row 4row 4':
        m__q='P'
    if m__q=='row 5row 1':
        m__q='Q'
    if m__q=='row 5row 2':
        m__q='R'
    if m__q=='row 5row 3':
        m__q='S'
    if m__q=='row 5row 4':
        m__q='T'
    if m__q=='row 6row 1':
        m__q='U'
    if m__q=='row 6row 2':
        m__q='V'
    if m__q=='row 6row 3':
        m__q='W'
    if m__q=='row 6row 4':
        m__q='X'
    easygui.msgbox('in which row is your fifth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row is your fifth letter this time?')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row is your fifth letter this time?')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__qq=x+z
    if m__qq=='row 1row 1':
        m__qq='A'
    if m__qq=='row 1row 2':
        m__qq='B'
    if m__qq=='row 1row 3':
        m__qq='C'
    if m__qq=='row 1row 4':
        m__qq='D'
    if m__qq=='row 2row 1':
        m__qq='E'
    if m__qq=='row 2row 2':
        m__qq='F'
    if m__qq=='row 2row 3':
        m__qq='G'
    if m__qq=='row 2row 4':
        m__qq='H'
    if m__qq=='row 3row 1':
        m__qq='I'
    if m__qq=='row 3row 2':
        m__qq='J'
    if m__qq=='row 3row 3':
        m__qq='K'
    if m__qq=='row 3row 4':
        m__qq='L'
    if m__qq=='row 4row 1':
        m__qq='M'
    if m__qq=='row 4row 2':
        m__qq='N'
    if m__qq=='row 4row 3':
        m__qq='O'
    if m__qq=='row 4row 4':
        m__qq='P'
    if m__qq=='row 5row 1':
        m__qq='Q'
    if m__qq=='row 5row 2':
        m__qq='R'
    if m__qq=='row 5row 3':
        m__qq='S'
    if m__qq=='row 5row 4':
        m__qq='T'
    if m__qq=='row 6row 1':
        m__qq='U'
    if m__qq=='row 6row 2':
        m__qq='V'
    if m__qq=='row 6row 3':
        m__qq='W'
    if m__qq=='row 6row 4':
        m__qq='X'

    easygui.msgbox('in which row is your sixth letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your sixth letter this time')
    #a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your sixth letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__qq_=x+z
    if m__qq_=='row 1row 1':
        m__qq_='A'
    if m__qq_=='row 1row 2':
        m__qq_='B'
    if m__qq_=='row 1row 3':
        m__qq_='C'
    if m__qq_=='row 1row 4':
        m__qq_='D'
    if m__qq_=='row 2row 1':
        m__qq_='E'
    if m__qq_=='row 2row 2':
        m__qq_='F'
    if m__qq_=='row 2row 3':
        m__qq_='G'
    if m__qq_=='row 2row 4':
        m__qq_='H'
    if m__qq_=='row 3row 1':
        m__qq_='I'
    if m__qq_=='row 3row 2':
        m__qq_='J'
    if m__qq_=='row 3row 3':
        m__qq_='K'
    if m__qq_=='row 3row 4':
        m__qq_='L'
    if m__qq_=='row 4row 1':
        m__qq_='M'
    if m__qq_=='row 4row 2':
        m__qq_='N'
    if m__qq_=='row 4row 3':
        m__qq_='O'
    if m__qq_=='row 4row 4':
        m__qq_='P'
    if m__qq_=='row 5row 1':
        m__qq_='Q'
    if m__qq_=='row 5row 2':
        m__qq_='R'
    if m__qq_=='row 5row 3':
        m__qq_='S'
    if m__qq_=='row 5row 4':
        m__qq_='T'
    if m__qq_=='row 6row 1':
        m__qq_='U'
    if m__qq_=='row 6row 2':
        m__qq_='V'
    if m__qq_=='row 6row 3':
        m__qq_='W'
    if m__qq_=='row 6row 4':
        m__qq_='X'

    easygui.msgbox('in which row is your seventh letter?')
    x=easygui.choicebox("1.A B C D                                                                       2.E F G H                                                                      3.I J K L                                                                       4.  M N O P                                                                       5.  Q R S T                                                                      6.   U V W X",                                                                  choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    easygui.msgbox('in which row  is your seventh letter this time')
   # a=easygui.choicebox('1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M'                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])
    a=easygui.choicebox("1.Q W E R                                                                       2.T U I O                                                                       3.P A S D                                                                       4.F G H J                                                                       5.K L X C                                                                       6.V B N M",                                                                 choices=['row 1','row 2','row 3','row 4','row 5','row 6'])


    easygui.msgbox('in which row  is your seventh letter this time')
    z=easygui.choicebox("1.A E I M Q U                                                                   2.B F J N R V                                                                  3.C G K O S W                                                                   4.  D H L P T X",                                                                                                                                                                                                                                                                                                                                                       choices=['row 1','row 2','row 3','row 4'])
    m__qq_x=x+z
    if m__qq_x=='row 1row 1':
        m__qq_x='A'
    if m__qq_x=='row 1row 2':
        m__qq_x='B'
    if m__qq_x=='row 1row 3':
        m__qq_x='C'
    if m__qq_x=='row 1row 4':
        m__qq_x='D'
    if m__qq_x=='row 2row 1':
        m__qq_x='E'
    if m__qq_x=='row 2row 2':
        m__qq_x='F'
    if m__qq_x=='row 2row 3':
        m__qq_x='G'
    if m__qq_x=='row 2row 4':
        m__qq_x='H'
    if m__qq_x=='row 3row 1':
        m__qq_x='I'
    if m__qq_x=='row 3row 2':
        m__qq_x='J'
    if m__qq_x=='row 3row 3':
        m__qq_x='K'
    if m__qq_x=='row 3row 4':
        m__qq_x='L'
    if m__qq_x=='row 4row 1':
        m__qq_x='M'
    if m__qq_x=='row 4row 2':
        m__qq_x='N'
    if m__qq_x=='row 4row 3':
        m__qq_x='O'
    if m__qq_x=='row 4row 4':
        m__qq_x='P'
    if m__qq_x=='row 5row 1':
        m__qq_x='Q'
    if m__qq_x=='row 5row 2':
        m__qq_x='R'
    if m__qq_x=='row 5row 3':
        m__qq_x='S'
    if m__qq_x=='row 5row 4':
        m__qq_x='T'
    if m__qq_x=='row 6row 1':
        m__qq_x='U'
    if m__qq_x=='row 6row 2':
        m__qq_x='V'
    if m__qq_x=='row 6row 3':
        m__qq_x='W'
    if m__qq_x=='row 6row 4':
        m__qq_x='X'
    easygui.msgbox('HERE COMES THE MAGIC,PRESS OK')
    easygui.msgbox('YOUR WORD IS')
    print m+m_+m__+m__q+m__qq+m__qq_+m__qq_x
    
    
    
    
    
    
    
    

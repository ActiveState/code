from Tkinter import *
import tkMessageBox as MB
import win32ui
import win32print
import win32con

root = Tk()
root.option_add('*Font',('Courier New', 12))

def onPrint():
    MB.showinfo('FYI','Make sure your printer is turned on and ready!\nThen press OK ;-)\n\nTested with hp f340')
    l = [(canvas.type(obj),canvas.coords(obj)) for obj in canvas.find_all()]
    print l
    print_canvas(l)

def print_canvas(coord_list, scale=20):
    '''Print canvas from list of coords for each canvas.object'''
    moves = []
    for obj in coord_list:
        if obj[0] == 'rectangle':
            #moves.append(('rectangle@: ', obj[1]))
            tlc, trc, blc, brc = (obj[1][0], obj[1][1]),(obj[1][2], obj[1][1]), (obj[1][0],obj[1][3]), (obj[1][2],obj[1][3])
            moves.append('dc.MoveTo((scale*%d, scale*-%d))' %(int(tlc[0]), int(tlc[1])))
            moves.append('dc.LineTo((scale*%d, scale*-%d))' %(int(blc[0]), int(blc[1])))
            moves.append('dc.LineTo((scale*%d, scale*-%d))' %(int(brc[0]), int(brc[1])))
            moves.append('dc.LineTo((scale*%d, scale*-%d))' %(int(trc[0]), int(trc[1])))
            moves.append('dc.LineTo((scale*%d, scale*-%d))' %(int(tlc[0]), int(tlc[1])))

        elif obj[0] == 'line':
            #moves.append(('line@: ', obj[1]))
            moves.append('dc.MoveTo((scale*%d, scale*-%d))' %(int(obj[1][0]), int(obj[1][1])))
            moves.append('dc.LineTo((scale*%d, scale*-%d))' %(int(obj[1][2]), int(obj[1][3])))
            
        elif obj[0] == 'polygon':
            #moves.append(('polygon@: ', obj[1]))
            start = 0
            temp = []
            for y in range(1, len(obj[1])+1, 2):
                temp.append( (obj[1][start], obj[1][y]) )
                start += 2
            sc = temp[0]
            ec = temp[1]
            if sc != ec:
                temp.append(sc)#close the polygon
            moves.append('dc.MoveTo((scale*%d, scale*-%d))' %(int(temp[0][0]), int(temp[0][1])))
            for x in temp[1:]:
                moves.append('dc.LineTo((scale*%d, scale*-%d))' %(int(x[0]), int(x[1])))
                
        elif obj[0] == 'arc':
            # draw curve to printer ???
            pass
        elif obj[0] == 'oval':
            # draw curve to printer ???
            pass
        else:
            pass
    for x in moves:
        print x
    try:
        print '\n\n--- Starting Print ---'
        dc = win32ui.CreateDC()
        dc.CreatePrinterDC(win32print.GetDefaultPrinter())
        dc.SetMapMode(win32con.MM_TWIPS) #1440 per inch
        dc.StartDoc('draw line')
        pen = win32ui.CreatePen(0, int(scale), 0L)
        dc.SelectObject(pen)
        for x in moves:
            exec(x)
        dc.EndDoc()
    except:
        print '\n\n!!! Print Failed !!!'
        

canvas = Canvas(root, bg='white')
canvas.pack()
Button(root, text="== Print Canvas Now ==", fg='red', command=onPrint).pack()

canvas.create_rectangle(310,10,325,100)
canvas.create_rectangle(330,10,345,100)
canvas.create_rectangle(350,10,365,100)
canvas.create_line(370,10,370,100)
canvas.create_polygon(200,150, 250,150, 250,250, 200,250)
canvas.create_polygon(135,38, 64,38, 29,100, 64,161, 135,161, 170,100)

root.mainloop()

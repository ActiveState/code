import Tkinter
import tkFileDialog

def main():
    global X, Y
    X, Y = 0, 0
    root = Tkinter.Tk()
    root.withdraw()
    root.resizable(False, False)
    root.title('Tiled Video Player')
    image = get_image()
    screen = Tkinter.Canvas(root, width=320, height=240, background='red', highlightthickness=0)
    screen.pack()
    screen.create_image(800, 600, image=image)
    screen.after(100, update, screen)
    root.deiconify()
    root.mainloop()

def get_image():
    try:
        filename = tkFileDialog.askopenfilename(title='Tiled Video Player', filetypes=['{Tiled Video} .gif'])
        assert filename
        image = Tkinter.PhotoImage(file=filename)
        assert (1600, 1200) == (image.width(), image.height())
        return image
    except:
        raise SystemExit

def update(screen):
    global X, Y
    screen.after(100, update, screen)
    X += 1
    if X == 5:
        X = 0
        Y += 1
        if Y == 5:
            Y = 0
            screen.move(1, 1280, 960)
        else:
            screen.move(1, 1280, -240)
    else:
        screen.move(1, -320, 0)

if __name__ == '__main__':
    main()

import time
class ascii:
    def __init__(self):
        self.clear()
    def clear():
        print "\n"*1000
    def pause(i):
        time.sleep(i)
    def roll_film(film, repi=1):
        for k in range(1, repi):
            for j in film:
                print j
                pause(1)
                clear()
            clear()
    def example():
        listf=['.  ',  ' . ', '  .']
        roll_film(listf, 4)
    def create_film(film):
        return film
class Txt_sprite:
    def __init__(self, surface, pic, ssl):
        self.screen=surface
        self.start_location=ssl
        self.image=pic
        self.screen[self.start_location]=self.image
        self.cur_loc=self.start_location
    def move(self, new_loc):
        self.screen[self.cur_loc]=' '
        self.screen[new_loc]=self.image
        self.cur_loc=new_loc
    def hide(self):
        self.screen[self.cur_loc]=' '
    def show(self):
        self.screen[self.cur_loc]=self.image
    def checkin(self, obj_loc):
        if self.cur_loc == obj_loc:
            return True
        else:
            return False
    def change_pic(self, new):
        self.image=new

def test_1():
    a=Ascii()
    screen=a.create_screen()
    sprite=Txt_sprite(screen, 'O', 0)
    x1=0
    x2=1
    hit=0
    while True:
        render(screen)
        a.pause(0.1)
        a.clear()
        if sprite.cur_loc == 19:
            hit=1
        elif sprite.cur_loc == 0:
            hit=0

        if hit == 0:
            sprite.move(x2)
        
            x1=x1+1
            x2=x2+1
        else:
            sprite.move(x1)
            x1=x1-1
            x2=x2-1
if __name__ == "__main__":
    a=ascii()
    a.example()
    

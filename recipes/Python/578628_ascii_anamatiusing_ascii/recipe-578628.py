import ascii
def bounce_ball():
    ball="o"
    a=ascii()
    film1=["_\no\n\n\n\n\n\n_", "_\n\no\n\n\n\n\n_", "_\n\n\no\n\n\n\n_",
           "_\n\n\n\no\n\n\n_", "_\n\n\n\n\no\n\n_", "_\n\n\n\n\n\no\n_"]
    filmb=["_\no\n\n\n\n\n\n_", "_\n\no\n\n\n\n\n_", "_\n\n\no\n\n\n\n_",
          "_\n\n\n\no\n\n\n_", "_\n\n\n\n\no\n\n_", "_\n\n\n\n\n\no\n_"]
    filmb=filmb[::-1]
    main=True
    while main:
        a.roll_film(film1, 2)
        a.roll_film(filmb, 2)
        

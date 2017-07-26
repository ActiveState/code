if __name__ == "__main__":
  mylist=list()
  mylist.append(0)
  mylist.append(1)
  mylist.append(2) 
  seclist=mylist
  seclist[2] = ’X’
  seclist
  [0, 1, ’X’]
  mylist
  [0, 1, 2]

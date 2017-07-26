#storage options:
# 0 = open read-only, most recently committed contents
# 1 = open in exclusive read-write mode
# 2 = open in "commit-extend" mode

main='test.mk';aside='test.mka'

#initalize
if not os.path.exists(main):
    print 'initalizing'
    db = metakit.storage(main, 1)
    db.getas("a[i:S]")
    db.commit()
    dba = metakit.storage(aside, 1)
    db.aside(dba)
    del db
    del dba

#commits w/extend do not 
#change old read
old_read = metakit.storage(main, 0)
old_reada = metakit.storage(aside, 0)
old_read.aside(old_reada)

vw = old_read.view("a")
old_len=len(vw)
print 'old length=',len(vw)

#now do commits with extend on aside file
#main is read-only aside is commit-extend
db = metakit.storage(main, 0)
dba = metakit.storage(aside, 2)
db.aside(dba)

vw = db.view("a")
vw.append(i=str(time.asctime()))
vw.append(i=str(time.asctime()))
db.commit()
dba.commit()
del db
del dba

#a new read should see the update
#extended in the aside file
new_read = metakit.storage(main, 0)
new_reada = metakit.storage(aside, 0)
new_read.aside(new_reada)

vw = new_read.view('a')
print "new length(should be %i)="%(old_len+2),len(vw)

#the old view should not be changed
vw = old_read.view('a')
print "old length(should still be %i)="%(old_len),len(vw)

#empty aside into main
#this is unsafe what extend enables
#you to do, is to control when
#to do this operation
empty_aside=1
if empty_aside:
    print 'Empty aside into main:',
    print 'not safe for readers!'
    db = metakit.storage(main, 1)
    dba = metakit.storage(aside, 1)
    db.aside(dba)
    db.commit(1)
    main_only = metakit.storage(main, 0)
    vw=main_only.view('a')
    print 'main now has',len(vw)
    del main_only

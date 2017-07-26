def timeAsrfc822 ( theTime ) :

    import rfc822
    return rfc822 . formatdate ( rfc822 . mktime_tz ( rfc822 . parsedate_tz ( theTime . strftime ( "%a, %d %b %Y %H:%M:%S" ) ) ) )

if __name__ == "__main__" :

    import datetime
    print timeAsrfc822 ( datetime . datetime . now ( ) )
    

There is a way to tell if we're actually in the script
which was directly launched.

Just like in Python there is:

if __name__ == '__main__':
    pass

...in PHP it looks like this:

if (basename($argv[0]) == basename(__FILE__)) {
    main();
}

I'm using this trick with PHPUnit testing:

// Test
if (basename($argv[0]) == basename(__FILE__)) {
    include substr(__FILE__, 0, -4) . 'Test.php';
}

Very, very useful.

Have a fun,
Mirek Rusin, Poland, Rzeszow

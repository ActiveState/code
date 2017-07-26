mynamespace = {};
(function() {
    //...

    this.__defineGetter__("my_expensive_attr", function() {
        var value = _do_expensive_calculation();
        /* Replace getter with the calculated value, so only bother checking the first time. */
        delete this.my_expensive_attr;
        this.my_expensive_attr = value;
        return value;
    });
    
    //...
}).apply(mynamespace);

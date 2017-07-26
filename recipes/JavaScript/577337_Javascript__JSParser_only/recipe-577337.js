/**
 * jObject.toJson - JSON Parser
 */
Object.prototype.toJson = function() {
    var tmp = '{';
	/* {"property1":"value1", "property2":"value2"} */    
    for (i in this) {
        if (this[i] != this.toJson) {
            tmp = tmp + '"' + i + '":"' + this[i] + '",';
        }
    }

    tmp = tmp.substring(0, (tmp.length - 1)) + '}';

    return tmp;
}

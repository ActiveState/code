# /* ================== */
# /* text_compressor.js */
# /* ================== */

function compress(string)
{
	// Get the unique characters and numeric base.
	var unique = create_set(string);
	var base = unique.length;
	// Create a key that will encode data properly.
	shuffle(unique);
	var mapping = create_dict(unique);
	while (!mapping[string[string.length - 1]])
	{
		shuffle(unique);
		mapping = create_dict(unique);
	}
	// Create a compressed numeric representation.
	var value = BigInteger();
	for (var place = 0; place < string.length; place++)
	{
		var multiple = BigInteger(base).pow(place);
		var product = BigInteger(mapping[string[place]]).multiply(multiple);
		value = value.add(product);
	}
	// Return the number as a string with the table.
	return [array_to_string(decode(value)), unique.join("")];
}

function create_set(string)
{
	var set = new Object();
	for (var index = 0; index < string.length; index++)
	{
		set[string[index]] = 0;
	}
	var array = new Array();
	for (var value in set)
	{
		array.push(value);
	}
	return array;
}

function shuffle(array)
{
	var range = array.length - 1;
	for (var index = 0; index < array.length; index++)
	{
		var destination = Math.floor(Math.random() * range);
		if (destination >= index)
		{
			destination++;
		}
		var temporary = array[destination];
		array[destination] = array[index];
		array[index] = temporary;
	}
}

function create_dict(array)
{
	var dict = new Object();
	for (var index = 0; index < array.length; index++)
	{
		dict[array[index]] = index;
	}
	return dict;
}

function decode(number)
{
	// Change a number into a string.
	var array = new Array();
	while (!number.isZero())
	{
		var answer = number.divRem(256);
		number = answer[0];
		array.push(answer[1]);
	}
	return array;
}

function array_to_string(array)
{
	for (var index = 0; index < array.length; index++)
	{
		array[index] = String.fromCharCode(array[index]);
	}
	return array.join("");
}

function decompress(string, key)
{
	// Get the numeric value of the string.
	var number = encode(string);
	// Find the numeric base and prepare storage.
	var base = key.length;
	var array = new Array();
	// Decode the value into the original string.
	while (!number.isZero())
	{
		var answer = number.divRem(base);
		number = answer[0];
		array.push(key[answer[1]]);
	}
	// Return the "string" as a bytes object.
	return array.join("");
}

function encode(string)
{
	// Change a string into a number.
	assert(string.length > 0 && string[string.length - 1] != String.fromCharCode(0), "String has ambiguous value!");
	var value = BigInteger();
	for (var shift = 0; shift < string.length; shift++)
	{
		var multiple = BigInteger(256).pow(shift);
		var product = BigInteger(string[shift].charCodeAt()).multiply(multiple);
		value = value.add(product);
	}
	return value;
}

function assert(okay, error)
{
	if (!okay)
	{
		alert(error);
		throw new Error(error);
	}
}

# /* ======== */
# /* Test.htm */
# /* ======== */

<html>
    <head>
        <title>Text Compressor</title>
        <script type="text/javascript" src="biginteger.js"></script>
        <script type="text/javascript" src="text_compressor.js"></script>
        <script type="text/javascript">
//<![CDATA[
            var example = "Hello, world! This is a simple test. What do you think of it so far? It probably needs more text. The key was 26 characters long, the data was 40 characters long, and the original string was 68 characters long. Having a longer string should allow for greater compression at the expense of (most likely) a longer key and lower compression ratio. The approximation was off so much after adding the length of the data and table (key) together along with one (1) for the value of a length field; I decided to make this string much longer in the hope of decreasing the error. Since this program is not very dynamic and only needs to be run once, having a long run time is not much of a problem. It certainly takes much longer to run now, and the ratios are considerably closer as well. Hopefully, anyone who might run this experiment will have the patience to let it run to completion. Well, that ends it.";
            
            function start()
            {
                document.getElementById("output").innerHTML = "Running compression test ...";
                setTimeout("test();", 10);
            }

            function test()
            {
                var lines = new Array();
                lines.push("Uncompressed size = " + example.length);
                var data = compress(example);
                lines.push("Compressed size = " + data[0].length);
                lines.push("Table size = " + data[1].length);
                lines.push("Approximate compression ratio = log(" + data[1].length + ") / log(256) = " +(100 * Math.log(data[1].length) / Math.log(256)) + "%");
                lines.push("Real compression ratio (data) = " + data[0].length + " / " + example.length + " = " + (100 * data[0].length / example.length) + "%");
                var total_length = data[0].length + data[1].length + 1;
                lines.push("Real compression ratio (total) = " + total_length + " / " + example.length + " = " + (100 * total_length / example.length) + "%");
                var original = decompress(data[0], data[1]);
                lines.push("Decompression of the data was " + (original == example ? "" : "not ") + "successful.");
                lines.push("The original text is displayed below:");
                lines.push("<hr />");
                lines.push(original);
                document.getElementById("output").innerHTML = lines.join("<br />");
            }
//]]>
        </script>
    </head>
    <body onload="setTimeout('start();', 1000);">
        <h1>Results</h1>
        <hr />
        <div id="output" />
    </body>
</html>

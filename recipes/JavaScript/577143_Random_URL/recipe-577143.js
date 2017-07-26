<script type="text/javascript">
function checkUrl(theURL) 
{
    var request = false;
    //Firefox and Netscape
    if (window.XMLHttpRequest) 
    {
        request = new XMLHttpRequest;
    }
    //IE
    else if (window.ActiveXObject) 
    {
        request = new ActiveXObject("Microsoft.XMLHttp");
    }
    
    if (request) 
    {
        request.open("GET", theURL);
        request.onreadystatechange = function() 
        {
            if (request.status == 200 && request.readyState == 4)
            {
                //page is there
                return true;
            }
            else if (request.status == 404) 
            {
                //page is not there
                return false;
            }
        }
        request.send(null);
    }
}

do
{
    //ping www.google.com => 64.233.167.147
    var ip0=Math.floor(Math.random()*256);
    var ip1=Math.floor(Math.random()*256);
    var ip2=Math.floor(Math.random()*256);
    var ip3=Math.floor(Math.random()*256);

    theURL="http://"+ip0+"."+ip1+"."+ip2+"."+ip3+"/";
}
while(checkUrl(theURL)==false);

window.location=theURL;
</script>

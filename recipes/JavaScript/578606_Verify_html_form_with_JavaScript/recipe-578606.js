function validateForm(str)
	{
		// first name is required
		var fn=document.forms[str]["first_name"].value;
		if (fn == "")
		{
  		  alert("Please Fill In First name");
		  return false;
		}
	
		// last name is required
		var fn=document.forms[str]["last_name"].value;
		if (fn == "")
		{
  		  alert("Please Fill In Last name");
		  return false;
		}
		// verify email if provided
		var em=document.forms[str]["email"].value;
		if (em != "") {
	    	var atpos=em.indexOf("@");
	    	var dotpos=em.lastIndexOf("."); 
			if (atpos<1 || dotpos<atpos+2 || dotpos+2>=em.length)
			  {
		    	alert("You have entered an invalid e-mail address");
			    return false;
			  }
		}
	}

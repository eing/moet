<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Test results</title>
</head>
<body>
    <p>
    <h3> Test Results </h3>
        <jsp:include page="results-android-emulator-5554.log" />
        
        <h3> Log file </h3>
        <!-- <jsp:include page="target/android-emulator-5554/adb.log" /> -->
        <a href="target/android-emulator-5554/adb.log">Adb log</a>
        <p>
            <hr>
            <p>
                <h3> Device screenshots</h3>
                
            </p>
            
           <%@ page language="java" import="java.io.File,java.util.*" errorPage="" %> 
<% 
	String filePath = "../webapps/MoetServlet/target/android-emulator-5554/";
    String path = "target/android-emulator-5554/";
	 File file = new File(filePath);
		if (file.exists())
		{
	      String[] fileList=file.list();
	      String filename;
	     for( int i=0; i < fileList.length; i++) 
	     { 
	    	filename = fileList[i];
	    	if (filename.contains("png") && (!filename.contains("_")))
	    	{
	        	out.println("<img src=\"" +  path + filename + "\" title=\"" + filename + "\" />"); 
	        	out.println(filename); 
	     	}
	     }
		}
%> 
 
</body>
</html>
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Mobile Remote Testing</title>
</head>
<body>
    <form name="moet" action="MoetServlet" method="Get">
		<p><h2>Android Launch Pad</h2>
		<input type="hidden" name="device" value="android">
		<input type="hidden" name="log" value="on">
		
		<p>
		<b>Tests &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</b>
        <input type="radio" name="testname" value="acceptance" checked> Acceptance BATS&nbsp;
		<input type="radio" name="testname" value="functional"> All functional tests
		
		<p>
		<b>OS &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</b>
		<input type="radio" name="os" value="2.3" checked> 2.3 Gingerbread&nbsp;
		<input type="radio" name="os" value="2.2"> 2.2 Fryo&nbsp;
		<input type="radio" name="os" value="1.6"> 1.6 Donut&nbsp;

		<p>
		<b>Resolution&nbsp;</b>
		<input type="radio" name="resolution" value="r240x320"> 240x320&nbsp;
		<input type="radio" name="resolution" value="r320x480" checked>320x480&nbsp;
		<input type="radio" name="resolution" value="r480x800"> 480x800&nbsp;
		<input type="radio" name="resolution" value="r854"> 480x854&nbsp;
		<input type="radio" name="resolution" value="r1280"> 800x1280&nbsp;
		
		<p>
		<b>Device &nbsp; &nbsp; &nbsp; &nbsp;</b>
		<input type="radio" name="deviceid" value="emulator" checked> Emulator&nbsp;
		<input type="radio" name="deviceid" value="device"> Device
				
		<p>
		<input type="submit" value="SUBMIT"/>
    </form> 
</body>
</html>

package com.intuit.moet;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.Writer;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class MoetServlet
 */
public class MoetServlet extends HttpServlet 
{
	private static final long serialVersionUID = 988801410507816192L;

	protected static final String ACCEPTANCE_TEST = "com.intuit.test.mobileTest.AcceptanceTest";
	protected static final String FUNCTIONAL_TEST = ACCEPTANCE_TEST + " com.intuit.test.mobileTest.FunctionalTest";
	protected static final String PROPERTY_TESTNAME = "testname";
	protected static final String PROPERTY_LOG = "log";
	public static final String SERVLETDIR = "/apache-tomcat-7.0.16/webapps/MoetServlet/";
	public static final String OUTPUTDIR = " -Doutputdir=" + SERVLETDIR;
	
	private static String[] emulatorsList = new String[] { "emulator-5554", "emulator-5556", "emulator-5558", "emulator-5560", "emulator-5562" };
	private static String[] devicesList = new String[] { "HTC0102033", "1010330330", "LG0838222", "XM243255s", "MT2432554" };
	
	private static enum resolutionsEnum
	{	
		r320x480,
		r480x800,
		r480x854,
		r800x1280,
		r240x320
	};
	
    /**
     * @see HttpServlet#HttpServlet()
     */
    public MoetServlet() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException 
    {
    	// TODO Auto-generated method stub
    	String testname = request.getParameter(MoetServlet.PROPERTY_TESTNAME);
    	String devicePropValue = request.getParameter(Settings.PROPERTY_DEVICE);
    	String device = " -Ddevice=" + devicePropValue;
    	String res = request.getParameter(Settings.PROPERTY_RESOLUTION);
    	String resolution = " -Dresolution=" + res.substring(1);
    	String os = " -Dos=" + request.getParameter(Settings.PROPERTY_OPERATINGSYSTEM);
    	String log = " -Dlog=" + request.getParameter(Settings.PROPERTY_LOG);
    	
    	String deviceIdPropValue = request.getParameter(Settings.PROPERTY_DEVICEID);	
    	String deviceId = null;
    	if (deviceIdPropValue != null)
    	{
    		if (deviceIdPropValue.contains("emulator"))
    			deviceIdPropValue = emulatorsList[resolutionsEnum.valueOf(res).ordinal()];
    		else 
    			deviceIdPropValue = devicesList[resolutionsEnum.valueOf(res).ordinal()];
    	}
    	deviceId = " -Ddeviceid=" + deviceIdPropValue;
    	
    	String classname = ACCEPTANCE_TEST;
    	if (testname.contains("functional"))
    	{
    		classname = FUNCTIONAL_TEST;
    	}

    	StringBuffer testCommand = new StringBuffer("java ");
    	testCommand.append(OUTPUTDIR);
    	testCommand.append(device).append(resolution).append(os).append(deviceId).append(log).append(" ");
    	testCommand.append(" org.junit.runner.JUnitCore ");
    	testCommand.append(classname);
   
    	response.setContentType("text/html");
    	PrintWriter out = response.getWriter();
    	out.println("<html>");
    	out.println("<head><title>Test Results</title></head>");
    	out.println("<body>");
    	out.println(testCommand.toString());

    	InputStreamReader errReader = null;
    	BufferedReader bufErrReader = null;
    	InputStreamReader outReader = null;
    	BufferedReader bufOutReader = null;
		BufferedWriter writer = null;
    	Process p = null;
		String resultsFile = ".." + File.separatorChar + "webapps" + File.separatorChar + 
			"MoetServlet" + File.separatorChar + "results-" + devicePropValue + "-" + deviceIdPropValue + ".log";

    	try
    	{
    		p = Runtime.getRuntime().exec(testCommand.toString());
    		// Wait for test to get started
    		Thread.sleep(3000);
    		
    		errReader = new InputStreamReader(p.getErrorStream());
    		bufErrReader = new BufferedReader(errReader);
    		writer = new BufferedWriter(new FileWriter(resultsFile));
    		String line;
    		while((line = bufErrReader.readLine()) != null)
			{
				writer.write(line + "<br>");
				writer.newLine();
			}
    		outReader = new InputStreamReader(p.getInputStream());    		
    		bufOutReader = new BufferedReader(outReader);
    		while((line = bufOutReader.readLine()) != null)
			{
				writer.write(line + "<br>");
				writer.newLine();
			}
    		response.sendRedirect("/MoetServlet/results-" + devicePropValue + "-" + deviceIdPropValue + ".jsp");
    	}
    	catch(InterruptedException e)
    	{
    		writer.write(e.getMessage());
    		e.printStackTrace(out);
    	}
    	finally
		{
			try 
			{
				errReader.close();
				bufErrReader.close();
				outReader.close();
				bufOutReader.close();
				writer.close();
	    		p.destroy();
			}
			catch(Exception e) {};
		}
    	
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException 
	{
		// TODO Auto-generated method stub
	}

}

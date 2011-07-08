package com.intuit.moet;

import java.io.File;
import java.io.FileInputStream;
import java.util.Properties;


public class Settings 
{
	private static Properties deviceProperties = new Properties();

	public static final String MOET_PROPERTIES_FILE = "moet.properties";
	public static final String PROPERTY_FILENAME = "app";
	public static final String PROPERTY_DEVICE = "device";
	public static final String PROPERTY_DEVICEID = "deviceid";
	public static final String PROPERTY_RESOLUTION = "resolution";
	public static final String PROPERTY_OPERATINGSYSTEM = "os";
	public static final String PROPERTY_OUTPUTDIR = "outputdir";
	public static final String PROPERTY_LOG = "log";
	public static final int SLEEP_INTERVAL= 3000;
	public static final String IMAGETOOL_DIR = System.getenv("IMAGETOOL");
	
	public String device = null;
	public String deviceId;
	public String resolution = "320x480";
	public String os = "2.2";
	public int resX;
	public int resY;
	
	// app specific setting
	public String outputDir = null;
	public String actualDir = null;
	public String expectedDir = null;
	public String log = "off";	

	public Settings() {}
	
	// read in a properties file or assume it is device.properties
	public void init()
	{
		// first check if each individual property is specified
		device = System.getProperty(PROPERTY_DEVICE);
		try 
		{
			// if system property is missing, look for properties file
			if (device == null)
			{
				String devicePropertyFile = System.getProperty(PROPERTY_FILENAME);
				if (devicePropertyFile == null)
				{		
					// last resort - check if default file exists
					File propFile = new File(Settings.MOET_PROPERTIES_FILE);
					if (propFile.exists())
						devicePropertyFile = Settings.MOET_PROPERTIES_FILE;		
				}
				if (devicePropertyFile != null)
				{
					FileInputStream in = new FileInputStream(devicePropertyFile);
					deviceProperties.load(in);
					in.close();
					device = deviceProperties.getProperty(PROPERTY_DEVICE);
					deviceId = deviceProperties.getProperty(PROPERTY_DEVICEID);
					resolution = deviceProperties.getProperty(PROPERTY_RESOLUTION);
					os = deviceProperties.getProperty(PROPERTY_OPERATINGSYSTEM);
					outputDir = deviceProperties.getProperty(PROPERTY_OUTPUTDIR);
					log = deviceProperties.getProperty(PROPERTY_LOG);
				}
			}
			else
			{
				deviceId = System.getProperty(PROPERTY_DEVICEID);
				resolution = System.getProperty(PROPERTY_RESOLUTION);
				os = System.getProperty(PROPERTY_OPERATINGSYSTEM);
				outputDir = System.getProperty(PROPERTY_OUTPUTDIR);
				log = System.getProperty(PROPERTY_LOG);
			}

			if (resolution != null)
			{
				String[] res = resolution.split("x");
				if (res.length >= 2) 
				{
					resX = Integer.parseInt(res[0]);
					resY = Integer.parseInt(res[1]);
				}
			}

			StringBuffer testdir = new StringBuffer("");
			StringBuffer archives = new StringBuffer("");
			
			if (outputDir != null)
			{
				testdir.append(outputDir).append(File.separatorChar);
				archives.append(outputDir).append(File.separatorChar);
			}
			testdir.append("target");
			archives.append("resources");

			if (this.device != null)
			{
				testdir.append(File.separatorChar);
				archives.append(File.separator);

				testdir.append(this.device);
				archives.append(this.device);

				if (this.deviceId != null)
				{
					testdir.append('-');
					testdir.append(this.deviceId);
				}		
				if (this.resolution != null)
				{
					archives.append(File.separator);	
					archives.append(this.resolution);	
				}
				testdir.append(File.separatorChar);	
				archives.append(File.separator);
			}	

			this.actualDir = testdir.toString();
			this.expectedDir = archives.toString();

			// create test output directory if not exist
			File expectedDirFile = new File(this.expectedDir);
			expectedDirFile.mkdirs();
			expectedDirFile = null;

			// create archives directory if not exist
			File actualDirFile = new File(this.actualDir);
			actualDirFile.mkdirs();
			actualDirFile = null;
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
	
	public String toString()
	{
		return this.device + " " + this.deviceId + " " + this.resolution + " " + this.os + " " + this.outputDir;
	}
}

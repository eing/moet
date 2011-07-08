package com.intuit.moet;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.logging.FileHandler;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import com.android.monkeyrunner.MonkeyDevice.TouchPressType;
import com.android.monkeyrunner.MonkeyImage;
import com.android.monkeyrunner.MonkeyManager;
import com.android.monkeyrunner.adb.AdbBackend;
import com.android.monkeyrunner.adb.AdbMonkeyDevice;

public class Android implements IDevice
{

	private static final String KEYCODE_MENU = "KEYCODE_MENU";
	private static final String KEYCODE_HOME = "KEYCODE_HOME";
	private static final String KEYCODE_DEL = "KEYCODE_DEL";
	private static final String KEYCODE_BACK = "KEYCODE_BACK";
	private static final String KEYCODE_ENTER = "KEYCODE_ENTER";
	private static final String KEYCODE_SPACE = "KEYCODE_SPACE";
	private static final String KEYCODE_UP = "KEYCODE_DPAD_UP";
	private static final String KEYCODE_DOWN = "KEYCODE_DPAD_DOWN";
	private static final String KEYCODE_LEFT = "KEYCODE_DPAD_LEFT";
	private static final String KEYCODE_RIGHT = "KEYCODE_DPAD_RIGHT";

	public static AdbBackend adbConn = null;
	public static AdbMonkeyDevice device = null;
	public MonkeyImage image;
	public Settings settings;
	public static String adbLogfile;
	
	private static final Logger LOG = Logger.getLogger(Settings.class.getName());

	public Android(Settings settings)
	{
		this.settings = settings;
		Logger MonkeyLog = Logger.getLogger(MonkeyManager.class.getName());

		if (!this.settings.log.contains("on"))
			MonkeyLog.setLevel(Level.SEVERE);

		Logger adbLog = Logger.getLogger(AdbMonkeyDevice.class.getName());
		adbLogfile = this.settings.actualDir + "adb.log";
		BufferedReader bufferedFile = null;

		try
		{
			Handler handler = new FileHandler(adbLogfile);
			adbLog.setUseParentHandlers(false);
			MonkeyLog.setUseParentHandlers(false);
			handler.setFormatter(new SimpleFormatter());
		    adbLog.addHandler(handler);
			MonkeyLog.addHandler(handler);
			
			if (adbConn == null)
				adbConn = new AdbBackend();
			
			if (device == null) 
			{
				if (settings.deviceId != null)
				{
					LOG.info("Establishing connection to "+ settings.deviceId);
					device = (AdbMonkeyDevice) adbConn.waitForConnection(10000, settings.deviceId);
				}
				else
				{
					device = (AdbMonkeyDevice) adbConn.waitForConnection();		
				}

				boolean reconnect = false;

				// Adding sleep for File IO to capture the logs from adb
				Thread.sleep(Settings.SLEEP_INTERVAL * 2);
				bufferedFile = new BufferedReader(new FileReader(adbLogfile));
				String line;
				while ( !reconnect && (line = bufferedFile.readLine()) != null )
				{
					if (line.indexOf("ShellCommandUnresponsiveException") > 0)
						reconnect = true;
				}
				if (reconnect)
				{
					LOG.info("!! -- ATTEMPTING TO RECONNECT TO ADB --  !! ");
					if (settings.deviceId != null)
						device = (AdbMonkeyDevice) adbConn.waitForConnection(10000, settings.deviceId);
					else
						device = (AdbMonkeyDevice) adbConn.waitForConnection();				
				}
			}
		}
		catch (Exception e) 
		{
			e.printStackTrace();
		}
		finally
		{
			try 
			{ 
				bufferedFile.close(); 
				adbLog = null;
			} 
			catch(Exception e) { /* ignore */ }  
		}
	}
	
	public void cleanup() throws Exception
	{
		adbConn.shutdown();
	}

	public void menu()
	{
		try 
		{
			device.press(KEYCODE_MENU, TouchPressType.DOWN_AND_UP);
			Thread.sleep(2000);
		}
		catch (InterruptedException e)
		{
			e.printStackTrace();
		}
	}

	public void home()
	{
		device.press(KEYCODE_HOME, TouchPressType.DOWN_AND_UP);
	}

	public void back()
	{
		device.press(KEYCODE_BACK, TouchPressType.DOWN_AND_UP);
	}


	public void backspaces(int num)
	{
		while (num > 0)
		{
			device.press(KEYCODE_DEL, TouchPressType.DOWN_AND_UP);
			num--;
		}
	}

	public void enter() 
	{
		try 
		{
			device.press(KEYCODE_ENTER, TouchPressType.DOWN_AND_UP);
			Thread.sleep(500);
		}
		catch (InterruptedException e)
		{
			e.printStackTrace();
		}
	}

	public void enter(String inputStr)
	{
		if (inputStr == null)
			this.enter();
		else
		{
			String[] strList = inputStr.split(" ");
			int strLen = strList.length;
			device.type(strList[0]);
			for (int index = 1;  index < strLen; index++)
			{
				device.press(KEYCODE_SPACE, TouchPressType.DOWN_AND_UP);
				device.type(strList[index]);
			}
		}

	}

	public void scroll(String direction)
	{
		scroll(direction, 1);
	}

	public void scroll(String direction, int num)
	{
		try 
		{
			String key;
			if (direction.contains("up"))
				key = KEYCODE_UP;
			else if (direction.contains("down"))
				key = KEYCODE_DOWN;
			else if (direction.contains("left"))
				key = KEYCODE_LEFT;
			else if (direction.contains("right"))
				key = KEYCODE_RIGHT;
			else	   
			{
				LOG.severe("Invalid direction for scroll");
				return;
			}
			while (num > 0)
			{
				device.press(key, TouchPressType.DOWN_AND_UP);
				num--;
			}
			Thread.sleep(200);
		}
		catch(InterruptedException e)
		{
			e.printStackTrace();
		}
	}

	private int absCoordinates(String percentCoord, String type)
	{
		int coordValue = 0;
		int resolution = 0;

		if (percentCoord.endsWith("%"))
		{
			coordValue = Integer.parseInt(percentCoord.substring(0, percentCoord.length() - 1));
			if (this.settings.resolution != null)
			{
				if (type.contains("x"))					
					resolution = this.settings.resX;
				else
					resolution = this.settings.resY;
			}
			else
			{
				if (type.contains("x"))
					resolution = 480;
				else
					resolution = 800;
			}		
			return (coordValue * resolution) / 100;

		}
		else
			return coordValue;
	}

	public void touch(int x, int y)
	{
		LOG.info("Tapping on screen at (" + x + ", " + y + ")");
		device.touch(x, y, TouchPressType.DOWN_AND_UP);
	}

	public void touch(String x, String y)
	{
		int xInt = absCoordinates(x, "x");
		int yInt = absCoordinates(y, "y");
		this.touch(xInt, yInt);
	}

	public void drag(int fromX, int fromY, int toX, int toY)
	{
		device.drag(fromX, fromY, toX, toY, 1, 5);
	}

	public void drag(String fromX, String fromY, String toX, String toY)
	{
		try 
		{
			int fromXInt = absCoordinates(fromX, "x");
			int fromYInt = absCoordinates(fromY, "y");
			int toXInt = absCoordinates(toX, "x");
			int toYInt = absCoordinates(toY, "y");
			LOG.info("Dragging from (" + fromXInt + ", " + fromYInt + ") to (" + toXInt + ", " + toYInt + ")");
			device.drag(fromXInt, fromYInt, toXInt, toYInt, 1, 5);
			Thread.sleep(1000);
		}
		catch (InterruptedException e)
		{
			e.printStackTrace();
		}
	}

	public void launch(String activity)
	{
		LOG.info("Launching activity - " + activity);
		device.shell(" am start -n " + activity);
	}

	public void screenshot(String filename)
	{
		image = device.takeSnapshot();
		filename = this.settings.actualDir + filename + ".png";
		//LOG.info("Saving file to " + filename);
		image.writeToFile(filename, "png");
	}
}
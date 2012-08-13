package app.addressbook.test;

import app.addressbook.test.impl.AndroidImpl;
import app.addressbook.test.impl.IAddressBook;
import app.addressbook.test.impl.iPhoneImpl;

import com.intuit.moet.Android;
import com.intuit.moet.IDevice;
import com.intuit.moet.Settings;
import com.intuit.moet.iPhone;

/**
 * Utilizes creator pattern to create needed device class at runtime.
 * @author eong
 *
 */
public class MobileTest 
{
	/** 
	 * Returns device for testing.
	 * @param deviceName device name : android or iphone
	 * @param settings contains resolution, output directories etc.
	 * @return device
	 */
	public static IDevice getDevice(String deviceName, Settings settings) throws Exception
	{
		if (deviceName.contains("android"))
			return new Android(settings);
		else if (deviceName.contains("iphone"))
			return new iPhone(settings);
		else
			return null;
	}

	/** 
	 * Returns mobile app for testing.
	 * @param deviceName device name : android or iphone
	 * @param settings contains resolution, output directories etc.
	 * @return android or iphone mobile app
	 */
	public static IAddressBook getMobileApp(IDevice device, Settings settings)
	{
		if (device.getClass().getName().contains("Android"))
				return new AndroidImpl(device, settings);
		else if (device.getClass().getName().contains("iPhone"))
			return new iPhoneImpl(device,settings);
		else
			return null;
	}

}

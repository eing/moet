package com.intuit.moet;

public class MobileTest 
{

	public static IDevice getDevice(String deviceName, Settings settings)
	{
		if (deviceName.contains("android"))
			return new Android(settings);
		else if (deviceName.contains("iphone"))
			return new iPhone(settings);
		else
			return null;
	}

	public static IMobileApp getMobileApp(IDevice device, Settings settings)
	{
		if (device.getClass().getName().contains("Android"))
				return new AndroidImpl(device, settings);
		else if (device.getClass().getName().contains("iPhone"))
			return new iPhoneImpl(device,settings);
		else
			return null;
	}

}

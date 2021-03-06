package app.addressbook.test;

import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Rule;
import org.junit.rules.TestName;

import app.addressbook.test.impl.IAddressBook;

import com.intuit.moet.IDevice;
import com.intuit.moet.ImageKit;
import com.intuit.moet.ImageObject;
import com.intuit.moet.Settings;
import com.intuit.moet.StatusEnum;
import com.intuit.moet.iPhone;

/**
 * Base class for all tests to extend.
 * Reads in application properties as well as obtain device and app for testing.
 * @author eong
 *
 */
public class BaseTest 
{
	private static final String APP_ICON_PNG = "appIcon.png";

	@Rule public TestName name = new TestName();
	
	Properties userProperties = new Properties();
	
	public static IDevice device;
	public IAddressBook addressbook;
	public Settings settings;
	public ImageKit imagekit;
	public ImageObject image;

	protected static final Logger LOG = Logger.getLogger(Settings.class.getName());
	
	// read in a properties file
	public BaseTest() throws Exception
	{
		this.init();
	}
	
	
	public void init() throws Exception
	{
		image = new ImageObject();
		this.settings = new Settings();
		this.settings.init();
		
		if (this.settings.log.contains("on"))
		{
			Logger.getLogger(Settings.class.getName()).setLevel(Level.INFO);
		}
		else
		{
			Logger.getLogger(Settings.class.getName()).setLevel(Level.SEVERE);
		}

        if (settings.device == null) 
        {
        	Assert.fail("Device is null. Pls specify device property");
        }
        
        String deviceName = settings.device;

        device = MobileTest.getDevice(deviceName, this.settings);
        Assert.assertNotNull(StatusEnum.DEVICE_INVALID.toString(), device);
        addressbook = MobileTest.getMobileApp(device, settings);
        Assert.assertNotNull(StatusEnum.APP_CREATION_FAILED.toString(), addressbook);
	}
	
	
	@Before
	public void setup() throws Exception
	{
		LOG.info("[Activity] *** Starting test : " + name.getMethodName() + " ***");
		if (device instanceof iPhone)
		{
			device.launch("Contacts~iphone.app");
		}
		else
		{
			device.launch("com.android.contacts/.DialtactsContactsEntryActivity");
			Thread.sleep(5000);
		}
		device.clearLog();
	}

	
}

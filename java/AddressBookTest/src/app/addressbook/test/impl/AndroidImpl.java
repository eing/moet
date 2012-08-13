package app.addressbook.test.impl;

import java.io.File;
import java.util.logging.Logger;

import app.addressbook.test.Contact;

import com.intuit.moet.Android;
import com.intuit.moet.IDevice;
import com.intuit.moet.ImageKit;
import com.intuit.moet.Settings;

/**
 * Android implementation of IMobileApp.
 * @author eong
 *
 */
public class AndroidImpl implements IAddressBook
{
	private Android device;
	private Settings settings;
	private static final int SLEEP_INTERVAL = 5000;
		private static final Logger LOG = Logger.getLogger(Settings.class.getName());
	

	/**
	 * Constructor for Android Implementation.
	 * @param device Android device
	 * @param settings System and Application configuration settings
	 */
	public AndroidImpl(IDevice device, Settings settings)
	{
		try
		{
			this.device = (Android) device;
			this.settings = settings;
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
		
	private void createScreenshot(String filename)
	{
		File expectedDirImage = new File(settings.expectedDir + filename + ".png");
		File actualDirImage = new File(settings.actualDir + filename + ".png");
		if (!expectedDirImage.exists())
		{
			if (!actualDirImage.exists())
				device.screenshot(filename);
		}
	}
	
	private void screen(String name) throws Exception
	{
		name = name.toLowerCase();
		device.scroll("up", 2);
		Thread.sleep(1000);
		if (name.contains("phone"))
		{
			device.scroll("left", 3);
		}
		else if (name.contains("contacts"))
		{
			device.scroll("right", 4);
			device.scroll("left", 1);
		}
		else if (name.contains("fav"))
		{
			device.scroll("right", 4);
		}
		else
		{
			device.scroll("left", 4);
			device.scroll("right", 1);			
		}
	}
	
	
	/**
	 * Add contact to address book app.
	 * @param contact Contact info object
	 * @return true if success
	 * @throws Exception exception
	 */
	public boolean addContact(Contact contact) throws Exception
	{
		
		this.screen("contacts");
		device.menu();

		Thread.sleep(1000);
		device.scroll("right");
		device.enter();
		Thread.sleep(2000);
		
		device.scroll("up", 7);
		device.scroll("down");
		device.enter(contact.getFirstname());
		device.scroll("down");
		device.enter(contact.getLastname());
		device.scroll("down", 2);
		
		device.enter(contact.getPhone());
		device.scroll("down", 2);
		
		device.enter(contact.getEmail());
		device.scroll("down", 7);
		
		device.enter();
		Thread.sleep(5000);
		return true;
	}
	
	/**
	 * Find contact to address book app.
	 * @param contact Contact info object
	 * @return true if success
	 * @throws Exception exception
	 */
	public boolean findContact(Contact contact) throws Exception
	{

		this.screen("contacts");
		device.menu();
		Thread.sleep(1000);
		device.scroll("up", 2);
		device.enter();
		device.enter(contact.getFirstname() + " " + contact.getLastname());
		device.enter();
		Thread.sleep(2000);
		
		device.scroll("down", 2);
		device.enter();
		Thread.sleep(2000);
		device.enter();
		Thread.sleep(2000);
		
		return true;
	}
	
	/**
	 * Delete contact to address book app.
	 * @param contact Contact info object
	 * @return true if success
	 * @throws Exception exception
	 */
	public boolean deleteContact(Contact contact) throws Exception
	{
		device.menu();
		Thread.sleep(1000);
		
		device.scroll("down", 2);
		Thread.sleep(1000);
		device.scroll("right", 1);
		Thread.sleep(1000);
		device.enter();
		Thread.sleep(1000);
		
		device.enter();
		Thread.sleep(2000);
		device.back();
		Thread.sleep(1000);
		device.back();
		Thread.sleep(1000);
		return true;
	}
	
}

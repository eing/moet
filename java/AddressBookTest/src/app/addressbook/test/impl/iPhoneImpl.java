package app.addressbook.test.impl;

import java.util.logging.Logger;

import app.addressbook.test.Contact;
import app.addressbook.test.Contact.EmailLabel;
import app.addressbook.test.Contact.PhoneLabel;

import com.intuit.moet.IDevice;
import com.intuit.moet.ImageKit;
import com.intuit.moet.ImageObject;
import com.intuit.moet.Settings;
import com.intuit.moet.iPhone;

/**
 * iPhone implementation of IMobileApp.
 * @author eong
 *
 */
public class iPhoneImpl implements IAddressBook 
{
	private static final String BUTTON_ALL_CONTACTS = "ButtonAllContacts.png";
	private static final String BUTTON_CANCEL = "ButtonCancel.png";
	private static final String BUTTON_DELETE = "ButtonDelete.png";
	private static final String BUTTON_EDIT = "ButtonEdit.png";
	private static final String BUTTON_SEARCH = "ButtonSearch.png";
	
	private static final String ICON_ADD_CONTACT = "IconAddContact.png";
	private static final String ICON_CANCEL = "IconCancel.png";
	private static final String ICON_SEARCH = "IconSearch.png";
	private static final String IMAGE_LISTITEM = "ImageListItem.png";
	
	private static final String KEY_SEARCH = "KeySearch.png";
	
	private iPhone device;
	private Settings settings;
	
	private static final int SLEEP_INTERVAL = 2000;
	private static final Logger LOG = Logger.getLogger(Settings.class.getName());
	
	public iPhoneImpl(IDevice device, Settings settings) 
	{
		this.device = (iPhone) device;
		this.settings = settings;
	};

	private void resetToHomeScreen() throws Exception
	{
		if (ImageKit.findImage(device, ICON_CANCEL))
		{
			device.tapImage(ICON_CANCEL);
		}
		if (ImageKit.findImage(device, BUTTON_SEARCH))
		{
			device.tapImage(BUTTON_SEARCH);
		}
		
		if (ImageKit.findImage(device, BUTTON_CANCEL))
		{
			device.tapImage(BUTTON_CANCEL);
		}
		else if (ImageKit.findImage(device, BUTTON_ALL_CONTACTS))
		{
			device.tapImage(BUTTON_ALL_CONTACTS);
		}

		Thread.sleep(SLEEP_INTERVAL);
	}
	
	/**
	 * Add contact to address book app.
	 * @param contact Contact info object
	 * @return true if success
	 * @throws Exception exception
	 */
	public boolean addContact(Contact contact) throws Exception
	{
		resetToHomeScreen();
		
		device.tapImage(ICON_ADD_CONTACT);
		Thread.sleep(SLEEP_INTERVAL);
		System.out.println(device.getText());
		
		if (contact.getFirstname() != null)
		{
			device.tap("First");
			device.enter(contact.getFirstname());
		}
		if (contact.getLastname() != null)
		{
			device.tap("Last");
			device.enter(contact.getLastname());
		}
		if (contact.getPhone() != null)
		{
			device.tap("Phone");
			device.enter(contact.getPhone());
			if (contact.getPhoneLabel() != PhoneLabel.mobile)
			{
				device.tap("mobile");
				System.out.println(device.getText());
				device.tap(contact.getPhoneLabel().name());
			}
		}
		if (contact.getEmail() != null)
		{
			device.tap("Email");
			device.enter(contact.getEmail());
			if (contact.getEmailLabel() != EmailLabel.home)
			{
				device.tap("home");
				System.out.println(device.getText());
				device.tap(contact.getEmailLabel().name());
			}
		}
		
		// Click Done
		device.tapImage("ButtonDone.png");
		Thread.sleep(SLEEP_INTERVAL);
		
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
		resetToHomeScreen();
		device.tapImage(ICON_SEARCH);
		device.enter(contact.getFirstname() + " " + contact.getLastname());
		device.tap(KEY_SEARCH);
		device.tap(IMAGE_LISTITEM);
		Thread.sleep(SLEEP_INTERVAL);
		return true;
	}
	
	/**
	 * Delete contact to address book app.
	 * Pre-condition : User has called findContact prior to deleteContact.
	 * @param contact Contact info object
	 * @return true if success
	 * @throws Exception exception
	 */
	public boolean deleteContact(Contact contact) throws Exception
	{
		device.tapImage(BUTTON_EDIT);
		device.scroll("down");
		device.tap(BUTTON_DELETE);
		Thread.sleep(SLEEP_INTERVAL);
		device.tap(BUTTON_DELETE);
		Thread.sleep(SLEEP_INTERVAL);
		return true;
	}
}

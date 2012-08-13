package app.addressbook.test;

import junit.framework.Assert;

import org.junit.Test;

public class AddContactTest extends BaseTest
{
	public AddContactTest() throws Exception
	{
		super();
	}

	@Test
	public void  addFirstnameOnlyTest() throws Exception
	{
		Contact contact = new Contact("Hello", "World");
		Assert.assertTrue(addressbook.addContact(contact));
		Assert.assertTrue(addressbook.findContact(contact));
		Assert.assertTrue(addressbook.deleteContact(contact));
	}
}

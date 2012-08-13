package app.addressbook.test;

/**
 * Contact in address book.
 * @author eong
 *
 */
public class Contact 
{
	public static enum PhoneLabel
	{ mobile, iPhone, home, work, main, 
	home_fax, work_fax, other_fax, pager, other };
	
	public static enum EmailLabel { home, work, other };

	private String firstname = null;
	private String lastname = null;
	private String phone = null;
	private String email = null;
	private EmailLabel emailLabel;
	private PhoneLabel phoneLabel;
	
	public Contact(String firstname, String lastname)
	{
		this.firstname = firstname;
		this.lastname = lastname;
	}
	
	public Contact() {}

	/**
	 * @return the firstname
	 */
	public String getFirstname() {
		return firstname;
	}

	/**
	 * @param firstname the firstname to set
	 */
	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}

	/**
	 * @return the lastname
	 */
	public String getLastname() {
		return lastname;
	}

	/**
	 * @param lastname the lastname to set
	 */
	public void setLastname(String lastname) {
		this.lastname = lastname;
	}

	/**
	 * @return the phone
	 */
	public String getPhone() {
		return phone;
	}

	/**
	 * @param phone the phone to set
	 */
	public void setPhone(String phone) {
		this.phone = phone;
	}

	/**
	 * @return the email1
	 */
	public String getEmail() {
		return email;
	}

	/**
	 * @param email1 the email1 to set
	 */
	public void setEmail(String email) {
		this.email = email;
	}

	/**
	 * @return the emailLabel
	 */
	public EmailLabel getEmailLabel() {
		return emailLabel;
	}

	/**
	 * @param emailLabel the emailLabel to set
	 */
	public void setEmailLabel(EmailLabel emailLabel) {
		this.emailLabel = emailLabel;
	}

	/**
	 * @return the phoneLabel
	 */
	public PhoneLabel getPhoneLabel() {
		return phoneLabel;
	}

	/**
	 * @param phoneLabel the phoneLabel to set
	 */
	public void setPhoneLabel(PhoneLabel phoneLabel) {
		this.phoneLabel = phoneLabel;
	}

}

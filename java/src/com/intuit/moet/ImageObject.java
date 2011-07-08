package com.intuit.moet;

public class ImageObject 
{
	public static final String defaultCrop = "100%x100%+0%+6%";
	public String filename;
	public String fileToCompare = null;
	public String crop = defaultCrop;
	public int tolerance = ImageKit.tolerance;
	public int tries = 1;
	
	public ImageObject(String image, String crop, int tolerance, int tries)
	{
		this.filename = image;
		this.crop = crop;
		this.tolerance = tolerance;
		this.tries = tries;
	}
	
	public ImageObject(String image, String crop, int tolerance)
	{
		this.filename = image;
		this.crop = crop;
		this.tolerance = tolerance;
	}
	
	public ImageObject(String image, String crop)
	{
		this.filename = image;
		this.crop = crop;
	}
	
	public ImageObject(String image)
	{
		this.filename = image;
	}
	
	public ImageObject() {}
	
	public void setImageObject(String filename)
	{
		this.filename = filename;
		this.crop = defaultCrop;
		this.tries = 1;
		this.tolerance = ImageKit.tolerance;
	}
	
	public void setImageObject(String filename, String crop)
	{
		this.filename = filename;
		this.crop = crop;
		this.tries = 1;
		this.tolerance = ImageKit.tolerance;
	}
	
	public void setImageObject(String filename, String crop, int tries)
	{
		this.filename = filename;
		this.crop = crop;
		this.tries = tries;
		this.tolerance = ImageKit.tolerance;
	}
	
	public void setImageObject(String filename, String crop, int tolerance, int tries)
	{
		this.filename = filename;
		this.crop = crop;
		this.tries = tries;
		this.tolerance = tolerance;
	}
}

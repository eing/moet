package com.intuit.moet;

public enum StatusEnum 
{
	SUCCESS (0, "Passed"),
	
	APP_CREATION_FAILED (100, "App instantiation failed"),
	APP_PRECONDITION_FAILED (101, "Precondition failed"),
	APP_POSTCONDITION_FAILED (102, "Post condition failed"),
	APP_PROCESSING_FAILED (103, "Processing failed"),
	MENU_OPTION_NOT_SUPPORTED(150, "User menu option is not supported"),
	
	DATA_SETTINGS_NULL(200, "Settings information is null"),
	
	IMAGE_STATUS_FAIL (500, "Image comparision failed"),	
	IMAGE_ABOVE_TOLERANCE (501, "Image difference is above tolerance level"),
	IMAGE_CROP_FORMAT (501, "Crop format specified is invalid"),
	IMAGE_IMPROPER_IMAGE_HEADER (502, "Improper image header"),
	IMAGE_SAME_FILES (503, "Comparing images of same filename and location"),
	IMAGE_MOVEFILE_ERROR (504, "Captured image move did not succeed"),
	IMAGE_MISSING_FILE (505, "Comparing with a missing archive file"),
	
	DEVICE_INVALID (600, "Invalid device");

	
	private final int code;
	private final String description;
	
	StatusEnum(int code, String description)
	{
		this.code = code;
		this.description = description;
	}
	
	public int getCode()
	{
		return code;
	}
	
	public String getDescription()
	{
		return description;
	}
	
	@Override
	public String toString()
	{
		return code + ": " + description;
	}
	
}

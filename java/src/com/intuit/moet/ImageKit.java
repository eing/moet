package com.intuit.moet;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.logging.Logger;


public class ImageKit 
{
	private static final Logger LOG = Logger.getLogger(Settings.class.getName());
	public static final int tolerance = 500;
	
	public static int calculateLandscape(int portraitCoord, int portraitRes, int landscapeRes)
	{
		return (landscapeRes/portraitRes * portraitCoord);
	}
	
	/**
	 *  Convert settings in % to actual resolution crop settings, e.g.
        parseCropSettings('100%x90%+10%+0%', '320', '240')
        parseCropSettings('100%x90%+10%+20%', '320', '240')
        parseCropSettings('100%x90%', '320', '240')
        parseCropSettings('+10%+0%', '320', '240')
	 */
	public static String crop(String cropSetting, int resX, int resY)
	{
		if (cropSetting == null)
			return null;
		String[] percentSplit = cropSetting.split("%");
		int x = 0;
		int y = 0;
		int sizeX = 0;
		int sizeY = 0;
		
		if (percentSplit.length == 2)
		{
			//'100%x90%' or '+10%+0%'
			String[] xSplit = cropSetting.split("x");
			if (xSplit.length == 2)
			{
				// 100%x90%
				x = Integer.parseInt(percentSplit[0]);
				y = Integer.parseInt(percentSplit[1].substring(1, xSplit[1].length()));
				x = (x * resX) / 100;
				y = (y * resY) / 100;
				sizeX = 0;
				sizeY = 0;
			}
			else 
			{
				// +10%+0%
				sizeX = Integer.parseInt(percentSplit[0].substring(1, percentSplit[0].length()));
				sizeY = Integer.parseInt(percentSplit[1].substring(1, percentSplit[1].length()));	
				sizeX = (sizeX * resX) / 100;
				sizeY = (sizeY * resY) / 100;
				x = 0;
				y = 0;
			}			
		}
		else if (percentSplit.length == 4)
		{
			// '100%x90%+10%+0%'
			x = Integer.parseInt(percentSplit[0]);
			y = Integer.parseInt(percentSplit[1].substring(1, percentSplit[1].length()));
			x = (x * resX) / 100;
			y = (y * resY) / 100;
			
			sizeX = Integer.parseInt(percentSplit[2].substring(1, percentSplit[2].length()));
			sizeY = Integer.parseInt(percentSplit[3].substring(1, percentSplit[3].length()));	
			sizeX = (sizeX * resX) / 100;
			sizeY = (sizeY * resY) / 100;
		}
		else
			return null;
		return "" + x + "x" + y + "+" + sizeX + "+" + sizeY;	
	}
	
	/**
	 * Has current screen changed from the image specified in image.filename
	 * @param image
	 * @param device
	 * @param settings
	 * @return
	 * @throws Exception
	 */
	public static StatusEnum hasScreenChanged(
			ImageObject image, 
			IDevice device, 
			Settings settings) throws Exception
	{
		return checkScreenWithStatus(image, device, settings, StatusEnum.IMAGE_ABOVE_TOLERANCE);
	}
	
	public static StatusEnum checkScreen(
			ImageObject image, 
			IDevice device, 
			Settings settings) throws Exception
	{
		return checkScreenWithStatus(image, device, settings, StatusEnum.SUCCESS);
	}
	
	/**
	 * Is current screen similar to image.filename
	 * Image files can be 
	 * 1. expectedDir/image.filename and currentImage
	 * 2. actualDir/image.filename and currentImage
	 * 3. image.filename does not exist, take a snapshot and return.
	 * @param image
	 * @param device
	 * @param settings
	 * @return
	 * @throws Exception
	 */
	public static StatusEnum checkScreenWithStatus(ImageObject image, IDevice device, 
			Settings settings, StatusEnum expectedStatus) throws Exception
	{
		
		StatusEnum results = StatusEnum.DATA_SETTINGS_NULL;
		int tries = image.tries;
		image.fileToCompare = image.filename + "_1";
		
		while ( (tries >= 1) && (results != expectedStatus))
		{
			device.screenshot(image.fileToCompare);
			results = compare(image, settings);
			if (results == StatusEnum.IMAGE_IMPROPER_IMAGE_HEADER)
				results = StatusEnum.IMAGE_STATUS_FAIL;
			tries = tries - 1;
			LOG.info("Results from Image compare " + results);
			Thread.sleep(Settings.SLEEP_INTERVAL);
		} 
	
		if (results == expectedStatus)
			return StatusEnum.SUCCESS;
		return StatusEnum.IMAGE_STATUS_FAIL;
	}
	
	/**
	 * Compare 2 image files - 
	 * Image files can be 
	 * 1. actualDir/image.filename and actualDir/image.filenameToCompare
	 * 2. expectedDir/image.png and actualDir/image.png
	 * @param image
	 * @param settings
	 * @return
	 */
	public static StatusEnum compare(ImageObject image, Settings settings)
	{
		if (settings == null)
			return StatusEnum.DATA_SETTINGS_NULL;
		
		// Expected image is the 'Golden' image to compare with
		String expectedFilename = image.filename;
		String expectedImage = settings.expectedDir + expectedFilename + ".png";
		String expectedCroppedImage = settings.actualDir + expectedFilename + "CropE.png";
		
		// Actual image is the current image to compare with the 'Golden' image
		String actualFilename = image.fileToCompare;
		String actualImage = settings.actualDir + actualFilename + ".png";
		String actualCroppedImage = settings.actualDir + actualFilename + "CropA.png";
		
		String diffImage = settings.actualDir + actualFilename + "Diff.png";

		// Verify the expected image to compare exists		
		File expectedDirImage = new File(expectedImage);
		if (!expectedDirImage.exists())
		{
			expectedImage = settings.actualDir + expectedFilename + ".png";
			File actualDirImage = new File(expectedImage);
			if (!actualDirImage.exists())
			{
				return StatusEnum.IMAGE_MISSING_FILE;
			}		
		}
		
		// Verify the actual image to compare exists
		File actualImageFile = new File(actualImage);
		if (!actualImageFile.exists())
			return StatusEnum.IMAGE_MISSING_FILE;

		String cropSetting = image.crop;
		int tolerance = image.tolerance; 

		StatusEnum results = StatusEnum.SUCCESS;
		int diff = -1;
		InputStreamReader inReader = null;
		BufferedReader bufReader = null;
		String line = null;

		try 
		{
			String imageToolDir = Settings.IMAGETOOL_DIR;

			// crop both images if needed
			if (cropSetting != null)
			{
				cropSetting = ImageKit.crop(cropSetting, settings.resX, settings.resY);
				if (cropSetting == null)
				{
					LOG.severe("Crop string error : " + cropSetting);
					return StatusEnum.IMAGE_CROP_FORMAT;
				}
				LOG.info("Crop setting is " + cropSetting);
				String[] cropActualImageCommand = {imageToolDir + "convert", "-crop", cropSetting, actualImage, actualCroppedImage};
				String[] cropExpectedImageCommand = {imageToolDir + "convert", "-crop", cropSetting, expectedImage, expectedCroppedImage};
				Runtime.getRuntime().exec(cropActualImageCommand);
				Runtime.getRuntime().exec(cropExpectedImageCommand);
				Thread.sleep(2000);
			}

			String[] compareImageCommand = { imageToolDir + "compare", "-verbose", "-fuzz", "5%", "-metric", "AE", actualCroppedImage,
					expectedCroppedImage, diffImage};

			Process p = Runtime.getRuntime().exec(compareImageCommand);
			Thread.sleep(3000);
			inReader = new InputStreamReader(p.getErrorStream());
			bufReader = new BufferedReader(inReader);
			while((line = bufReader.readLine()) != null)
			{
				if (line.contains("all"))
				{
					diff = Integer.parseInt(line.split(":")[1].trim());
					LOG.info("Image diff - " + diff);
				}
				else if (line.contains("improper image header"))
				{
					LOG.severe("Improper header detected");
					return StatusEnum.IMAGE_IMPROPER_IMAGE_HEADER;
				}
			}
			if (diff == -1) 
			{
				LOG.severe("Unable to obtain diff - likely missing archived image");
				return StatusEnum.IMAGE_MISSING_FILE;
			}
			// Check diff amount, if higher than tolerance, set results = false
			if (diff > tolerance)
				return StatusEnum.IMAGE_ABOVE_TOLERANCE;
			// always return true in capture mode
			return results;
		}
		catch (Exception e)
		{
			e.printStackTrace();
			return StatusEnum.IMAGE_STATUS_FAIL;
		}
		finally
		{
			try 
			{
				inReader.close();
				bufReader.close();	
			}
			catch(Exception e) {};
		}
	}
}

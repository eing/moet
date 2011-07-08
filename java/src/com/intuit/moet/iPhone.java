package com.intuit.moet;

public class iPhone implements IDevice
{
	public iPhone(Settings settings) {};
	public void cleanup() {}; 
	
	public void menu() {};	
	public void home() {};	
	public void back() {};
	public void backspaces(int num) {};
	public void enter() {};
	public void enter(String inputStr){};

	public void scroll(String direction){};
	public void scroll(String direction, int num){};
	
	public void touch(int x, int y){};
	public void touch(String x, String y){};
	
	public void drag(int fromX, int fromY, int toX, int toY){};
	public void drag(String fromX, String fromY, String toX, String toY){};	
	
	public void launch(String activity){};
	
	public void screenshot(String filename){};
}

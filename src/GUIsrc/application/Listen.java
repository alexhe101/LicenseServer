package application;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Field;

import com.sun.jna.Pointer;
import com.sun.jna.platform.win32.Kernel32;
import com.sun.jna.platform.win32.WinNT;

public class Listen extends Thread{
	//private String commandserver;
	private String commandclient;
	private String road;
	Data data;
	
	public void mystart(String road,Data data)
	{
		//commandserver="python server.py";
		//commandclient="python client.py";
		commandclient="client.exe";
		this.data=data;
		this.road=road;
	}
	
	public File getfile(String str)
	{
		File directory = new File(str);
		return directory;
	}
	
	public void run()
	{
		System.out.println("test");
		try {
			//Process server =Runtime.getRuntime().exec(commandserver,null,getfile(road));
			/*Process client =Runtime.getRuntime().exec(commandclient,null,getfile(road));
			InputStream is = client.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            //br.wait(100);
			String line=br.readLine();
			System.out.println("1test");*/
			Thread.sleep(50);
			
			File f=new File(road+"\\status.txt");
			Process client =Runtime.getRuntime().exec(commandclient,null,getfile(road));
			String line;
			
			while(true)
			{
				//System.out.println("test3");
				
				
				BufferedReader bu = new BufferedReader(new FileReader(f));
				line=bu.readLine();
				bu.close();
				//System.out.println(line);
				//f.delete();
				
				data.setflag(line);
				if(data.getstop()==1)
				{
					data.setstop(0);
					//server.destroy();
					//client.destroy();
					killProcessTree(client);
					//f.delete();
					//Thread.interrupted();
					break;
				}
				//line=br.readLine();
				
			}
			System.out.println("test2");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	private static void killProcessTree(Process process) {
		try {
			Field f = process.getClass().getDeclaredField("handle");
			f.setAccessible(true);
			long handl = f.getLong(process);
			Kernel32 kernel = Kernel32.INSTANCE;
			WinNT.HANDLE handle = new WinNT.HANDLE();
			handle.setPointer(Pointer.createConstant(handl));
			int ret = kernel.GetProcessId(handle);
			Long PID = Long.valueOf(ret);
			String cmd = getKillProcessTreeCmd(PID);
			Runtime rt = Runtime.getRuntime();
			Process killPrcess = rt.exec(cmd);
			killPrcess.waitFor();
			killPrcess.destroy();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
 
	private static String getKillProcessTreeCmd(Long Pid) {
		String result = "";
		if (Pid != null)
			result = "cmd.exe /c taskkill /PID " + Pid + " /F /T ";
		return result;
	}
}

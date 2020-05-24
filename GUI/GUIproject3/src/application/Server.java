package application;

import java.io.File;
import java.io.IOException;

public class Server extends Thread{
	private String commandserver="python server.py";
	private String road;
	private Process server;
	
	public void mystart(String road)
	{
		//commandserver="python server.py";
		this.road=road;
	}
	
	public File getfile(String str)
	{
		File directory = new File(str);
		return directory;
	}
	
	@SuppressWarnings("unused")
	public void run()
	{
		try {
			server =Runtime.getRuntime().exec(commandserver,null,getfile(road));
			/*InputStream is = server.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String content = br.readLine();
            while (true) {
                System.out.println(content+"server");
                content = br.readLine();
                Thread.sleep(100);
            }*/
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void mystop()
	{
		server.destroy();
	}
}

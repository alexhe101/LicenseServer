package application;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;

public class Control {
	@FXML private Button getkey;
	@FXML private Button start;
	@FXML private Label id;
	@FXML private Label password;
	@FXML private Label key;
	@FXML private TextField idtext;
	@FXML private TextField passwordtext;
	@FXML private TextField keytext;
	@FXML private Alert a;
	
	@FXML private Label text;
	@FXML private Button exit;
	@FXML private Button myreturn;
	
	@FXML private RadioButton ten;
	@FXML private RadioButton five;
	
	@SuppressWarnings("unused")
	private String namestr;
	@SuppressWarnings("unused")
	private String passwordstr;
	private String keystr;
	
	private String road;
	private int flag=0;
	private int flagwait=0;
	
	
	public void initialize() throws FileNotFoundException
	{
		
		Data data = new Data();
		
		text.setVisible(false);
		myreturn.setVisible(false);
		//exit.setVisible(false);
		
		road=System.getProperty("user.dir");
		//System.out.println(road);
		
		/*Process client;
		try {
			File d = new File(road);
			client = Runtime.getRuntime().exec("java -version",null,d);
			InputStream is = client.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String content = br.readLine();
            while (content != null) {
                System.out.println(content);
                content = br.readLine();
            }
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}*/
		
		Server server=new Server();
		server.mystart(road);
		server.start();
		
		start.setOnAction(e->{
			
			
			Listen listen=new Listen();
			namestr=idtext.getText();
			passwordstr=passwordtext.getText();
			keystr=keytext.getText();
			File f=new File(road+"\\key");
			try {
				@SuppressWarnings("resource")
				FileWriter writer = new FileWriter(f);
				writer.write(keystr);
				writer.flush();
				writer.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			
			if(f.exists())
			{
				listen.mystart(road,data);
				listen.start();
				start.setVisible(false);
				while(true)
				{
					if(flagwait==1)
					{
						try {
							Thread.sleep(2000);
							flagwait=0;
						} catch (InterruptedException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
					}
					if(data.getflag()!=null&&data.getflag().equals("GOOD"))
					{
						getkey.setVisible(false);
						start.setVisible(false);
						id.setVisible(false);
						password.setVisible(false);
						key.setVisible(false);
						idtext.setVisible(false);
						passwordtext.setVisible(false);
						keytext.setVisible(false);
						text.setVisible(true);
						//exit.setVisible(true);
						myreturn.setVisible(true);
						flag=0;
						break;
					}
					else
					{
						flag++;
						if(flag>200)
						{
							flag=0;
							a = new Alert(AlertType.WARNING);
							a.titleProperty().set("key");
							a.headerTextProperty().set("请检查输入的许可证");
							a.showAndWait();
							start.setVisible(true);
							data.setstop(1);
							break;
						}
						try {
							Thread.sleep(10);
						} catch (InterruptedException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						};
					}
				}
			}
			else
			{
				a = new Alert(AlertType.WARNING);
				a.titleProperty().set("key");
				a.headerTextProperty().set("请重新输入许可证");
				a.showAndWait();
			}
		});
		
		getkey.setOnAction(e->{
			String v = null;
			if(ten.isSelected())
			{
				v="/10";
			}
			else if(five.isSelected())
			{
				v="/50";
			}
			 try {
		            Runtime.getRuntime().exec(
		                    "cmd /c start http://127.0.0.1:10002/gen"+v);
		        } catch (IOException e1) {
		            e1.printStackTrace();
		        }
		});
		
		exit.setOnAction(e->{
			server.mystop();
			data.setstop(1);
			System.exit(0);
		});
		
		myreturn.setOnAction(e->{
			data.setstop(1);
			getkey.setVisible(true);
			start.setVisible(true);
			id.setVisible(true);
			password.setVisible(true);
			key.setVisible(true);
			idtext.setVisible(true);
			passwordtext.setVisible(true);
			keytext.setVisible(true);
			
			text.setVisible(false);
			myreturn.setVisible(false);
			//exit.setVisible(false);
			
			flagwait=1;
		});
		
		
	}

}

package application;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Label;
import javafx.scene.control.Alert.AlertType;

public class Monitor extends Thread{
	@FXML private Alert a;
	@FXML private Label text;
	@SuppressWarnings("unused")
	private String road;
	private Data data;
	
	public void run()
	{
		
		//File f=new File(road+"\\status.txt");
		//String line;
		
		while(true)
		{
			try {
				Thread.sleep(3000);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			if(!(data.getflag().equals("GOOD")||data.getflag()==null||data.getflag().equals("null")))
			{
				Platform.runLater(new Runnable() {
				    @Override
				    public void run() {
				        //更新JavaFX的主线程的代码放在此处
				    	text.setText("程序终止运行，请退出程序");
						a = new Alert(AlertType.ERROR);
						a.titleProperty().set("shutdowm");
						a.headerTextProperty().set(data.getflag());
						a.showAndWait();
				    }
				});
				break;
			}
			else
			{
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}

	public void mystart(Alert a2, Label text2, String road, Data data) {
		// TODO Auto-generated method stub
		this.a=a2;
		this.text=text2;
		this.road=road;
		this.data=data;
	}

}

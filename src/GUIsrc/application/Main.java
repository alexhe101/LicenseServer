package application;
	
import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Parent;
import javafx.scene.Scene;


public class Main extends Application {
	@Override
	public void start(Stage stage) throws IOException {
		Parent root=FXMLLoader.load(getClass().getResource("Scene.fxml"));
		Scene scene = new Scene(root);
		stage.setTitle("Cient"); // displayed in window's title bar
	    stage.setScene(scene);
	    stage.show();
	}
	
	public static void main(String[] args) {
		launch(args);
	}
}

package com.automationanywhere.botcommand.samples.commands.basic;

import com.automationanywhere.botcommand.data.impl.StringValue;
import com.automationanywhere.commandsdk.annotations.BotCommand;
import com.automationanywhere.commandsdk.annotations.CommandPkg;
import com.automationanywhere.commandsdk.annotations.Execute;
import com.automationanywhere.commandsdk.annotations.Idx;
import com.automationanywhere.commandsdk.annotations.Pkg;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;

import com.sun.jna.platform.win32.Advapi32;
import com.sun.jna.platform.win32.Winsvc;

import static com.automationanywhere.commandsdk.model.AttributeType.TEXT;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "ServiceCommunicator", label = "[[ServiceCommunicator.label]]",
		node_label = "[[ServiceCommunicator.node_label]]", description = "[[ServiceCommunicator.description]]", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[ServiceCommunicator.return_label]]", return_type = STRING, return_required = true)
public class ServiceCommunicator {
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public StringValue action(
			//Idx 1 would be displayed first, with a text box for entering the value.
			@Idx(index = "1", type = TEXT) 
			//UI labels.
			@Pkg(label = "[[ServiceCommunicator.firstString.label]]")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty 
			String serviceName) {


		// Load Advapi32 library
		Advapi32 advapi32 = Advapi32.INSTANCE;
		Winsvc.SC_HANDLE serviceManager = advapi32.OpenSCManager(null, null, Winsvc.SC_MANAGER_ALL_ACCESS);



		if (serviceManager != null) {
			Winsvc.SC_HANDLE service = advapi32.OpenService(serviceManager, serviceName, Winsvc.SERVICE_ALL_ACCESS);



			if (service != null) {
				// Start the service
				if (advapi32.StartService(service, 0, null)) {
					return new StringValue("Service started successfully.");
				} else {
					System.err.println("Failed to start service.");
				}



				// Stop the service
				if (advapi32.ControlService(service, Winsvc.SERVICE_CONTROL_STOP, new Winsvc.SERVICE_STATUS())) {
					System.out.println("Service stopped successfully.");
				} else {
					System.err.println("Failed to stop service.");
				}



				// Close service handle
				advapi32.CloseServiceHandle(service);
			} else {
				System.err.println("Failed to open service.");
			}



			// Close service manager handle
			advapi32.CloseServiceHandle(serviceManager);
		} else {
			System.err.println("Failed to open Service Control Manager.");
		}
		return new StringValue("Failed to start service.");
	}
}

/*
 * Copyright (c) 2019 Automation Anywhere.
 * All rights reserved.
 *
 * This software is the proprietary information of Automation Anywhere.
 * You shall use it only in accordance with the terms of the license agreement
 * you entered into with Automation Anywhere.
 */
/**
 *
 */
package com.automationanywhere.botcommand.samples.commands.basic;

import com.automationanywhere.botcommand.data.Value;
import com.automationanywhere.botcommand.data.impl.StringValue;
import com.automationanywhere.commandsdk.annotations.BotCommand;
import com.automationanywhere.commandsdk.annotations.CommandPkg;
import com.automationanywhere.commandsdk.annotations.Execute;
import com.automationanywhere.commandsdk.annotations.Idx;
import com.automationanywhere.commandsdk.annotations.Pkg;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;
import com.automationanywhere.commandsdk.model.DataType;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.util.Map;

import static com.automationanywhere.commandsdk.model.AttributeType.*;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

/**
 *<pre>
Concatenates the second string to the end of first string. 
Accepts two String inputs. The resulting string by appending second string atthe end of the first string would be sent as an output to a variable of type String. 
Both first and second strings must be Not NULL and providing the output variable is also mandatory. 

This class displays following
	1.How to convert a POJO to AA command action.
	2.Externalize and internationalize the UI labels.
	3.Externalize and internationalize the exception messages.
	4.Add validation rules.

Write the simple java class for the required action.
	1.Create an method (action) with two string parameters as input and StringValue as output.
	2.Write the business logic for concatenation.

How to convert a POJO to AA command action with validation rules.
	1.Configure the class
		1.Add BotCommand annotation to the class, to make it eligible for converting to AA action.
		2.Add CommandPkg to provide details about the UI packaging. 
			1.Provide the mandatory name attribute for identification of the action. It must be unique inside a package.
			2.Provide UI labels like label (mandatory), description, node_label,icon.
			3.Provide return attributes so that AA can store the output of the action. Our actions returns a String and is mandatory so configure the return_type as String and made the return_required as true.

	2.Configure the method. 
		Annotate the action entry method with Execute. Please note all parameters need to be annotated when a method has Execute annotation.

	3.Configuring the parameters
		1.Add the Idx annotation on the required parameters. The format for index is table of content style, where the entry before the last �.� denotes the parent. The UI will display the parameters in a sorted manner based on index.
		2.Add the type, in our case we want to display a textbox to accept the strings.
		3.Add the Pkg annotation with appropriate label to display in the UI.
		4.Since we want the parameters to be mandatory add NotEmpty to the parameter.

Externalize and internationalize the UI labels.
	1.This applicable on labels and description in CommandPkg and Pkg annotations only.
	2.Copy the entry from one for the labels/description and add it to locales/en_US.json located in src/main/resources.
	3.Ensure that the entry has a unique key inside the json.
	4.In the class replace the label value with the key surrounded with �[[� and �]]�.
	5.Repeat for all labels and descriptions in the action.
	6.Internationalize the json for other languages as needed and copy them in locales folder with appropriate locales identifier, viz. ja_JP forJapanese.

Externalize and internationalize the exception messages.
	1.Create Messages using the MessagesFactory by providingthe appropriate message property file.
	2.Move all exception messages to the property file.
	3.Ensure that the entry has unique identifier.
	4.Fetch the entries using the getString on the Messages object created in first step and providing the identifier.
	5.Internationalize the property for other languages as needed and copy themin same folder with appropriate locales identifier, viz. ja_JP forJapanese.

 * </pre>
 * 
 * @author Raj Singh Sisodia
 */

//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "TriggerAPI", label = "Trigger API",
		node_label = "Trigger API", description = "Triggers an API and does not wait for response", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "Assign status to the variable", return_type = STRING, return_required = true)
public class TriggerAPI {
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	private static final Logger LOGGER = LogManager.getLogger(TriggerAPI.class);

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public Value<String> action(
			//Idx 1 would be displayed first, with a text box for entering the value.
			@Idx(index = "1", type = TEXT) 
			//UI labels.
			@Pkg(label = "Enter the URL")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty 
			String urlString,
			
			@Idx(index = "2", type = DICTIONARY)
			@Pkg(label = "Enter the headers in this dictionary")
			@NotEmpty
			Map<String, StringValue> headers,
			@Idx(index = "3", type = NUMBER )
			//UI labels.
			@Pkg(label = "Enter readTimeOut time in millisecond",default_value="5000",default_value_type = DataType.NUMBER)
			@NotEmpty
			Double readTimeOut,
			@Idx(index = "4", type = NUMBER )
			//UI labels.
			@Pkg(label = "Enter connectionTimeOut in millisecond",default_value_type = DataType.NUMBER)
			Double connTimeOut) {
		
		//Internal validation, to disallow empty strings. No null check needed as we have NotEmpty on firstString.
		try {
			LOGGER.traceEntry();
			// Create a URL object
			URL url = new URL(urlString);

			// Open a connection
			HttpURLConnection connection = (HttpURLConnection) url.openConnection();

			// Set the request method to POST
			connection.setRequestMethod("POST");

			// Set headers if any are provided
			if (headers != null) {
				for (Map.Entry<String, StringValue> header : headers.entrySet()) {
					connection.setRequestProperty(header.getKey(), header.getValue().toString());
				}
			}

			// Enable output for sending the request body (even if it's empty)
			connection.setDoOutput(true);

//			System.out.println("Post Request triggered");
			if(connTimeOut!=null){
				connection.setConnectTimeout(connTimeOut.intValue());
			}
			connection.setReadTimeout(readTimeOut.intValue());
			int statusCode;

			// Checking if there's a response
			try (InputStream is = connection.getInputStream()) {
				statusCode = connection.getResponseCode();
				byte[] buffer = new byte[1024];
				while (is.read(buffer) != -1) {
					// Optionally process the response
				}
			}catch (SocketTimeoutException e){
				return new StringValue("Request Sent.");

			}

			return new StringValue(statusCode);

		} catch (Exception e) {
			e.printStackTrace();
			LOGGER.error(e.getMessage());
			return new StringValue(e.getMessage());

		}

	}
}

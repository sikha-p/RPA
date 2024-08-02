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
package com.automationanywhere.botcommand.samples.commands.aa;

import com.automationanywhere.botcommand.data.Value;
import com.automationanywhere.botcommand.data.impl.StringValue;
import com.automationanywhere.commandsdk.annotations.*;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLSocketFactory;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import static com.automationanywhere.commandsdk.model.AttributeType.FILE;
import static com.automationanywhere.commandsdk.model.AttributeType.TEXT;
import static com.automationanywhere.commandsdk.model.DataType.STRING;


//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "SoapWithDefaultTrustStore", label = "[[SoapWithDefaultTrustStore.label]]",
		node_label = "[[SoapWithDefaultTrustStore.node_label]]", description = "[[SoapWithDefaultTrustStore.description]]", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[SoapWithDefaultTrustStore.return_label]]", return_type = STRING, return_required = true)
public class SoapWithDefaultTrustStore {
//	private static final String CERT_TYPE = "X.509", TLS_VER = "TLSv1.2";
	private static final Logger LOGGER = LogManager.getLogger(SSLUtility.class);

	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public Value<String> action(
			@Idx(index = "1", type = FILE)
			//UI labels.
			@Pkg(label = "[[SoapPost.firstString.label]]")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String keystorePath,
			@Idx(index = "2", type = TEXT)
			//UI labels.
			@Pkg(label = "[[SoapPost.secondString.label]]")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String soapEndpointUrl,
			@Idx(index = "3", type = TEXT)
			//UI labels.
			@Pkg(label = "[[SoapPost.thirdString.label]]")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String soapRequestPayload
				) {

		SSLUtility sslConfigurator = new SSLUtility();

		SSLSocketFactory sslSocketFactory = sslConfigurator.configureSSL(keystorePath);
		if (sslSocketFactory != null) {
			LOGGER.info("SSL Socket Factory configured successfully.");

			try {
				String response = sendSoapRequest(soapEndpointUrl, soapRequestPayload, sslSocketFactory);
				return new StringValue(response);
			} catch (IOException e) {
				LOGGER.error("Error sending SOAP request", e);
				return new StringValue(e.getMessage());
			}

		} else {
			LOGGER.error("Failed to configure SSL Socket Factory.");
		}


		return null;
	}
	public static String sendSoapRequest(String soapEndpointUrl,String soapRequestPayload,SSLSocketFactory sslSocketFactory ) throws IOException {
		URL url = new URL(soapEndpointUrl);

		// Open a connection
		HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
		connection.setSSLSocketFactory(sslSocketFactory);

		// Set the request method to POST
		connection.setRequestMethod("POST");

		// Set the request headers
		connection.setRequestProperty("Content-Type", "application/xml");
		connection.setRequestProperty("Accept", "application/xml");

		// Enable input and output streams
		connection.setDoOutput(true);
		connection.setDoInput(true);

		// Send the SOAP request
		try (DataOutputStream wr = new DataOutputStream(connection.getOutputStream())) {
			wr.writeBytes(soapRequestPayload);
			wr.flush();
		}

		// Get the response code
		int responseCode = connection.getResponseCode();
		StringBuilder response = new StringBuilder();

		// Read the response or error stream based on the response code
		BufferedReader in;
		if (responseCode == 200) {
			in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		} else {
			in = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
		}

		String inputLine;
		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();

		return "Response Code: " + responseCode + "\nResponse: " + response.toString();
	}

	}


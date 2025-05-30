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
import com.automationanywhere.botcommand.exception.BotCommandException;
import com.automationanywhere.commandsdk.annotations.BotCommand;
import com.automationanywhere.commandsdk.annotations.CommandPkg;
import com.automationanywhere.commandsdk.annotations.Execute;
import com.automationanywhere.commandsdk.annotations.Idx;
import com.automationanywhere.commandsdk.annotations.Pkg;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

import static com.automationanywhere.commandsdk.model.AttributeType.FILE;
import static com.automationanywhere.commandsdk.model.AttributeType.TEXT;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "Base64Encode", label = "[[Base64Encode.label]]",
		node_label = "[[Base64Encode.node_label]]", description = "Encode file with Base64", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[Base64Encode.return_label]]", return_type = STRING, return_required = true)
public class Base64Encode {
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public Value<String> action(
			//Idx 1 would be displayed first, with a text box for entering the value.
			@Idx(index = "1", type = FILE)
			//UI labels.
			@Pkg(label = "File to be encoded")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty 
			String strFilePath
			
			) {
		if ("".equals(strFilePath.trim())) {
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"strFilePath"}));
		} else {
			Path file = Paths.get(strFilePath);

			String encodedString;
			try {
				byte[] data = Files.readAllBytes(file);
				encodedString = Base64.getEncoder().encodeToString(data);
			} catch (IOException var5) {
				var5.printStackTrace();
				encodedString = "";
			}

			return new StringValue(encodedString);
		}
	}
}

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
import com.automationanywhere.commandsdk.annotations.*;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.OpenOption;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

import static com.automationanywhere.commandsdk.model.AttributeType.TEXT;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "Base64Decode", label = "[[Base64Decode.label]]",
		node_label = "[[Base64Decode.node_label]]", description = "[[Base64Decode.description]]", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[Base64Decode.return_label]]", return_type = STRING, return_required = true)
public class Base64Decode {
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public Value<String> action(
			//Idx 1 would be displayed first, with a text box for entering the value.
			@Idx(index = "1", type = TEXT) 
			//UI labels.
			@Pkg(label = "Base64 string to be decoded")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty 
			String strBase64,
			@Idx(index = "2", type = TEXT)
			//UI labels.
			@Pkg(label = "File path to be saved")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String strTargetPath
			
			) {
		if ("".equals(strBase64.trim())) {
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"strBase64"}));
		} else if ("".equals(strTargetPath.trim())) {
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"strTargetPath"}));
		} else {
			String result = "Success";
			Path file = Paths.get(strTargetPath);
			byte[] data = Base64.getDecoder().decode(strBase64);

			try {
				Files.write(file, data, new OpenOption[0]);
			} catch (IOException var7) {
				var7.printStackTrace();
				result = "failed";
			}

			return new StringValue(result);
		}
	}
}

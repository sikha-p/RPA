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

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

import static com.automationanywhere.commandsdk.model.AttributeType.TEXT;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "concatenate", label = "[[LineNumber.label]]",
		node_label = "[[LineNumber.node_label]]", description = "[[LineNumber.description]]", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[LineNumber.return_label]]", return_type = STRING, return_required = true)
public class LineNumber {
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public Value<String> action(
			//Idx 1 would be displayed first, with a text box for entering the value.
			@Idx(index = "1", type = TEXT) 
			//UI labels.
			@Pkg(label = "[[LineNumber.firstString.label]]")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty 
			String metaData
			
			) {

		//Internal validation, to disallow empty strings. No null check needed as we have NotEmpty on firstString.
		String matched = "";
		try {
			Pattern pattern = Pattern.compile("executeNode(\\d+)");
			Matcher matcher = pattern.matcher(metaData);


			// Extract and print the matching lines
			while (matcher.find()) {
				matched = matcher.group(1);
			}


		} catch (PatternSyntaxException e) {
			System.err.println("Invalid regex pattern: " + e.getMessage());
		} catch (IllegalStateException e) {
			System.err.println("Error processing the stack trace: " + e.getMessage());
		} catch (Exception e) {
			System.err.println("An unexpected error occurred: " + e.getMessage());
		}
		return new StringValue(matched);
	}
}

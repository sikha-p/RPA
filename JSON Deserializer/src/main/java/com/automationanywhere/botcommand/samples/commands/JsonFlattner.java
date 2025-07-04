package com.automationanywhere.botcommand.samples.commands;


import com.automationanywhere.botcommand.data.Value;
import com.automationanywhere.botcommand.data.impl.*;
import com.automationanywhere.botcommand.exception.BotCommandException;
import com.automationanywhere.commandsdk.annotations.*;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;
import com.automationanywhere.commandsdk.model.AttributeType;
import com.automationanywhere.commandsdk.model.DataType;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import com.github.wnameless.json.flattener.JsonFlattener;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;


import static com.automationanywhere.commandsdk.model.AttributeType.FILE;
import static com.automationanywhere.commandsdk.model.AttributeType.TEXT;

//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "JsonFlattner", label = "To Dictionary",
		node_label = "To Dictionary", description = "Deserialize any JSON file into a flat dictionary structure", icon = "pkg.svg",

		//Return type information. return_type ensures only the right kind of variable is provided on the UI.
		return_label = "[[JsonToArray.return_label]]", return_type = DataType.DICTIONARY, return_required = true)
public class JsonFlattner {
	private static final Messages MESSAGES = MessagesFactory.getMessages("com.automationanywhere.botcommand.samples.messages");
	private static Logger logger = LogManager.getLogger(JsonFlattner.class);

	public JsonFlattner() {
	}

	//Identify the entry point for the action. Returns a Value<String> because the return type is String.
	@Execute
	public DictionaryValue action(
			@Idx(
					index = "1",
					type = AttributeType.RADIO,
					options = {
							@Idx.Option(
									index = "1.1",
									pkg =
									@Pkg(
											label =
													"Enter JSON File Path",
											value = "jsonfilepath"
											)),
							@Idx.Option(
									index = "1.2",
									pkg =
									@Pkg(
											label =
													"Enter JSON String",
											value = "STRING"))
					})
			@Pkg(
					label = "Input JSON",
					default_value_type = DataType.STRING
//					default_value = "FILE"
			)
			String inputJsonType,

			@Idx(index = "1.1.1", type = AttributeType.FILE)
			@Pkg(label = "File containing valid JSON string")
			String jsonFilePath,

			@Idx(index = "1.2.2", type = TEXT)
			@Pkg(label = "Enter JSON String")
			String jsonString

	) {
		if (!inputJsonType.equals("jsonfilepath") || jsonFilePath != null && !"".equals(jsonFilePath.trim())) {
			if (inputJsonType.equals("jsonstring") && (jsonString == null || "".equals(jsonString.trim()))) {
				logger.debug("[MAIN: Action]: Null Exception Triggered : " + inputJsonType + " Input Json :" + jsonString);

				throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"jsonString"}));
			} else {
				String JsonString = "";
				JSONParser parser = new JSONParser();
				Map<String, Value> flattenedJson = new HashMap();
				DictionaryValue dict = new DictionaryValue();
				logger.trace("[MAIN: Action]: Json parsing started: " + inputJsonType);
				try {
					logger.debug("[MAIN: Action]: Json parsing started: " + inputJsonType);
					Object obj;
					if (inputJsonType.equals("jsonfilepath")) {
						logger.debug("[MAIN: Action]: Json parsing started: " + inputJsonType);
						obj = parser.parse(new FileReader(jsonFilePath));
					} else {
						logger.debug("[MAIN: Action]: Json parsing started: " + inputJsonType);
						obj = parser.parse(jsonString);
					}

					JsonString = obj.toString();
					logger.debug("[MAIN: Action]: Json object converted to string:" + JsonString);
					if (JsonString.trim().startsWith("[")) {
						JSONArray jsonArray = (JSONArray)obj;
						JsonString = jsonArray.toString();
						logger.debug("[MAIN: Action]: Json object converted to string identified as array object:" + JsonString);
					} else {
						JSONObject jsonObject = (JSONObject)obj;
						JsonString = jsonObject.toString();
						logger.debug("[MAIN: Action]: Json object converted to string identified as non-array object:" + JsonString);
					}

					Map<String, Object> flattenedJsonMap = JsonFlattener.flattenAsMap(JsonString);
					logger.debug("[MAIN: Action]: Json object successfully flattened into dictionary object");
					Iterator var12 = flattenedJsonMap.entrySet().iterator();

					while(var12.hasNext()) {
						Map.Entry<String, Object> entry = (Map.Entry)var12.next();
						String key = (String)entry.getKey();
						Object value = entry.getValue();
						if (value == null) {
							value = new StringValue("null");
						}

						String classname = value.getClass().getSimpleName();
						logger.debug("[MAIN: Action]: Class identified as:" + classname);
						switch (classname) {
							case "String":
								flattenedJson.put(key, new StringValue(value));
								break;
							case "Integer":
							case "Double":
							case "Long":
								flattenedJson.put(key, new NumberValue(value));
								break;
							case "Boolean":
								flattenedJson.put(key, new BooleanValue(value));
								break;
							default:
								logger.debug("[MAIN: Action]: Unidentified class for key:" + key);
								flattenedJson.put(key, new StringValue(value));
						}
					}

					dict.set(flattenedJson);
					return dict;
				} catch (ParseException var17) {
					var17.printStackTrace();
					logger.error("[MAIN: Action]: Exception Occurred: Failed to parse the input Json file");
					logger.error("[MAIN: Action]: Exception Occurred: Returning NULL Dictionary Object");
					logger.error("[MAIN: Action]: Exception Occurred: Validate input Json file");
					throw new BotCommandException("Failed to parse input JSON, please validate JSON and try again.");
				} catch (IOException var18) {
					var18.printStackTrace();
					logger.error("[MAIN: Action]: Exception Occurred: " + var18.getMessage());
					logger.error("[MAIN: Action]: Exception Occurred: Returning NULL Dictionary Object");
					throw new BotCommandException("Exception Occurred, " + var18.getMessage());
				} catch (Exception var19) {
					var19.printStackTrace();
					logger.error("[MAIN: Action]: Exception Occurred: " + var19.getMessage());
					logger.error("[MAIN: Action]: Exception Occurred: Returning NULL Dictionary Object");
					throw new BotCommandException("Exception Occurred, refer to bot_launcher.log for details " + var19.getLocalizedMessage());
				}
			}
		} else {
			logger.debug("[MAIN: Action]: Null Exception Triggered : " + inputJsonType + " Input Json :" + jsonFilePath);
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"jsonFilePath"}));
		}
	}

}

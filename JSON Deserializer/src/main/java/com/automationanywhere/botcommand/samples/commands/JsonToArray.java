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
package com.automationanywhere.botcommand.samples.commands;

import com.automationanywhere.botcommand.data.Value;
import com.automationanywhere.botcommand.data.impl.*;
import com.automationanywhere.botcommand.data.model.Schema;
import com.automationanywhere.botcommand.data.model.table.Row;
import com.automationanywhere.botcommand.data.model.table.Table;
import com.automationanywhere.botcommand.exception.BotCommandException;
import com.automationanywhere.commandsdk.annotations.*;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;
import com.automationanywhere.commandsdk.model.AttributeType;
import com.automationanywhere.commandsdk.model.DataType;
import com.github.wnameless.json.flattener.JsonFlattener;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.automationanywhere.commandsdk.model.AttributeType.*;
import static com.automationanywhere.commandsdk.model.DataType.STRING;
import static com.automationanywhere.commandsdk.model.DataType.TABLE;



//BotCommand makes a class eligible for being considered as an action.
@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "JsonToTable", label = "ToTable",
		node_label = "To Table", description = "Deserialize any JSON file into a flat table structure", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[JsonToArray.return_label]]", return_type = TABLE, return_required = true)
public class JsonToArray {
	private static final Messages MESSAGES = MessagesFactory.getMessages("com.automationanywhere.botcommand.samples.messages");
	private static Logger logger = LogManager.getLogger(JsonToArray.class);
	public int rowIndex = 0;
	String JsonString = "";

	public JsonToArray() {
	}


	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public TableValue action(

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
				JSONParser parser = new JSONParser();
				Map<String, Value> flattenedJson = new HashMap();
				DictionaryValue dict = new DictionaryValue();
				Map<String, Value> tableHeader = new HashMap();
				int tableColumnOrder = 0;
				Table finalJsonTable = new Table();
				TableValue finalJsonTableValue = new TableValue();
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

					logger.debug("[MAIN: Action]: Json parsed object created");
					this.JsonString = obj.toString();
					logger.debug("[MAIN: Action]: Json object converted to string:" + this.JsonString);
					if (this.JsonString.trim().startsWith("[")) {
						JSONArray jsonArray = (JSONArray)obj;
						this.JsonString = jsonArray.toString();
						logger.debug("[MAIN: Action]: Json object converted to string identified as array object:" + this.JsonString);
					} else {
						JSONObject jsonObject = (JSONObject)obj;
						this.JsonString = jsonObject.toString();
						logger.debug("[MAIN: Action]: Json object converted to string identified as non-array object:" + this.JsonString);
					}

					Map<String, Object> flattenedJsonMap = JsonFlattener.flattenAsMap(this.JsonString);
					logger.debug("[MAIN: Action]: Json object successfully flattened into dictionary object");
					String[][] jsonToTableMapping = new String[flattenedJsonMap.size() + 1][5];
					int index = 0;
					int maxRowCount = 0;

					for(Iterator var17 = flattenedJsonMap.entrySet().iterator(); var17.hasNext(); ++index) {
						Map.Entry<String, Object> entry = (Map.Entry)var17.next();
						String key = (String)entry.getKey();
						Object value = entry.getValue();
						String tableColumnHeader = this.CreateColumnHeader(key);
						if (!tableHeader.containsKey(tableColumnHeader)) {
							tableHeader.put(tableColumnHeader, new NumberValue(tableColumnOrder));
							++tableColumnOrder;
						}

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
								try {
									flattenedJson.put(key, new StringValue(value));
								} catch (Exception var25) {
									flattenedJson.put(key, new NumberValue(value));
								}
								break;
							case "Boolean":
								flattenedJson.put(key, new BooleanValue(value));
								break;
							default:
								logger.debug("[MAIN: Action]: Unidentified class for key:" + key);
								flattenedJson.put(key, new StringValue(value));
						}

						jsonToTableMapping[index][0] = key;
						jsonToTableMapping[index][1] = value.toString();
						jsonToTableMapping[index][2] = tableColumnHeader;
						jsonToTableMapping[index][3] = String.valueOf(this.rowIndex + 1);
						jsonToTableMapping[index][4] = ((Value)tableHeader.get(tableColumnHeader)).toString();
						if (maxRowCount < this.rowIndex + 1) {
							maxRowCount = this.rowIndex + 1;
						}
					}

					++maxRowCount;
					String[][] finalArray = this.jsontoTable(index, maxRowCount, tableColumnOrder, jsonToTableMapping);
					logger.debug("[MAIN: Action]: Successfully created a two dimensional array from input JSON");
					logger.debug("[MAIN: Action]: Process for creating TABLE Started");
					List<Row> rows = new ArrayList();
					Row row = new Row();
					List<Value> values = new ArrayList();
					List<Schema> tableSchema = new ArrayList();
					finalJsonTable.setSchema(tableSchema);
					finalJsonTable.setRows(rows);
					finalJsonTableValue.set(finalJsonTable);
					logger.debug("[MAIN: Action]: Process for creating TABLE schema started");

					int iRow;
					for(iRow = 0; iRow < finalArray[0].length; ++iRow) {
						String columnName = finalArray[0][iRow];
						if (columnName.matches("^\\..*") || columnName.matches("^\\[[0-9]*]")) {
							columnName = columnName.substring(columnName.indexOf(".") + 1);
						}

						tableSchema.add(iRow, new Schema(columnName));
					}

					logger.debug("[MAIN: Action]: Process for creating TABLE schema completed");
					logger.debug("[MAIN: Action]: Process for inserting TABLE rows started");

					for(iRow = 1; iRow < finalArray.length; ++iRow) {
						for(int iCol = 0; iCol < finalArray[iRow].length; ++iCol) {
							values.add(iCol, new StringValue(finalArray[iRow][iCol]));
						}

						row.setValues(values);
						rows.add(iRow - 1, row);
						values = new ArrayList();
						row = new Row();
					}

					logger.debug("[MAIN: Action]: Process for inserting TABLE rows completed");
					return finalJsonTableValue;
				} catch (ParseException var26) {
					var26.printStackTrace();
					logger.error("[MAIN: Action]: Exception Occurred: Failed to parse the input Json file");
					logger.error("[MAIN: Action]: Exception Occurred: Returning NULL Table Object");
					logger.error("[MAIN: Action]: Exception Occurred: Validate input Json file");
					throw new BotCommandException("Failed to parse input JSON, please validate JSON and try again.");
				} catch (IOException var27) {
					var27.printStackTrace();
					logger.error("[MAIN: Action]: Exception Occurred: " + var27.getMessage());
					logger.error("[MAIN: Action]: Exception Occurred: Returning NULL Table Object");
					throw new BotCommandException("Exception Occurred, " + var27.getMessage());
				} catch (Exception var28) {
					var28.printStackTrace();
					logger.error("[MAIN: Action]: Exception Occurred: " + var28.getMessage());
					logger.error("[MAIN: Action]: Exception Occurred: Returning NULL Table Object");
					throw new BotCommandException("Exception Occurred, refer to bot_launcher.log for details " + var28.getMessage());
				}
			}
		} else {
			logger.debug("[MAIN: Action]: Null Exception Triggered : " + inputJsonType + " Input Json :" + jsonFilePath);
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"jsonFilePath"}));
		}
	}

	private String CreateColumnHeader(String inputKey) {
		Pattern pattern = Pattern.compile("\\[[0-9]+\\]+");
		Matcher matcher = pattern.matcher(inputKey);

		int iCount;
		for(iCount = 0; matcher.find(); ++iCount) {
			String index = matcher.group(0);
			index = index.replaceAll("\\[|\\]", "");
			if (iCount == 0) {
				this.rowIndex = Integer.parseInt(index);
			} else if (inputKey.contains("][")) {
				inputKey = inputKey.replaceAll("\\[[0-9]+\\]", "");
			} else {
				inputKey = inputKey.replaceFirst("\\[[0-9]+\\]", "");
				inputKey = inputKey.replaceAll("\\[", ".");
				inputKey = inputKey.replaceAll("\\]", "");
			}
		}

		if (iCount == 0) {
			this.rowIndex = 0;
		}

		if (iCount == 1) {
			inputKey = inputKey.replaceAll("\\[[0-9]+\\]", "");
		}

		return inputKey;
	}

	private String[][] jsontoTable(int index, int rowCount, int colCount, String[][] jsonTableMapping) {
		String[][] jsontoArray = new String[rowCount][colCount];

		int iRow;
		int iCol;
		int iColumn;
		for(iRow = 0; iRow < index; ++iRow) {
			for(iCol = 0; iCol < colCount; ++iCol) {
				iColumn = Integer.parseInt(jsonTableMapping[iRow][4].replaceAll("\\.0", ""));
				if (iColumn == iCol) {
					jsontoArray[0][iCol] = jsonTableMapping[iRow][2];
					break;
				}
			}
		}

		for(iRow = 0; iRow < index; ++iRow) {
			iCol = Integer.parseInt(jsonTableMapping[iRow][4].replaceAll("\\.0", ""));
			iColumn = Integer.parseInt(jsonTableMapping[iRow][3].replaceAll("\\.0", ""));
			int colValue = Integer.parseInt(jsonTableMapping[iRow][3].replaceAll("\\.0", ""));
			jsontoArray[iColumn][iCol] = jsonTableMapping[iRow][1];
		}

		return jsontoArray;
	}

}

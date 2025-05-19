package com.automationanywhere.botcommand.samples;

import com.automationanywhere.botcommand.data.Value;
import com.automationanywhere.botcommand.data.impl.CredentialObject;
import com.automationanywhere.botcommand.data.impl.DictionaryValue;
import com.automationanywhere.botcommand.data.impl.StringValue;
import com.automationanywhere.botcommand.exception.BotCommandException;
import com.automationanywhere.commandsdk.annotations.*;
import com.automationanywhere.commandsdk.annotations.rules.NotEmpty;
import com.automationanywhere.commandsdk.i18n.Messages;
import com.automationanywhere.commandsdk.i18n.MessagesFactory;
import com.automationanywhere.commandsdk.model.AttributeType;
import com.automationanywhere.commandsdk.model.DataType;
import com.automationanywhere.core.security.SecureString;
import okhttp3.*;

import java.io.File;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import static com.automationanywhere.commandsdk.model.AttributeType.*;
import static com.automationanywhere.commandsdk.model.DataType.CREDENTIAL;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "PostRequest", label = "[[Post.label]]",
		node_label = "[[Post.node_label]]", description = "[[Post.description]]", icon = "pkg.svg",
		
		//Return type information. return_type ensures only the right kind of variable is provided on the UI. 
		return_label = "[[response]]", return_type = STRING, return_required = true)
public class CustomPost {

	@Idx(index = "7", type = GROUP)
	@Pkg(label = "Body (form-data)")
	String nameGroup;

	@Idx(index = "2", type = GROUP)
	@Pkg(label = "Basic Authentication")
	String nameGroup1;
	@Idx(index = "4.3", type = TEXT, name = "PARAMNAME")
	@Pkg(label = "PARAMNAME", default_value_type = DataType.STRING)
	@NotEmpty
	private String paramName;
	@Idx(index = "4.4", type = AttributeType.CREDENTIAL, name = "PARAMVALUE")
	@Pkg(label = "PARAMVALUE", default_value_type = CREDENTIAL)
	private SecureString paramValue;

	@Idx(index = "5.3", type = TEXT, name = "NAME")
	@Pkg(label = "NAME", default_value_type = DataType.STRING)
	@NotEmpty
	private String name;
	@Idx(index = "5.4", type = AttributeType.CREDENTIAL, name = "VALUE")
	@Pkg(label = "VALUE", default_value_type = DataType.CREDENTIAL)
	private SecureString value;

	@Idx(index = "6.3", type = TEXT, name = "BODYKEY")
	@Pkg(label = "BODYKEY", default_value_type = DataType.STRING)
	@NotEmpty
	private String bodyKey;
	@Idx(index = "6.4", type = AttributeType.TEXT, name = "BODYVALUE")
	@Pkg(label = "BODYVALUE", default_value_type = DataType.STRING)
	private String bodyValue;
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public Value<String> action(
			//Idx 1 would be displayed first, with a text box for entering the value.
			@Idx(index = "1", type = TEXT) 
			//UI labels.
			@Pkg(label = "URI")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String uri,
			@Idx(index = "2.1", type = AttributeType.CREDENTIAL)
			@Pkg(label = "Username")
			//Ensure that a validation error is thrown when the value is null.
			SecureString username,
			@Idx(index = "2.2", type = AttributeType.CREDENTIAL)
			@Pkg(label = "Password")
			//Ensure that a validation error is thrown when the value is null.
			SecureString password,

			@Idx(index = "4", type = ENTRYLIST, options = {
					@Idx.Option(index = "4.1", pkg = @Pkg(title = "PARAMNAME", label = "PARAMNAME")),
					@Idx.Option(index = "4.2", pkg = @Pkg(title = "PARAMVALUE", label = "PARAMVALUE")),
			})
			@Pkg(label = "Query Parameters")
			List<Value> customParams,
			@Idx(index = "5", type = ENTRYLIST, options = {
					@Idx.Option(index = "5.1", pkg = @Pkg(title = "NAME", label = "NAME")),
					@Idx.Option(index = "5.2", pkg = @Pkg(title = "VALUE", label = "VALUE")),
			})
			@Pkg(label = "Custom Headers")
			List<Value> customHeaders,
			@Idx(index = "6", type = ENTRYLIST, options = {
					@Idx.Option(index = "6.1", pkg = @Pkg(title = "BODYKEY", label = "BODYKEY")),
					@Idx.Option(index = "6.2", pkg = @Pkg(title = "BODYVALUE", label = "BODYVALUE")),
			})
			@Pkg(label = "Body (form-data)")

			List<Value> bodyKeyValue,
			@Idx(index = "7.1", type = TEXT)
			@Pkg(label = "Key")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String key,
			@Idx(index = "7.2", type = FILE)
			@Pkg(label = "File")
			//Ensure that a validation error is thrown when the value is null.
			@NotEmpty
			String inputFile) {

		if ("".equals(uri.trim())) {
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"uri"}));
		} else if ("".equals(inputFile.trim())) {
			throw new BotCommandException(MESSAGES.getString("emptyInputString", new Object[]{"inputFile"}));
		} else {
			if (customParams != null && customParams.size() > 0) {
				uri = uri + "?";

				String name;
				String secureValue;
				for(Iterator var9 = customParams.iterator(); var9.hasNext(); uri = uri + name + "=" + URLEncoder.encode(secureValue, StandardCharsets.UTF_8) + "&") {
					Value element = (Value)var9.next();
					Map<String, Value> customHeaderMap = ((DictionaryValue)element).get();
					name = customHeaderMap.containsKey("PARAMNAME") ? ((StringValue)customHeaderMap.get("PARAMNAME")).get() : "";
					secureValue = customHeaderMap.getOrDefault("PARAMVALUE", (Value) null) == null ? null : ((CredentialObject)customHeaderMap.get("PARAMVALUE")).get().getInsecureString();
				}

				uri = uri.substring(0, uri.length() - 1);
			}

			String responseBody;
			try {
				OkHttpClient client = (new OkHttpClient()).newBuilder().build();
				MediaType mediaType = MediaType.parse("text/plain");
				MultipartBody.Builder mRequestBody = (new MultipartBody.Builder()).setType(MultipartBody.FORM);
				if (bodyKeyValue != null && bodyKeyValue.size() > 0) {
					Iterator var25 = bodyKeyValue.iterator();

					while(var25.hasNext()) {
						Value element = (Value)var25.next();
						Map<String, Value> bodyPairs = ((DictionaryValue)element).get();
						String bodykey = bodyPairs.containsKey("BODYKEY") ? ((StringValue)bodyPairs.get("BODYKEY")).get() : "";
						String value = bodyPairs.getOrDefault("BODYVALUE", (Value) null) == null ? null : ((StringValue)bodyPairs.get("BODYVALUE")).get();
						mRequestBody.addFormDataPart(bodykey, value);
					}
				}

				mRequestBody.addFormDataPart(key, inputFile, RequestBody.create(MediaType.parse("application/octet-stream"), new File(inputFile)));
				RequestBody body = mRequestBody.build();
				Request request = (new Request.Builder()).url(uri).method("POST", body).build();
				if (username != null && password != null && !"".equals(username.getInsecureString()) && !"".equals(password.getInsecureString())) {
					Request.Builder var10000 = request.newBuilder();
					Base64.Encoder var10002 = Base64.getEncoder();
					String var10003 = username.getInsecureString();
					byte[] var33 = (var10003 + ":" + password.getInsecureString()).getBytes();
					request = var10000.addHeader("Authorization", "Basic " + var10002.encodeToString(var33)).build();
				}

				String name;
				String secureValue;
				if (customHeaders != null && customHeaders.size() > 0) {
					for(Iterator var28 = customHeaders.iterator(); var28.hasNext(); request = request.newBuilder().addHeader(name, secureValue).build()) {
						Value element = (Value)var28.next();
						Map<String, Value> customHeaderMap = ((DictionaryValue)element).get();
						name = customHeaderMap.containsKey("NAME") ? ((StringValue)customHeaderMap.get("NAME")).get() : "";
						secureValue = customHeaderMap.getOrDefault("VALUE", (Value) null) == null ? null : ((CredentialObject)customHeaderMap.get("VALUE")).get().getInsecureString();
					}
				}

				Response response = client.newCall(request).execute();
				int var30 = response.code();
				responseBody = "Status: " + var30 + "  " + response.body().string();
			} catch (Exception var20) {
				throw new BotCommandException(var20);
			}

			return new StringValue(responseBody);
		}
	}
}

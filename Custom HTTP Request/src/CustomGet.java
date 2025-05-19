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
import com.automationanywhere.toolchain.runtime.mapper.CredentialMapper;
import okhttp3.*;

import java.io.File;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.io.FileOutputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;

import static com.automationanywhere.commandsdk.model.AttributeType.*;
import static com.automationanywhere.commandsdk.model.DataType.CREDENTIAL;
import static com.automationanywhere.commandsdk.model.DataType.STRING;

@BotCommand

//CommandPks adds required information to be dispalable on GUI.
@CommandPkg(
		//Unique name inside a package and label to display.
		name = "GetRequest", label = "[[Get.label]]",
		node_label = "[[Get.node_label]]", description = "[[Get.description]]", icon = "pkg.svg")
public class CustomGet {

	@Idx(index = "2", type = GROUP)
	@Pkg(label = "Basic Authentication")
	String nameGroup1;
	@Idx(index = "4.3", type = TEXT, name = "PARAMNAME")
	@Pkg(label = "PARAMNAME", default_value_type = DataType.STRING)
	@NotEmpty
	private String paramName;
	@Idx(index = "4.4", type = AttributeType.CREDENTIAL, name = "PARAMVALUE")
	@Pkg(label = "PARAMVALUE", default_value_type = CREDENTIAL)
	private String paramValue;

	@Idx(index = "5.3", type = TEXT, name = "NAME")
	@Pkg(label = "NAME", default_value_type = DataType.STRING)
	@NotEmpty
	private String name;
	@Idx(index = "5.4", type = AttributeType.CREDENTIAL, name = "VALUE")
	@Pkg(label = "VALUE", default_value_type = DataType.CREDENTIAL)
	private String value;
	
	//Messages read from full qualified property file name and provide i18n capability.
	private static final Messages MESSAGES = MessagesFactory
			.getMessages("com.automationanywhere.botcommand.samples.messages");

	//Identify the entry point for the action. Returns a Value<String> because the return type is String. 
	@Execute
	public void action(
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
			@Idx(index = "6", type = FILE)
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
				for(Iterator var7 = customParams.iterator(); var7.hasNext(); uri = uri + name + "=" + URLEncoder.encode(secureValue, StandardCharsets.UTF_8) + "&") {
					Value element = (Value)var7.next();
					Map<String, Value> customHeaderMap = ((DictionaryValue)element).get();
					name = customHeaderMap.containsKey("PARAMNAME") ? ((StringValue)customHeaderMap.get("PARAMNAME")).get() : "";
					secureValue = customHeaderMap.getOrDefault("PARAMVALUE", (Value) null) == null ? null : ((CredentialObject)customHeaderMap.get("PARAMVALUE")).get().getInsecureString();
				}

				uri = uri.substring(0, uri.length() - 1);
			}

			CloseableHttpClient httpClient = HttpClientBuilder.create().build();
			HttpGet request = new HttpGet(uri);
			request.addHeader("Accept", "*/*");
			if (username != null && password != null && !"".equals(username.getInsecureString()) && !"".equals(password.getInsecureString())) {
				Base64.Encoder var10002 = Base64.getEncoder();
				String var10003 = username.getInsecureString();
				byte[] var27 = (var10003 + ":" + password.getInsecureString()).getBytes();
				request.addHeader("Authorization", "Basic " + var10002.encodeToString(var27));
			}

			if (customHeaders != null && customHeaders.size() > 0) {
				Iterator var21 = customHeaders.iterator();

				while(var21.hasNext()) {
					Value element = (Value)var21.next();
					Map<String, Value> customHeaderMap = ((DictionaryValue)element).get();
					String name = customHeaderMap.containsKey("NAME") ? ((StringValue)customHeaderMap.get("NAME")).get() : "";
					String secureValue = customHeaderMap.getOrDefault("VALUE", (Value) null) == null ? null : ((CredentialObject)customHeaderMap.get("VALUE")).get().getInsecureString();
					request.addHeader(name, secureValue);
				}
			}

			try {
				CloseableHttpResponse response = httpClient.execute(request);

				try {
					HttpEntity entity = response.getEntity();
					if (entity != null) {
						FileOutputStream outstream = new FileOutputStream(inputFile);

						try {
							entity.writeTo(outstream);
						} catch (Throwable var16) {
							try {
								outstream.close();
							} catch (Throwable var15) {
								var16.addSuppressed(var15);
							}

							throw var16;
						}

						outstream.close();
					}
				} catch (Throwable var17) {
					if (response != null) {
						try {
							response.close();
						} catch (Throwable var14) {
							var17.addSuppressed(var14);
						}
					}

					throw var17;
				}

				if (response != null) {
					response.close();
				}
			} catch (Exception var18) {
				throw new BotCommandException(MESSAGES.getString("apiCallError", new Object[]{"uri"}));
			}
		}
	}
}

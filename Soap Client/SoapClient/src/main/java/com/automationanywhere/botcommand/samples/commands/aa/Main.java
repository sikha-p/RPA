package com.automationanywhere.botcommand.samples.commands.aa;

import com.automationanywhere.botcommand.data.Value;

public class Main {

    public static void main(String[] args) {
        soapWithWindowsTrustStore sp = new soapWithWindowsTrustStore();
        Value<String> js = sp.action("path/to/keystorefile",
                "soap url",
                "soap request payload");
        System.out.println(js.toString());


    }


}

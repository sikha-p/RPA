
# Creating an SDK for Soap Service with SSL Authentication







## Documentation

Download the package SDK from https://docs.automationanywhere.com/bundle/enterprise-v2019/page/enterprise-cloud/topics/developer/cloud-package-dev-kit-rel-note.html.

Remove the sample files.

Create a SSL utility for ssl authentication.

Create a function returning SSLSocketFactory.

Initialize the keystore as default or windows, loading the file that would needed for authentication.

Initialize the truststore as default or windows. The algorithm needs to explicitly specified as a public certificate(ex: SUNX509).

Return the SSLSocketFactory.

Create the action method which will be used in the bot.

Create an object for the previous class.

Use this object for SSL authentication for your soap service.

Make connection to the soap service.

Once the jar is complete with all the configurations build it and upload it to the control room.




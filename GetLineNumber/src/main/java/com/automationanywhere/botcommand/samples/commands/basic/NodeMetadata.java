package com.automationanywhere.botcommand.samples.commands.basic;

import com.automationanywhere.botcommand.data.impl.StringValue;
import com.automationanywhere.commandsdk.annotations.BotCommand;
import com.automationanywhere.commandsdk.annotations.CommandPkg;
import com.automationanywhere.commandsdk.annotations.Execute;
import com.automationanywhere.commandsdk.annotations.VariableExecute;

import static com.automationanywhere.commandsdk.model.DataType.STRING;

@BotCommand
@CommandPkg(
        //Unique name inside a package and label to display.
        name = "NodeMetadata", label = "[[NodeMetadata]]",
        node_label = "[[NodeMetadata]]", description = "[[Returns Node Metadata]]", icon = "pkg.svg",

        //Return type information. return_type ensures only the right kind of variable is provided on the UI.
        return_label = "[[NodeMetadata.return_label]]", return_type = STRING, return_required = true)

public class NodeMetadata {

    @Execute
    public StringValue action(

          ) {
        try {
            Thread thread = new Thread();
            thread.currentThread();
            StackTraceElement[] stackTrace = thread.currentThread().getStackTrace();
            StringBuilder result = new StringBuilder();
            for (StackTraceElement element : stackTrace) {
                result.append(element.toString()).append("\n");
            }
            return new StringValue(result.toString());
        } catch (Exception e) {
            // Log or handle the exception
            System.err.println("An error occurred while fetching the stack trace: " + e.getMessage());
            return new StringValue("Error: " + e.getMessage());
        }
    }


}
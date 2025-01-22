package com.automationanywhere.botcommand.samples.commands.basic;

public class Main {
    public static void main(String[] args) {

//        String stackTrace = "java.base/java.lang.Thread.getStackTrace(Unknown Source)\n" +
//                "com.automationanywhere.botcommand.samples.commands.basic.NodeMetadata.action(NodeMetadata.java:28)\n" +
//                "com.automationanywhere.botcommand.samples.commands.basic.NodeMetadataCommand.execute(NodeMetadataCommand.java:38)\n" +
//                "com.automationanywhere.toolchain.runtime.BotCommand.execute(BotCommand.java:73)\n" +
//                "java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\n" +
//                "java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(Unknown Source)\n" +
//                "java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)\n" +
//                "java.base/java.lang.reflect.Method.invoke(Unknown Source)\n" +
//                "com.automationanywhere.bot.metrics.TimerInvocationHandler.invoke(TimerInvocationHandler.java:65)\n" +
//                "com.sun.proxy.$Proxy43.execute(Unknown Source)\n" +
//                "com.automationanywhere.botrunner.bot.Bot_Sample_hello.executeNode1(Bot_Sample_hello.java:189)\n" +
//                "com.automationanywhere.botrunner.bot.Bot_Sample_hello.play(Bot_Sample_hello.java:248)\n" +
//                "com.automationanywhere.botrunner.Main.play(Main.java:51)\n" +
//                "com.automationanywhere.botcommand.task.commands.RunTask.runTaskWithHandledExceptions(RunTask.java:245)\n" +
//                "com.automationanywhere.botcommand.task.commands.RunTask.runTask(RunTask.java:161)\n" +
//                "com.automationanywhere.botcommand.task.commands.RunTaskCommand.execute(RunTaskCommand.java:264)\n" +
//                "com.automationanywhere.toolchain.runtime.BotCommand.execute(BotCommand.java:73)\n" +
//                "java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\n" +
//                "java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(Unknown Source)\n" +
//                "java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)\n" +
//                "java.base/java.lang.reflect.Method.invoke(Unknown Source)\n" +
//                "com.automationanywhere.bot.metrics.TimerInvocationHandler.invoke(TimerInvocationHandler.java:65)\n" +
//                "com.sun.proxy.$Proxy42.execute(Unknown Source)\n" +
//                "com.automationanywhere.botrunner.bot.Bot_MainBot.executeNode8(Bot_MainBot.java:269)\n" +
//                "com.automationanywhere.botrunner.bot.Bot_MainBot.play(Bot_MainBot.java:311)\n" +
//                "com.automationanywhere.botrunner.Main.play(Main.java:63)\n" +
//                "com.automationanywhere.botengine.service.impl.BotLauncherImpl.runBot(BotLauncherImpl.java:22)\n" +
//                "com.automationanywhere.botengine.service.impl.DispatcherImpl.lambda$start$9(DispatcherImpl.java:631)\n" +
//                "com.automationanywhere.botengine.utils.ThreadUtil.lambda$withThreadContext$0(ThreadUtil.java:20)\n" +
//                "java.base/java.util.concurrent.CompletableFuture$AsyncSupply.run(Unknown Source)\n" +
//                "java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)\n" +
//                "java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)\n" +
//                "java.base/java.lang.Thread.run(Unknown Source)\n";

//        LineNumber glt = new LineNumber();
//        System.out.println(glt.action(stackTrace));

        NodeMetadata sm = new NodeMetadata();
        System.out.println(sm.action());


    }
}




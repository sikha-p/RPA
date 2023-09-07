using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using WindowsAccessBridgeInterop;
using System.Windows.Forms;
using System.IO;
using log4net.Core;
using log4net.Repository.Hierarchy;
using log4net;
using log4net.Layout;
using log4net.Appender;
using static log4net.Appender.ColoredConsoleAppender;


// Author: Sikha P
// Department : Partner Solution Desk(PSD)
// Date: 24-08-2023
// Description: This program helps to do operations in Oracle EBS application. 
//              This code uses WindowsAccessBridgeInterop.dll .NET library to interact with the controls/elements in the Oracle EBS application.


namespace OracleEBSOperations
{
    public class Operations
    {
        public static Int32 counter = 0;

        public static void ConfigureLog(string logFolder, string logLevel)
        {
            Log.Configure(logFolder, logLevel);
        }

   
        // Depth-first search to find an AccessibleContext with a specific attribute.
        public static AccessibleNode GetPopUp()
        {

            try
            {
                AccessBridge Java = new AccessBridge();
                IntPtr handle = new IntPtr(0);
                List<IntPtr> windowHandles = new List<IntPtr>();
                Java.Initialize(false);
                Application.DoEvents();
                //Get the Oracle EBS application process from the running processes in the system using the process name "jp2launcher" .
                Log.InfoDebugTrace("Trying to get the Oracle EBS application process from the running processes in the system using the process name jp2launcher");

                foreach (Process window in Process.GetProcesses())
                {
                    window.Refresh();
                    try
                    {
                        if (window.HasExited == false)
                        {
                            Console.WriteLine(window.ProcessName);
                            if (window.ProcessName.Contains("jp2launcher"))
                            {
                                Log.InfoDebugTrace("Identified the Oracle EBS application process");
                                handle = window.MainWindowHandle;
                                Log.InfoDebugTrace("Got the Oracle EBS application process handle");
                                break;
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        Log.Error("From process search catch" + ex.Message);
                        continue;
                    }
                }
                //Get the Oracle application window using the process handle.
                Log.InfoDebugTrace("Get the Oracle application window using the process handle.");
                Java.Functions.GetAccessibleContextFromHWND(handle, out int vmid, out JavaObjectHandle javaObjectHandle);
                AccessibleWindow win = Java.CreateAccessibleWindow(handle);
                //Get the root element in the oracle application to search for the pop up element
                Log.InfoDebugTrace("Get the root element in the oracle application to search for the pop up element");
                var rootpane = win.GetChildren().ToArray()[0];        
                return searchPopup(rootpane, handle, Java);
            }
            catch (Exception ex)
            {
                Log.Error("Final catch" + ex.Message);
                return null;
            }

        }

        public static AccessibleNode searchPopup(AccessibleNode accessibleNode, IntPtr handle, AccessBridge Java)
        {
            Log.InfoDebugTrace("Get each elements/children's properties");
            PropertyList list = accessibleNode.GetProperties(PropertyOptions.AccessibleContextInfo);
            Log.InfoDebugTrace("PropertyList : " + list.ToString());
            Console.WriteLine(list[3].Value);
            Console.WriteLine(list[0].Value);
            String state = list[5].Value.ToString();
            Console.WriteLine(state);
            Log.InfoDebugTrace("Check the state property has model & active values");
            if (state.Contains("modal") && state.Contains("active"))
            {
                Log.InfoDebugTrace("state.Contains(modal) && state.Contains(active)");
                return accessibleNode;
            }
            Log.InfoDebugTrace("state doesn't Contains(modal & active)");
            Log.InfoDebugTrace("do the same for the children of the current element");
            foreach (var child in accessibleNode.GetChildren())
            {
                AccessibleNode resultNode = searchPopup(child, handle, Java);
                if (resultNode != null)
                {
                    Log.InfoDebugTrace("resultNode != null . Returning resultNode");
                    return resultNode;
                }
            }
            return null;
        }
  
        
        
        public static string getScrollBarClickCoordinates()
        {
            try
            {
                   AccessBridge Java = new AccessBridge();
                   IntPtr handle = new IntPtr(0);
                    List<IntPtr> windowHandles = new List<IntPtr>();
            Java.Initialize(false);
            Application.DoEvents();
            //Get the Oracle EBS application process from the running processes in the system using the process name "jp2launcher" .
            Log.InfoDebugTrace("Trying to get the Oracle EBS application process from the running processes in the system using the process name jp2launcher");

            foreach (Process window in Process.GetProcesses())
            {
                window.Refresh();
                try
                {
                    if (window.HasExited == false)
                    {
                        Console.WriteLine(window.ProcessName);
                        if (window.ProcessName.Contains("jp2launcher"))
                        {
                            Log.InfoDebugTrace("Identified the Oracle EBS application process");
                            handle = window.MainWindowHandle;
                            Log.InfoDebugTrace("Got the Oracle EBS application process handle");
                            break;
                        }
                    }
                }
                catch (Exception ex)
                {
                    Log.Error("From process search catch" + ex.Message);
                    continue;
                }
            }
                //Get the Oracle application window using the process handle.
                Java.Functions.GetAccessibleContextFromHWND(handle, out int vmid, out JavaObjectHandle javaObjectHandle);
                AccessibleWindow win = Java.CreateAccessibleWindow(handle);
                //Traverse through the elements in the oracle application to get the scroll bar control/element
                var rootpane = win.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectRootPane = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectHandle, rootpane.GetIndexInParent());
                var layeredPanel1 = rootpane.GetChildren().ToArray()[1];
                JavaObjectHandle javaObjectLayeredPane1 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectRootPane, layeredPanel1.GetIndexInParent());
                var panel1 = layeredPanel1.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectPanel1 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectLayeredPane1, panel1.GetIndexInParent());
                var frame1 = panel1.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectFrame1 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectPanel1, frame1.GetIndexInParent());
                var panel2 = frame1.GetChildren().ToArray()[1];
                JavaObjectHandle javaObjectPanel2 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectFrame1, panel2.GetIndexInParent());
                var panel3 = panel2.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectPanel3 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectPanel2, panel3.GetIndexInParent());
                var scrollPane1 = panel3.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectscrollPane1 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectPanel3, scrollPane1.GetIndexInParent());
                var viewPort1 = scrollPane1.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectviewPort1 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectscrollPane1, viewPort1.GetIndexInParent());
                var desktopPane1 = viewPort1.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectdesktopPane1 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectviewPort1, desktopPane1.GetIndexInParent());
                var internalPane = desktopPane1.GetChildren().ToArray()[24];
                JavaObjectHandle javaObjectInternalPane = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectdesktopPane1, internalPane.GetIndexInParent());
                var panel4 = internalPane.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectpanel4 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectInternalPane, panel4.GetIndexInParent());
                var scrollpane2 = panel4.GetChildren().ToArray()[2];
                JavaObjectHandle javaObjectscrollpane2 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectpanel4, scrollpane2.GetIndexInParent());
                var viewport2 = scrollpane2.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectviewport2 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectscrollpane2, viewport2.GetIndexInParent());
                var panel5 = viewport2.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectpanel5 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectviewport2, panel5.GetIndexInParent());
                var scrollpane3 = panel5.GetChildren().ToArray()[0];
                JavaObjectHandle javaObjectscrollpane3 = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectpanel5, scrollpane3.GetIndexInParent());
                var scrollbar = scrollpane3.GetChildren().ToArray()[1];
                JavaObjectHandle javaObjectscrollbar = Java.Functions.GetAccessibleChildFromContext(vmid, javaObjectscrollpane3, scrollbar.GetIndexInParent());

                //Get the scrollbar element's properties
                PropertyList list = scrollbar.GetProperties(PropertyOptions.AccessibleContextInfo);
                String ScrollBar_propertiesStr = list[7].Value.ToString();
                //Get the X,Y,Height,Width of the scrollbar from properties
                ScrollBar_propertiesStr = ScrollBar_propertiesStr.Trim('{');
                ScrollBar_propertiesStr = ScrollBar_propertiesStr.Trim('}');
                String[] splitedProp = ScrollBar_propertiesStr.Split(',');
               // return ScrollBar_propertiesStr;
                String ScrollBarX = splitedProp[0].Split('=')[1];
                String ScrollBarY = splitedProp[1].Split('=')[1];
                String ScrollBarWidth = splitedProp[2].Split('=')[1];
                String ScrollBarHeight = splitedProp[3].Split('=')[1];
                //Apply the logic to get the position of the scrollbar at the right side (not the extreem right) 
                Double ClickPositionX_ = (Double.Parse(ScrollBarX) + Double.Parse(ScrollBarWidth)) - 50;
                Double ClickPositionY_ = Math.Round(Double.Parse(ScrollBarY) + (Double.Parse(ScrollBarHeight)/2));

                //Get the application handle & the scrollbar again in case of X & Y co-ordinates are negative values.
                if (ClickPositionX_ < 0 || ClickPositionY_ < 0)
                {
                    Log.DebugTrace("Getting negative co-ordinates values.Iteration : " + counter);
                    counter++;
                    //Throw error if getting negative values even after 5 times 
                    if (counter > 5)
                    {
                        Log.InfoDebugTrace("Getting negative co-ordinates values even after 5 times");
                        Log.Error("Error: Unable to retrieve Scrollbar co-ordinates");
                        return "Error: Unable to retrieve Scrollbar co-ordinates";
                    }
                    Log.DebugTrace("Calling  getScrollBarClickCoordinates function again");
                    return getScrollBarClickCoordinates();
                }
                else
                {
                    //return the mouse lick co-odrinates 
                   
                    String ClickPositionX = ClickPositionX_.ToString();
                    String ClickPositionY = ClickPositionY_.ToString();
                    Log.InfoDebugTrace("Returning the mouse lick co-odrinates. ClickPositionX : " + ClickPositionX + " ClickPositionY : " + ClickPositionY);
                    return "" + ClickPositionX + "," + ClickPositionY;
                }
                
            }
            catch (Exception ex)
            {
                Log.Error("Final catch" + ex.Message);
                return ex.Message;
            }
        }

        public static string getPopUpDetails(Boolean returnCoordinates)
        {
            try
            {
                Log.InfoDebugTrace("Inside getPopUpDetails function,returnCoordinates value  "+ returnCoordinates.ToString());
                AccessibleNode popUpElement = GetPopUp();
               
                if (popUpElement != null)
                {
                    Log.InfoDebugTrace("Got popUpElement " + popUpElement.ToString());
                    PropertyList list = popUpElement.GetProperties(PropertyOptions.AccessibleContextInfo);
                    Log.InfoDebugTrace("PropertyList of the element " + list.ToString() );
                    String popUp_propertiesStr = list[7].Value.ToString();
                    if (returnCoordinates)
                    {
                        popUp_propertiesStr = popUp_propertiesStr.Replace("{", "");
                        popUp_propertiesStr = popUp_propertiesStr.Replace("}", ",");
                        Log.InfoDebugTrace("returning  "+ popUp_propertiesStr+ " PopUpMessage :"+ list[0].Value.ToString());
                        return popUp_propertiesStr + "PopUpMessage=" + list[0].Value.ToString();
                    }
                    else
                    {
                        Log.InfoDebugTrace("Returning  " + list[0].Value.ToString());
                        return list[0].Value.ToString();
                    }
                }
                else
                {
                    Log.InfoDebugTrace("Returning  No Pop up found");
                    return "No Pop up found";
                }
             
            }
            catch (Exception ex)
            {
                Log.Error("Final catch" + ex.Message);
                return ex.Message;
            }
        }



    }
}

# A WLM solution that ensures 100% device utilization and Process the WorkItems from different Queues based on the Process Priority & WorkItem Priority


A WLM solution that ensures 100% device utilization and Process the WorkItems from different Queues based on the Process Priority & WorkItem PriorityEdit Title

## Description
* Let's assume you have 3 Queues in your WLM setup for different processes.
    * InvoiceQueue
    * PurchaseOrderQueue
    * PayrollQueue

* You have assigned a device pool invoice to the InvoiceQueue with 1 device, a Purchase Order device pool with 2 devices to the PurchaseOrderQueue, and a Payroll device pool with 1 device to the PayrollQueue. This allocation defines the device distribution for each process (Invoice, PO, and Payroll), which means the Process Priority. Purchase Order has high Process Priority, so allocated2 devices for PurchaseOrderQueue.  As a result, even if there are 5 work items in the InvoicePool, only 1 device will be allocated to process them.


* In this scenario, assume that 5 invoice work items and 1 payroll work item are in the feeder queues, with no Purchase Order work items in the PurchaseOrderQueue. In total, there are 2 + 1 + 1 = 4 devices available, but only 1 device is assigned to the InvoiceQueue and PayrollQueue. Therefore, the InvoiceQueue and PayrollQueue each pick 1 work item from the list of NEW work items and deploy it on the allocated devices. Meanwhile, the 2 devices assigned to the PurchaseOrderQueue remain idle since there are no work items in the queue.


* How can we fully utilize all the available devices in this situation? How can unprocessed invoice work items utilize the PO devices? Additionally, how can work items in each queue be selected based on priority? For example, if 10 items are accumulated in the InvoiceQueue at different times, the highest-priority work item should be selected for deployment, rather than being processed based on the order of insertion into the queue.
 

* Don’t worry, we have a solution to address all of these questions. Let’s explore the details.

##### STEP 1: 
First, you need to PAUSE the automation for all the existing queues. To do this, click on the three dots on the right side of each queue, go to the Automation section, and select PAUSE. For the sake of explanation, we'll refer to these paused queues as FeederQueues. Next, create a new queue, which will be our Active Queue moving forward. The work item structure of the Active Queue will differ from that of each FeederQueue. Here’s the work item structure for the Active Queue.Additionally, attach a new device pool to the ActiveQueue and include all the devices from the device pools attached to the FeederQueues in this new pool. In our example, the ActiveQueue's device pool will contain a total of 4 devices.

![image](https://github.com/user-attachments/assets/6c7ea92c-aa5a-4824-86ca-ff42dd0b82bc)


![image](https://github.com/user-attachments/assets/7a48d004-c658-4afe-aa69-c0352b855ccf)


#### STEP 2: 
* We need to set up a cron job that invokes a Python script. This script will retrieve unprocessed work items from the FeederQueues and add them to the ActiveQueue, taking into account the device allocation and work item priority of each FeederQueue.

* When the cron job runs at specified intervals (you can configure it to match the shortest ProcessCycleTime from the list of processes. For example, if the InvoiceProcess has a ProcessCycleTime of 30 minutes, the PurchaseOrderProcess has 60 minutes, and the PayrollProcess has 45 minutes, the cron job can be set to run every 30 minutes, as it is the shortest ProcessCycleTime among them. ), it will pick work items from the FeederQueues and insert them into the ActiveQueue. The ActiveQueue will have an associated bot running, and within that bot, we will dynamically call the corresponding FeederQueue bot as a child bot, passing the BotPath. This way, the bot associated with the ActiveQueue automation will execute the FeederQueue bot based on the device allocation and available devices.



* The work items will be picked from the FeederQueue based on the value in the WorkitemPriority column. Work items with a priority value of 1 will be picked by the logic before those with a value of 2. So, the cron job's Python script will sort the items at the queue level each time it picks them.

![image](https://github.com/user-attachments/assets/a796b8cb-aacd-4fd4-8999-105d6890ebbf)



 



## Authors

Contributors names and contact info

ex. Sikha Poyyil 

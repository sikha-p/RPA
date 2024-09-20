# Triggering an API without waiting for the response

The Code in this repo is to trigger an API and not wait for the response. In certain cases there is a need to just trigger the service and the backend takes too long to return the response, and in a scenario where we just want to trigger it and continue with our process, this SDK helps in doing so.


#### To add the built jar from this repo directly to your control room

* Download the jar from this project to your local.

* To add it to your control room, open your control room , in the manage sections click on packages and click on add package.

* Select the jar that you've just downloaded , click on accept and enable.

* Create a new bot and in the action section, you'll find your package there.

#### How to use the package

* Drag and drop the package.

* Enter the parameters

* <img width="686" alt="image" src="https://github.com/user-attachments/assets/7e81fa88-3717-47e2-b594-11b5e05d0019">

* The different types of content for the body is shown in the below picture.
* ![image](https://github.com/user-attachments/assets/0048788d-4ccb-4f41-a3ac-83b1ac07d198)

* Add the readTimeOut, connectionTimeOut and the payload, the datatype for payload is string, it can also be added in the form of string variable
* ![image](https://github.com/user-attachments/assets/7337dd79-70bf-4945-8d75-1454179a96a7)


//*********************************************//
//* Author : Sikha Poyyil
//*          Global Solution Desk
//*          Automation Anywhere
//********************************************//

function afterWindowLoaded() {
    console.log('DOMContentLoaded')
    window.addEventListener('hashchange', function () {
        console.log('hashchange event triggered')

        setTimeout(() => {

        const IneligibleAmountEle = document.querySelector("#elem-TextBox2 > div > input");
        const TotalAmountEle = document.querySelector("#elem-TextBox0 > div > input");
        const ApprovedAmountEle = document.querySelector("#elem-TextBox1 > div > input");

        // Ensure both text fields exist on the page
        if (IneligibleAmountEle) {
            IneligibleAmountEle.addEventListener('input', function () {
                //calculate Approved Amount 
                const ApprovedAmount = parseInt(TotalAmountEle.value) - parseInt(IneligibleAmountEle.value);
                ApprovedAmountEle.value = ApprovedAmount.toString();
                //bubble up the ApprovedAmountEle value change
                const event = new Event('input', {
                    bubbles: true,
                    cancelable: true,
                });
                ApprovedAmountEle.dispatchEvent(event);

            });
        }

         }, 1000);
    })


}

if (document.readyState !== 'complete') {
    console.log("document.readyState NOT COMPLETED");
    window.addEventListener('DOMContentLoaded', afterWindowLoaded);
} else {
    afterWindowLoaded();
}





(function () {
    const downloadFilename = advanceForm => {
        const today = new Date();
        const year = today.getFullYear();
        const month = ("0" + String(today.getMonth() + 1).slice(-2));
        const day = ("0" + today.getDate()).slice(-2);
        return year + month + day + " Advance - " + advanceForm.travel_city;
    };

    const dateFromString = dateString => {
        const dateParts = dateString.split('-');
        const year = dateParts[0];
        const month = parseInt(dateParts[1], 10) - 1;
        const day = dateParts[2];
        return new Date(year, month, day);
    };

    const dateDiff = (first, second) => Math.round((second-first)/(1000*60*60*24)); // Round to "handle" DST 
    
    const changeMdlTextField = (formElement, val) => formElement.parentElement.MaterialTextfield.change(val);

    document.addEventListener("DOMContentLoaded", () => {
        const submitButton = document.querySelector("#submit_expenses");
        
        submitButton.addEventListener('mdl-componentupgraded', () => {   
            const depDateField = document.querySelector("#dep_date");
            const retDateField = document.querySelector("#ret_date");
            const bfastField = document.querySelector('#num_breakfasts');
            const lunchField = document.querySelector('#num_lunches');
            const dinnerField = document.querySelector('#num_dinners');
            const hotelNightsField = document.querySelector('#hotel_nights');

            const dateChangeHandler = () => {
                if ((depDateField.value == "") || (retDateField.value == ""))
                    return;

                const depDate = dateFromString(depDateField.value);
                const retDate = dateFromString(retDateField.value);
                const tripDuration = dateDiff(depDate, retDate);

                if (tripDuration !== tripDuration) // Check for NaN, which happens if either value is invalid
                    return;
                    
                if (tripDuration < 0)
                    return;

                changeMdlTextField(hotelNightsField, tripDuration);
                changeMdlTextField(bfastField, tripDuration + 1);
                changeMdlTextField(lunchField, tripDuration + 1);
                changeMdlTextField(dinnerField, tripDuration + 1);                
            }

            submitButton.setAttribute('type', 'button');
            depDateField.addEventListener('change', dateChangeHandler);
            retDateField.addEventListener('change', dateChangeHandler);

            submitButton.addEventListener('click', () => {
                const formElements = document.querySelectorAll('#advance-form input[type=text]');
                const data = {}; 
                let errorFlag = false;
                
                for (element of formElements) {
                    if (element.value == "") {
                        alert("Error! All fields must have a value.");
                        errorFlag = true;
                        break; 
                    }
                    data[element.id] = element.value;
                }

                data["email_me"] = document.querySelector('input[name="email_me"]:checked').value;

                if (!errorFlag) {
                    console.log("JSON submitted => " + JSON.stringify(data));
                    submitButton.setAttribute('disabled', 1);

                    const request = new XMLHttpRequest();
                    request.open("POST", "/api/advance_form", true);
                    request.setRequestHeader("Content-Type", "application/json");
                    request.responseType = "blob";

                    request.addEventListener('load', event => {
                        if (request.status == 200) {
                            const blob = request.response;
                            const link = document.createElement('a');
                            link.href = window.URL.createObjectURL(blob);
                            link.download = downloadFilename(data) + ".docx";
                            link.click();
                            alert('Thanks! Please submit the file that you just downloaded.')
                            window.location.reload(true);
                        } else {
                            alert('Something went wront on the server (' + 
                                request.status + ') - check your input and try again.');
                            submitButton.setAttribute('disabled', 0);    
                        }
                    });
                    request.send(JSON.stringify(data));
                }
            });
        });
    });
})();
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
    
    const changeMdlTextField = (jqObject, val) => jqObject.get(0).parentElement.MaterialTextfield.change(val);

    $(document).ready(() => {
        const submitButton = $("#submit_expenses");
        
        submitButton.on('mdl-componentupgraded', () => {    
            const depDateField = $("#dep_date");
            const retDateField = $("#ret_date");
            const bfastField = $('#num_breakfasts');
            const lunchField = $('#num_lunches');
            const dinnerField = $('#num_dinners');
            const hotelNightsField = $('#hotel_nights');

            const dateChangeHandler = () => {
                if ((depDateField.val() == "") || (retDateField.val() == ""))
                    return;

                const depDate = dateFromString(depDateField.val());
                const retDate = dateFromString(retDateField.val());
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

            depDateField.change(dateChangeHandler);
            retDateField.change(dateChangeHandler);

            submitButton.click(() => {
                const formElements =$("#advance-form input[type=text]");
                let data = {}; // FIXME to const
                let errorFlag = false;
                
                for (element of formElements) {
                    if (element.value == "") {
                        alert("Error! All fields must have a value.");
                        errorFlag = true;
                        break;
                    }
                    data[element.id] = element.value;
                }

                if (!errorFlag) {
                    console.log("JSON submitted => " + JSON.stringify(data));
                    submitButton.prop('disabled', 1);

                    // let fakeData = {
                    //     "full_name":"James McNeil",
                    //     "phone_num":"613.888.9999",
                    //     "dep_date":"2017-04-01",
                    //     "ret_date":"2017-05-02",
                    //     "trip_purpose":"Advance PM's visit to Barrie",
                    //     "travel_city":"Toronto",
                    //     "num_breakfasts":"3",
                    //     "num_lunches":"3",
                    //     "num_dinners":"2",
                    //     "num_incidentals":"1",
                    //     "hotel_cost":"150",
                    //     "hotel_nights":"2",
                    //     "rental_amount":"160.99",
                    //     "transport_amount":"60"
                    // } 
                    // data = fakeData; // FIXME

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
                            submitButton.prop('disabled', 0);    
                        }
                    });

                    request.send(JSON.stringify(data));
                }
            });
        });
    });
})();
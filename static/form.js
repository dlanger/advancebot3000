(function () {
    const downloadFilename = (advanceForm) => {
        const today = new Date();
        const year = today.getFullYear();
        const month = ("0" + String(today.getMonth() + 1).slice(-2));
        const day = ("0" + today.getDate()).slice(-2);

        return year + month + day + " Advance - " + advanceForm.travel_city;
    };

    $(document).ready(() => {
        $('#submit-expenses').on('mdl-componentupgraded', () => {
            const submitButton = $("#submit-expenses");

            $("#submit-expenses").click(() => {
                const formElements =$("#advance-form input[type=text]");
                let data = {}; // FIXME to const
                let errorFlag = false;
                
                for (element of formElements) {
                    if (element.value == "") {
                        // alert("Error! All fields must have a value.");
                        // errorFlag = true;
                        // break;
                        // FIXME
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
                    // } // FIXME

                    // data = fakeData; // FIXME

                    const request = new XMLHttpRequest();
                    request.open("POST", "/api/advance_form", true);
                    request.setRequestHeader("Content-Type", "application/json");
                    request.responseType = "blob";

                    request.addEventListener('load', (event) => {
                        if (request.status == 200) {
                            const blob = request.response;
                            const link = document.createElement('a');
                            link.href = window.URL.createObjectURL(blob);
                            link.download = downloadFilename(data) + ".docx";
                            link.click();
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
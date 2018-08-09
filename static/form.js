(function () {
    $(document).ready(() => {
        $('#submit-expenses').on('mdl-componentupgraded', () => {
            $("#submit-expenses").click(() => {
                const formElements =$("#advance-form input[type=text]");
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

                if (!errorFlag) {
                    alert(JSON.stringify(data));
                    $("#submit-expenses").prop('disabled',1);
                }
            });
        });
    });
})();
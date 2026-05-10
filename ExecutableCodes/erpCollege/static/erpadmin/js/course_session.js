document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("courseSessionForm");

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        const formData = new FormData(form);

        fetch("/erpadmin/save-course-session/", {

            method: "POST",

            body: formData

        })
        .then(response => response.json())
        .then(data => {

            if(data.complete_name){

                const sessionData = document.getElementById("sessionData");

                sessionData.innerHTML =
                `
                    <div class="session-item">
                        ${data.complete_name}
                    </div>
                ` + sessionData.innerHTML;

                form.reset();
            }

        });

    });

});
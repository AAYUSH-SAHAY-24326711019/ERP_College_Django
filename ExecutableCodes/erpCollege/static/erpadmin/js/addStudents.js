$(function () {

    // ==========================
    // CSRF
    // ==========================
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // ==========================
    // AJAX WRAPPER (IMPORTANT)
    // ==========================
    function ajaxRequest(options) {
        return $.ajax({
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            contentType: "application/json",
            dataType: "json",
            ...options
        });
    }

    // ==========================
    // STUDENT PREVIEW (LIVE)
    // ==========================
    $("#student_ids").on("keyup", function () {

        let studentIds = $(this).val().trim();

        $(".student-preview-wrapper").remove();

        if (!studentIds) return;

        ajaxRequest({
            url: "/erpadmin/get-students-preview/",
            method: "POST",
            data: JSON.stringify({ student_ids: studentIds }),

            success: function (res) {

                let rows = "";

                if (res.students?.length) {
                    res.students.forEach(s => {
                        rows += `
                            <tr>
                                <td>${s.student_id}</td>
                                <td>${s.name}</td>
                            </tr>
                        `;
                    });
                } else {
                    rows = `<tr><td colspan="2">No Students Found</td></tr>`;
                }

                const html = `
                    <div class="student-preview-wrapper">
                        <table class="preview-table">
                            <thead>
                                <tr>
                                    <th>Student ID</th>
                                    <th>Name</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                `;

                $("#addStudentsForm").after(html);
            }
        });
    });

    // ==========================
    // ADD STUDENTS
    // ==========================
    $("#addStudentsForm").on("submit", function (e) {

        e.preventDefault();

        ajaxRequest({
            url: "/erpadmin/add-students-to-course/",
            method: "POST",
            data: JSON.stringify({
                student_ids: $("#student_ids").val(),
                course_id: $("#course_id").val()
            }),

            success: function (res) {

                alert(res.message);

                loadCourseStudents($("#course_id").val());

                $("#student_ids").val("");
                $(".student-preview-wrapper").remove();
            }
        });
    });

    // ==========================
    // TAB CLICK (DELEGATED)
    // ==========================
    $(document).on("click", ".course-tab", function () {

        $(".course-tab").removeClass("active");
        $(this).addClass("active");

        loadCourseStudents($(this).data("course"));
    });

    // ==========================
    // LOAD STUDENTS
    // ==========================
    function loadCourseStudents(courseId) {

        ajaxRequest({
            url: `/erpadmin/course-students/${courseId}/`,
            method: "GET",

            success: function (res) {

                let rows = "";

                if (res.students?.length) {
                    res.students.forEach(s => {
                        rows += `
                            <tr>
                                <td>${s.id}</td>
                                <td>${s.student_id}</td>
                                <td>${s.name}</td>
                                <td>${s.email}</td>
                                <td>${s.date_created}</td>
                            </tr>
                        `;
                    });
                } else {
                    rows = `<tr><td colspan="5">No Students Added</td></tr>`;
                }

                $("#courseStudentsContainer").html(`
                    <div class="students-table-wrapper">
                        <table class="students-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Student ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Added On</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                `);
            }
        });
    }

    // ==========================
    // AUTO LOAD FIRST TAB
    // ==========================
    const first = $(".course-tab.active").data("course");

    if (first) {
        loadCourseStudents(first);
    }

});
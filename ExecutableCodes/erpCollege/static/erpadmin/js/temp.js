// addStudents.js

$(document).ready(function () {

    // ==========================
    // CSRF TOKEN
    // ==========================

    function getCSRFToken() {

        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        ).value;

    }


    // ==========================
    // LIVE STUDENT FETCH
    // ==========================

    $("#student_ids").on("keyup", function () {

        let studentIds = $(this).val().trim();

        // remove old preview
        $(".student-preview-wrapper").remove();

        if (studentIds.length === 0) {
            return;
        }

        $.ajax({

            url: "/erpadmin/get-students-preview/",

            method: "POST",

            headers: {
                "X-CSRFToken": getCSRFToken()
            },

            data: JSON.stringify({
                student_ids: studentIds
            }),

            contentType: "application/json",

            success: function (response) {

                let html = `
                    <div class="student-preview-wrapper">
                        <table class="preview-table">
                            <thead>
                                <tr>
                                    <th>Student ID</th>
                                    <th>Name</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                if (response.students.length > 0) {

                    response.students.forEach(student => {

                        html += `
                            <tr>
                                <td>${student.student_id}</td>
                                <td>${student.name}</td>
                            </tr>
                        `;

                    });

                } else {

                    html += `
                        <tr>
                            <td colspan="2">
                                No Students Found
                            </td>
                        </tr>
                    `;

                }

                html += `
                            </tbody>
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

    $("#addStudentsForm").submit(function (e) {

        e.preventDefault();

        let student_ids = $("#student_ids").val();

        let course_id = $("#course_id").val();

        $.ajax({

            url: "/erpadmin/add-students-to-course/",

            method: "POST",

            headers: {
                "X-CSRFToken": getCSRFToken()
            },

            data: JSON.stringify({

                student_ids: student_ids,
                course_id: course_id

            }),

            contentType: "application/json",

            success: function (response) {

                alert(response.message);

                loadCourseStudents(course_id);

                $("#student_ids").val("");

                $(".student-preview-wrapper").remove();

            }

        });

    });


    // ==========================
    // COURSE TAB CLICK
    // ==========================

    // $(".course-tab").click(function () {

    //     $(".course-tab").removeClass("active");

    //     $(this).addClass("active");

    //     let courseId = $(this).data("course");

    //     loadCourseStudents(courseId);

    // });

$(document).on("click", ".course-tab", function () {

    $(".course-tab").removeClass("active");
    $(this).addClass("active");

    let courseId = $(this).data("course");

    loadCourseStudents(courseId);

});

    // ==========================
    // LOAD COURSE STUDENTS
    // ==========================

    function loadCourseStudents(courseId) {

        $.ajax({

            url: `/erpadmin/course-students/${courseId}/`,

            method: "GET",

            success: function (response) {

                let html = `
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

                            <tbody>
                `;

                if (response.students.length > 0) {

                    response.students.forEach(student => {

                        html += `
                            <tr>
                                <td>${student.id}</td>
                                <td>${student.student_id}</td>
                                <td>${student.name}</td>
                                <td>${student.email}</td>
                                <td>${student.date_created}</td>
                            </tr>
                        `;

                    });

                } else {

                    html += `
                        <tr>
                            <td colspan="5">
                                No Students Added
                            </td>
                        </tr>
                    `;

                }

                html += `
                            </tbody>

                        </table>

                    </div>
                `;

                $("#courseStudentsContainer").html(html);

            }

        });

    }


    // ==========================
    // AUTO LOAD FIRST TAB
    // ==========================

    let firstCourse = $(".course-tab.active").data("course");

    if (firstCourse) {

        loadCourseStudents(firstCourse);

    }

});
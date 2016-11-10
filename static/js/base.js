$(document).ready(function () {
            $(".content-markdown").each(function () {
                var content = $(this).text().trim()
                var markedContent = marked(content)
                $(this).html(markedContent)
            })

            //preview-title
            var titleInput = $("#id_title");


            function setTitle(value) {
                $("#preview-title").text(value)
            }

            setTitle(titleInput.val())

            titleInput.keyup(function () {
                var newTitle = titleInput.val()
                setTitle(newTitle)
            })
            //preview-content
            var contentInput = $("#id_content");

            function setContent(value) {
                var markedContent = marked(value)
                $("#preview-content").html(markedContent)
                $("#preview-content img").each(function () {
                    $(this).addClass("img-responsive")
                })
            }
            setContent(contentInput.val())

            contentInput.keyup(function () {
                var newContent = $(this).val()
                setContent(newContent)
            })
            $(".commit-reply-btn").click(function (event) {
                event.preventDefault();
                $(this).parent().next(".comment-replay").fadeToggle();
            })

        }
)
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
$('.radio_search').each(function (e) {
        $('.radio_search').each(function (e) {
        $(this).children('label').click(function (e) {
            $('#search_type_button').text($(this).text() + ' ');
        })
    })
})

$('#search_type_button').text($('input[name=search_radio]:checked', '.radio_search').parent().text() + ' ');

$(".alert").delay(2000).slideUp(200, function() {
    $(this).alert('close');
});


// deep search button click on/off
$('.no-checkedselector').on('change', 'input[type="radio"].toggle', function () {
    if (this.checked) {
        $('input[name="' + this.name + '"].checked').removeClass('checked');
        $(this).addClass('checked');
        $('.toggle-container').addClass('force-update').removeClass('force-update');
    }
});
$('.no-checkedselector input[type="radio"].toggle:checked').addClass('checked');

function deepSearchClickLink(element) {
    console.log("DUPQA!!!!!!!!");
    console.log(element);
    $(element).attr('href', function() {
        if ($('#toggle-on').is(':checked')) {
            return this.href + '?deep_search=on';
        } else {
            return this.href;
        }
    });

}
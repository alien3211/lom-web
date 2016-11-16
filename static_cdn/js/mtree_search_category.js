/**
 * Created by alan on 14.11.16.
 */
$(document).ready(function () {

    function expend_collapse_mtree_search_category() {
        if ($(".menufilter").val() == '') {
            $(".fordtreeview span").each(function(e){
                $(this).removeClass('fordtreeview-found');
            });
            $('.mtree li').each(function() {
              $(this).removeClass('mtree-open').addClass('mtree-closed');
            });
            $('.mtree ul').each(function() {
              $(this).css({'overflow': 'hidden', 'height': '0px', 'display': 'none'});
        });

        } else {
            $('.mtree li').each(function() {
              $(this).removeClass('mtree-closed').addClass('mtree-open');
            });
            $('.mtree ul').each(function() {
              $(this).css({'height': 'auto', 'display': 'block'});
            });
        }
    }



	$('.hasSub').click(function () {
    $(this).parent().toggleClass('subactivated');
		$(this).parent().children('ul:first').toggle();

	});

  $(".menufilter").keyup(function () {
    /*expend and collapse mtree search category menu*/
    expend_collapse_mtree_search_category();

    var searchTerm = $(".menufilter").val();
    var listItem = $('.fordtreeview').children('li');

    var searchSplit = searchTerm.replace(/ /g, "'):containsi('")

      //extends :contains to be case insensitive
  $.extend($.expr[':'], {
  'containsi': function(elem, i, match, array)
  {
    return (elem.textContent || elem.innerText || '').toLowerCase()
    .indexOf((match[3] || "").toLowerCase()) >= 0;
  }
});

    $(".fordtreeview span").not(":containsi('" + searchSplit + "')").each(function(e){
        $(this).removeClass('fordtreeview-found');
    });

    if (searchSplit != '') {
        $(".fordtreeview span:containsi('" + searchSplit + "')").each(function(e){
            $(this).addClass('fordtreeview-found');
        });
    }

    $(".fordtreeview li").not(":containsi('" + searchSplit + "')").each(function(e)   {
      $(this).hide()
    });

    $(".fordtreeview li:containsi('" + searchSplit + "')").each(function(e) {
      $(this).show();
    });


  });
});
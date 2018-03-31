$(document).ready(function() {

    // Toggle deal description in list view
    $('a.toggle-description').click(function() {

        var deal_id = $(this).data("deal-id");

        $('#deal' + deal_id + ' .description').toggle();
        $(this).siblings('.fa').toggleClass('fa-plus-square fa-minus-square');

        return false;
    });

    // Append/toggle comment reply form
    $('a.comment-reply').click(function() {

        var comment_id = $(this).data("comment-id");
        var replyform = $('#comment' + comment_id + ' .reply-form');

        if (replyform.length) {
            replyform.toggle();
        } else {
            $(this).closest('ul').after(
                '<div class="reply-form">' +
                '  <form>' +
                '    <input type="hidden" name="parent" value="' + comment_id + '">' +
                '    <textarea name="reply"></textarea><br />' +
                '    <input type="submit" value="Save" class="btn btn-sm btn-primary" />' +
                '  </form>' +
                '</div>'
            );
        }

        return false;
    });

    // Vote on a deal/comment
    $('a.upvote, a.downvote').click(function() {

        var link = $(this);
        var parent_id = '#' + link.data('object') + link.data('object-id');

        $.post(
            this.href,
            {csrfmiddlewaretoken: crsftoken},
            function(data) {
                $(parent_id + ' .vote-toggle a').removeClass('voted');
                $(parent_id + ' .upvote').attr('href', data.upvote);
                $(parent_id + ' .downvote').attr('href', data.downvote);
                $(parent_id + ' .score').html(data.score);
                if (data.voted) {
                    link.addClass('voted');
                }
            }
        );

        return false;
    });

});

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

    // Vote on a deal
    $('a.upvote, a.downvote').click(function() {

        var link = $(this);
        var deal_id = link.data('deal-id');

        $.post(
            this.href,
            {csrfmiddlewaretoken: crsftoken},
            function(data) {
                // Delete a vote
                if (link.hasClass('voted')) {
                    if (link.hasClass('upvote')) {
                        link.attr('href', '/deals/' + deal_id + '/vote/up/');
                    } else {
                        link.attr('href', '/deals/' + deal_id + '/vote/down/');
                    }
                    $('#deal' + deal_id + ' a.voted').removeClass('voted');
                // Upvote/downvote
                } else {
                    if (link.hasClass('upvote')) {
                        $('#downvote' + deal_id).attr('href', '/deals/' + deal_id + '/vote/down/');
                    } else {
                        $('#upvote' + deal_id).attr('href', '/deals/' + deal_id + '/vote/up/');
                    }
                    link.attr('href', '/deals/' + deal_id + '/vote/delete/');
                    $('#deal' + deal_id + ' a.voted').removeClass('voted');
                    link.addClass('voted');
                }
                $('#deal' + deal_id + ' .score').html(data.score);
            }
        );

        return false;
    });

});

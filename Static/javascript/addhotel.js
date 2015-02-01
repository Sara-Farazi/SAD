/**
 * Created by mac on 1/28/15.
 */
$(document).ready(function(){

    $('#submit-form').click(function () {
        data = $(this).parent().serialize();
//
//        alert(data);
//        console.log(data);
        var rate = $("#hotel-rate").rating('get rating');
        var input = $("<input name='rate'>").attr("type", "hidden").val(rate);
        $('form').append($(input));
        $('form').submit();
    });


});
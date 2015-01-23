/**
 * Created with PyCharm.
 * User: MrMo
 * Date: 12/8/13
 * Time: 4:11 PM
 * To change this template use File | Settings | File Templates.
 */
$('.ui.selection.dropdown').dropdown();
$('.bar').css({'width':'25%'});



$('#menu_signin').click(function(){
        $('#signin_modal')
            .modal('setting', 'transition', 'horizontal flip')
            .modal('toggle');    }
    );
$('#menu_search').click(function(){
        $('#sidebar_search')
            .sidebar('toggle');    }
    );
$('.close_sidebar').click(function(){
        $(this.parentNode)
            .sidebar('toggle');    }
    );
$('.send_message').click(function(){
        $('#sidebar_send_message'+this.value)
            .sidebar('toggle');    }
    );
$('#adv_search_btt').click(function(){
        $('#adv_search').toggle('slow');
    }
    );
$('.search_result_item').click(function(){
        $('#karjo_modal'+this.value)
            .modal('setting', 'transition', 'fade up')
            .modal('toggle')
        ;
    }
    );
$('.checkbox_en').click(function(){
        $(this.parentNode.parentNode)
            .checkbox('enable')
        ;
    }
    );
$('.checkbox_dis').click(function(){
        $(this.parentNode.parentNode)
            .checkbox('disable')
        ;
    }
    );

$('.ui.dropdown')
    .dropdown()
;

$('.ui.checkbox')
    .checkbox()
;
$('.ui.accordion')
    .accordion()
;
//$('.next_step_btt').click(
//    function(){
//
//        $.get('/action/register/karfarma/2/',
//            function(data){
//
//                $('#action_div').html(data);
//            }
//        );
//
//    }
//);
$('.secondary-filters').hide()
$('.primary-filters').hide()


$(".filters-toggle-primary").click(function() {
    $('.primary-filters').toggle()

    if($(".toggle-text-primary").hasClass('fa-angle-double-down')) {
        $(".toggle-text-primary").removeClass('fa-angle-double-down')
        $(".toggle-text-primary").addClass('fa-angle-double-up')
    }
    else {
            $(".toggle-text-primary").removeClass('fa-angle-double-up')
            $(".toggle-text-primary").addClass('fa-angle-double-down')
            $('.secondary-filters').hide()
            $(".toggle-text-secondary").removeClass('fa-angle-double-up')
            $(".toggle-text-secondary").addClass('fa-angle-double-down')
    }

})

$(".filters-toggle-secondary").click(function() {
    $('.secondary-filters').toggle()

    if($(".toggle-text-secondary").hasClass('fa-angle-double-down')) {
        $(".toggle-text-secondary").removeClass('fa-angle-double-down')
        $(".toggle-text-secondary").addClass('fa-angle-double-up')
    }
    else {
            $(".toggle-text-secondary").removeClass('fa-angle-double-up')
            $(".toggle-text-secondary").addClass('fa-angle-double-down')
    }

})

$('.hidden-image').hide()

$(".hidden-images-show").click(function() {
    $('.hidden-image').toggle()

    if($(".hidden-images-show").hasClass('fa-angle-double-down')) {
        $(".hidden-images-show").removeClass('fa-angle-double-down')
        $(".hidden-images-show").addClass('fa-angle-double-up')
    }
    else {
            $(".hidden-images-show").removeClass('fa-angle-double-up')
            $(".hidden-images-show").addClass('fa-angle-double-down')
    }
})

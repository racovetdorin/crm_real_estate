$("input[type='date']").on("change", function() {
    if(this.value){
        $(this).attr('data-date', moment(this.value, 'YYYY-MM-DD').format($(this).attr('data-date-format')));
    } 
    else{
        $(this).attr('data-date', 'dd/mm/yyyy');
    }
}).trigger("change")
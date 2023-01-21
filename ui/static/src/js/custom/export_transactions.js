$('#transactions-export').click( function(event) {
    var baseUrl,
        $filterForm,
        filterFormData,
        exportUrl;

    event.preventDefault();

    baseUrl = $(this).attr('href');

    filterFormData = new URLSearchParams(window.location.search)

    exportUrl = baseUrl + "?" + filterFormData;

    window.open(exportUrl);

});

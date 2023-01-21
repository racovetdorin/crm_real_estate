/**
* Theme: Hyper - Responsive Bootstrap 4 Admin Dashboard
* Author: Coderthemes
* Component: Dragula component
*/



!function ($) {
    "use strict";

    var Dragula = function () {
        this.$body = $("body")
    };


    /* Initializing */
    Dragula.prototype.init = function () {

        $('[data-plugin="dragula"]').each(function () {
            var containersIds = $(this).data("containers");
            var containers = [];
            if (containersIds) {
                for (var i = 0; i < containersIds.length; i++) {
                    containers.push($("#" + containersIds[i])[0]);
                }
            } else {
                containers = [$(this)[0]];
            }

            // if handle provided
            var handleClass = $(this).data("handleclass");

            // init dragula
            if (handleClass) {
                dragula(containers, {
                    moves: function (el, container, handle) {
                        return handle.classList.contains(handleClass);
                    }
                });
            } else {
                dragula(containers, {
                    moves: function (el, source, handle, sibling) {
                        if (el.classList.contains('no-drag')) {
                            return false;
                        } else {
                            return true;
                        }

                    }
                }).on('drop', function (element, container) {
                    var activityId = $(element).data('activity-id');
                    $.ajax({
                      type: "POST",
                      url: $(element).data('change-type-url'),
                      data: JSON.stringify({ status: $(container).data('status') }),
                      contentType:"application/json; charset=utf-8",
                      dataType: "json",
                      success:  $('#modal-select-' + String(activityId)).val($(container).data('status')).attr('selected','selected')
                    });
                });
            }

        });
    },

        //init dragula
        $.Dragula = new Dragula, $.Dragula.Constructor = Dragula

}(window.jQuery),

//initializing Dragula
function ($) {
"use strict";
    $.Dragula.init()
}(window.jQuery);

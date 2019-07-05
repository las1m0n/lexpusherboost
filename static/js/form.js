(function(){
    let _p = project;
    _p.setupValidator = function($f){
        var targetInputs = $f.find('input,textarea,select'),
            infoElement = $f.find('.validation_info');
        targetInputs.add($f).each(function(){
            var $i = $(this),
                hR = $i.attr('humanReadable');
            $i.data('showErrorMessage',function(msg){
                infoElement.append($('<p/>').html(hR+': '+msg));
            });
        });
        $f.on('submit', function(e, machineGenerated) {
            if(machineGenerated) return;
            infoElement.html('');
            e.preventDefault();
            var ser = targetInputs.serialize();
            ser += '&form=' + $f.attr('id');
            $.post('/ajaxValidation/', ser, function(info) {
                if (info != 'ok') {
                    var errors = $.parseJSON(info);
                    for (var i = 0; i < errors.length; i++) {
                        var input = $f.find(errors[i].key);
                        if($f.is(errors[i].key)){
                            input = $f;
                        }
                        if(input.data('showErrorMessage')){
                            input.data('showErrorMessage')(errors[i].desc);
                        } else {
                            console.log(input,errors[i].desc);
                        }
                    }
                } else {
                    $f.trigger('submit', [true]);
                }
            });
        });
    }

    $(function (){
        _p.setupValidator($('.'+_p.validateeFormClass));
    });
})();
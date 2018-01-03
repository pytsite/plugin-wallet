define(['assetman', 'widget-input-text', 'jquery-inputmask'], function (assetman) {
    assetman.loadCSS('plugins.wallet@css/widget-input-money.css');

    return function (widget) {
        widget.em.find('input[type=text],input[type=tel],input[type=number]').inputmask('decimal', {
            allowMinus: false
        });
    }
});

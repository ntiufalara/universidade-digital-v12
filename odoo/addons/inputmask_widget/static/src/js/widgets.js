odoo.define('web.inputmask_widgets', function (require) {
    var form_widgets = require('web.basic_fields');
    var fieldRegistry = require('web.field_registry');

    function mask_attrs(attrs) {
        var keyMask = 'data-inputmask';
        var attributes = {};
        if (keyMask in attrs)
            attributes[keyMask] = attrs[keyMask];
        else
            attributes = Object.keys(attrs).reduce(function (filtered, key) {
                if (key.indexOf(keyMask) !== -1)
                    filtered[key] = attrs[key];
                return filtered;
            }, {});
        if (!attributes)
            console.warn("The widget Mask expects the 'data-inputmask[-attribute]' attributes!")
        return attributes;
    }

    var FieldMask = form_widgets.FieldChar.extend({
        template: "inputmask_widget.FieldMask",
        attributes: {},
        init: function () {
            this._super.apply(this, arguments);
            this.attributes = mask_attrs(this.attrs);
        },
        _renderEdit: function (mask) {
            this._super.apply(this, arguments);
            console.log(this.attributes);
            if (this.attributes) {
                if (this.$input !== undefined)
                    this.$input.inputmask(mask);
                else if ('contenteditable' in this.attrs)
                    this.$el.inputmask(mask);
            }
        },
    });

    var FieldMaskRegex = FieldMask.extend({
        render_value: function () {
            this._super("Regex");
        }
    });

    fieldRegistry.add('mask', FieldMask);
    fieldRegistry.add('mask_regex', FieldMaskRegex);

    return {FieldMask: FieldMask, FieldMaskRegex: FieldMaskRegex};
});

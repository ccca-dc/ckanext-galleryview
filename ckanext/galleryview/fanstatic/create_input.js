"use strict";

ckan.module('create_input', function ($, _) {
    var next = 1;
    var field;
    var imagename;

  return {
    initialize: function () {
        $.proxyAll(this, /_on/);
        this.el.on('click', this._onClick);
        field = this.options.field;
        imagename = this.options.imagename;

        if(field !== "button"){
            this.createInput();
        }
    },

    _onClick: function(event) {
        field = "";
        imagename = "";
        this.createInput();
    },

    createInput: function () {
        next = next + 1;

        if(next == 2){
            $("#field").append($('<div id="br2"></br></div>'));
        }

        var newInput = $('<input autocomplete="off" class="input" id="field' + next + '" name="fields" type="text" placeholder="link eg. http://example.com/image.jpg" value="' + field + '">');
        var newInputImageName = $('<input autocomplete="off" class="input" id="image_name' + next + '" name="image_names" type="text" placeholder="name of the image" value="' + imagename + '"/>');
        var removeButton = $('<button id="remove-' + next + '" class="btn btn-danger remove-me" >-</button></div><div id="field">');

        $("#field").append(newInput);
        $(newInput).after(" ", newInputImageName);
        $(newInputImageName).after(" ", removeButton);

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.substr(this.id.indexOf("-") + 1);
                var fieldID = "#field" + fieldNum;
                var imageID = "#image_name" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
                $(imageID).remove();

                if(fieldNum == 2){
                    var br = "#br2";
                    $(br).remove();
                }

            });
    }
  };
});

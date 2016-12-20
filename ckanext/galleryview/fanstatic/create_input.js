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

        // when field or imagename was not filled out last time, it gets filled out with 'true' and therefore it is here set to '' again
        if(field == true){
            field = ""
        }
        if(imagename == true){
            imagename = ""
        }

        //this adds two input fields with the given text (when pictures previously saved) and one remove button
        var newInput = $('<input autocomplete="off" class="input form-control" id="field' + next + '" name="fields" type="text" placeholder="link eg. http://example.com/image.jpg" value="' + field + '"/>');
        var newInputImageName = $('<input autocomplete="off" class="input" id="image_name' + next + '" name="image_names" type="text" placeholder="name of the image" value="' + imagename + '"/>');
        var removeButton = $('<button id="remove-' + next + '" class="btn btn-danger remove-me" >-</button><div id="field"></div>');

        $("#field").append(newInput);
        $(newInput).after(" ", newInputImageName);
        $(newInputImageName).after(" ", removeButton);

            //when pressing the remove button it deletes both input fields and the button
            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.substr(this.id.indexOf("-") + 1);
                var fieldID = "#field" + fieldNum;
                var imageID = "#image_name" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
                $(imageID).remove();
            });
    }
  };
});

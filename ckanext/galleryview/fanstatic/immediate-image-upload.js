"use strict";
/* Image Upload
 *
 */
ckan.module('immediate-image-upload', function($, _) {
  var count = -1;
  return {
    /* options object can be extended using data-module-* attributes */
    options: {
      is_url: false,
      is_upload: false,
      field_upload: 'image_upload',
      field_url: 'image_url',
      field_clear: 'clear_upload',
      field_name: 'name',
      upload_label: '',
      data_dict: '',
      resource_id: '',
      type: '',
      image_name: '',
      i18n: {
        upload: _('Upload'),
        url: _('Link'),
        remove: _('Remove'),
        upload_label: _('Image'),
        label_for_url: _('URL'),
        label_for_upload: _('File'),
        upload_tooltip: _('Upload a file on your computer'),
        url_tooltip: _('Link to a URL on the internet (you can also link to an API)')
      }
    },

    /* Should be changed to true if user modifies resource's name
     *
     * @type {Boolean}
     */
    _nameIsDirty: false,

    /* Initialises the module setting up elements and event listeners.
     *
     * Returns nothing.
     */

    initialize: function () {
      $.proxyAll(this, /_on/);
      var options = this.options;
      this.data_dict = options.data_dict;
      var type = options.type;
      this.resource_id = options.resource_id;
      this.upload_label = options.upload_label;
      this.image_name = options.image_name;

      if(this.upload_label == true){
          this.upload_label = ""
      }
      if(this.image_name == true){
          this.image_name = ""
      }

      this.input = new Array();
      this.field_url = new Array();
      this.field_image = new Array();
      this.label_location = new Array();
      this.is_data_resource = new Array();
      this.field_clear = new Array();
      this.button_url = new Array();
      this.button_upload = new Array();
      this.field_name = new Array();
      this.field_url_input = new Array();
      this.fields = new Array();

      this.el.on('click', this._onClick);

      /* createInput should be called from div, when creating the div
      and from button, when it is clicked */
      if(type != "button"){
          this.createInput();
      }
    },

    _onClick: function(event) {
      this.upload_label = "";
      this.image_name = "";
      this.createInput();
    },

    createInput: function () {
        var options = this.options;
        count = count + 1;

        // inserting all fields that are inserted in the image_upload macro in form.html

        var sectionDiv = $('<div id="sectiondiv-' + count + '" class="image-upload">');

        var controlGroupUrl = $('<div class="control-group control-full"></div>');
        var controlsUrl = $('<div class="controls"></div>');
        var inputUrl = $('<input id="field-image-url' + count + '" name="image_url" value="' + this.upload_label + '" placeholder="http://example.com/my-image.jpg" type="text"/>')
        var controlLabelUrl = $('<label class="control-label" for="field-image-url">Image URL</label>');

        var controlGroupUpload = $('<div class="control-group control-full"></div>');
        var controlLabelUpload = $('<label class="control-label" for="field-image-upload">Image URL</label>');
        var controlsUpload = $('<div class="controls"></div>');
        var inputUpload = $('<input id="field-image-upload' + count + '" name="image_upload" value="" placeholder="" type="file"/>');

        var removeButton = $('<button id="remove-' + count + '" class="btn btn-danger remove-me remove">-</button><div id="field"></div>');

        var inputName = $('<input id="field-name' + count + '" name="image_names" value="' + this.image_name + '" placeholder="name of the image" type="text"/>')
        var controlLabelName = $('<label class="control-label" for="field-name">Image Name</label>');

        $("#masterdiv").append(sectionDiv);
        sectionDiv.append(controlGroupUrl);

        controlGroupUrl.append(controlLabelUrl);
        controlGroupUrl.append(controlsUrl);
        controlsUrl.append(inputUrl);

        sectionDiv.append(controlGroupUpload);

        controlGroupUpload.append(controlLabelUpload);
        controlGroupUpload.append(controlsUpload);
        controlsUpload.append(inputUpload);

        sectionDiv.append(controlLabelName);
        sectionDiv.append(inputName);
        sectionDiv.append(removeButton);

        //$("#masterdiv").remove($("#addbtn"));
        //$("#addbtn").remove();
        $("#masterdiv").append($("#addbtn"));

        // fields from image-upload macro end here

        //image-upload code with a few changes
        // firstly setup the fields
        var field_upload = 'input[name="' + options.field_upload + '"]';
        var field_url = 'input[name="' + options.field_url + '"]';
        var field_clear = 'input[name="' + options.field_clear + '"]';
        var field_name = 'input[name="' + options.field_name + '"]';

        this.input[count] = $(field_upload, sectionDiv);
        this.field_url[count] = $(field_url, sectionDiv).parents('.control-group');
        this.field_image[count] = this.input[count].parents('.control-group');
        this.field_url_input[count] = $('input', this.field_url[count]);
        this.field_name[count] = sectionDiv.parents('form').find(field_name);
        this.label_location[count] = $('label[for="field-image-url' + count + '"]');
        this.is_data_resource[count] = (this.options.field_url === 'url') && (this.options.field_upload === 'upload');

        // Is there a clear checkbox on the form already?
        var checkbox = $(field_clear, sectionDiv);
        if (checkbox.length > 0) {
          checkbox.parents('.control-group').remove();
        }
        // Adds the hidden clear input to the form
        //CHANGE
        this.field_clear[count] = $('<input type="hidden" name="clear_upload">')
          .appendTo(sectionDiv);

        // Button to set the field to be a URL
        this.button_url[count] = $('<a href="javascript:;" class="btn" id="url-' + count + '"><i class="icon-globe"></i>'+this.i18n('url')+'</a>')
          .prop('title', this.i18n('url_tooltip'))
          .on('click', this._onFromWeb)
          .insertAfter(this.input[count]);


        // Button to attach local file to the form
        this.button_upload[count] = $('<a href="javascript:;" class="btn"><i class="icon-cloud-upload"></i>'+this.i18n('upload')+'</a>')
          .insertAfter(this.input[count]);

        // Button for resetting the form when there is a URL set
        $('<a href="javascript:;" class="btn btn-danger btn-remove-url" id="remove-upload-' + count + '">'+this.i18n('remove')+'</a>')
          .prop('title', this.i18n('remove'))
          .on('click', this._onRemove)
          .insertBefore(this.field_url_input[count]);


        // Update the main label (this is displayed when no data/image has been uploaded/linked)
        $('label[for="field-image-upload' + count + '"]').text(options.upload_label || this.i18n('upload_label'));


        // Setup the file input
        this.input[count]
          .on('mouseover', this._onInputMouseOver)
          .on('mouseout', this._onInputMouseOut)
          .on('change', this._onInputChange)
          .prop('title', this.i18n('upload_tooltip'))
          .css('width', this.button_upload[count].outerWidth());


        // Fields storage. Used in this.changeState
        this.fields[count] = $('<i />')
          .add(this.button_upload[count])
          .add(this.button_url[count])
          .add(this.input[count])
          .add(this.field_url[count])
          .add(this.field_image[count]);

        // Disables autoName if user modifies name field
        this.field_name[count]
          .on('change', this._onModifyName);
        // Disables autoName if resource name already has value,
        // i.e. we on edit page
        if (this.field_name[count].val()){
          this._nameIsDirty = true;
        }

        if (options.is_url) {
          this._showOnlyFieldUrl(count);

          this._updateUrlLabel(this.i18n('label_for_url'));
        } else if (options.is_upload) {
          this._showOnlyFieldUrl(count);

          this.field_url_input[count].prop('readonly', true);
          // If the data is an uploaded file, the filename will display rather than whole url of the site
          var filename = this._fileNameFromUpload(this.field_url_input[count].val());
          this.field_url_input[count].val(filename);

          this._updateUrlLabel(this.i18n('label_for_upload'));
        } else {
          this._showOnlyButtons(count);
        }

        //on click event for removing the whole section

        var field_url_input = this.field_url_input;
        var resource_id = this.resource_id;

        $('#remove-' + count).click(function(e){
            e.preventDefault();
            var id = this.id.substr(this.id.indexOf("-") + 1);
            sectionDiv.remove();

            var image_url = field_url_input[id].val();

            if(image_url.length > 24 && image_url.startsWith("http") == false){
                var data = new FormData();
                data.append('image_url', image_url);
                data.append('resource_id', resource_id);

                $.ajax({
                    url: '/image_delete',
                    data: data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    type: 'POST'
                });
            }
        });

    },

    /* Quick way of getting just the filename from the uri of the resource data
     *
     * url - The url of the uploaded data file
     *
     * Returns String.
     */
    _fileNameFromUpload: function(url) {
      // remove fragment (#)
      url = url.substring(0, (url.indexOf("#") === -1) ? url.length : url.indexOf("#"));
      // remove query string
      url = url.substring(0, (url.indexOf("?") === -1) ? url.length : url.indexOf("?"));
      // extract the filename
      url = url.substring(url.lastIndexOf("/") + 1, url.length);

      return url; // filename
    },

    /* Update the `this.label_location` text
     *
     * If the upload/link is for a data resource, rather than an image,
     * the text for label[for="field-image-url"] will be updated.
     *
     * label_text - The text for the label of an uploaded/linked resource
     *
     * Returns nothing.
     */
    _updateUrlLabel: function(label_text, id) {
      if (! this.is_data_resource[id]) {
        return;
      }

      this.label_location[id].text(label_text);
    },

    /* Event listener for when someone sets the field to URL mode
     *
     * Returns nothing.
     */
    _onFromWeb: function(event) {
      var id = parseInt(event.target.id.slice(-1));
      this._showOnlyFieldUrl(id);

      this.field_url_input[id].focus()
        .on('blur', this._onFromWebBlur);

      if (this.options.is_upload) {
        this.field_clear[id].val('true');
      }

      this._updateUrlLabel(this.i18n('label_for_url'), id);
    },

    /* Event listener for resetting the field back to the blank state
     *
     * Returns nothing.
     */
    _onRemove: function(event) {
      var id = parseInt(event.target.id.slice(-1));
      var data = new FormData();
      data.append('image_url', this.field_url_input[id].val());
      data.append('resource_id', this.resource_id);

      $.ajax({
          url: '/image_delete',
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          type: 'POST'
      });

      this._showOnlyButtons(id);

      this.field_url_input[id].val('');
      this.field_url_input[id].prop('readonly', false);

      this.field_clear[id].val('true');
      this.input[id].val('');
    },


    /* Event listener for when someone chooses a file to upload
     *
     * Returns nothing.
     */
    _onInputChange: function(event) {
      var id = parseInt(event.target.id.slice(-1));
      var data = new FormData();

      jQuery.each(this.input[id][0].files, function(i, file) {
        data.append('file-'+i, file);
      });
      /*
      jQuery.each(jQuery($('#field-image-upload' + count))[0].files, function(i, file) {
        data.append('file-'+i, file);
      });*/

      data.append('dict', this.data_dict);
      data.append('resource_id', this.resource_id);

      var file_name = '';

      $.ajax({
          url: '/image_upload',
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          type: 'POST',
          success: function(response){
            file_name = response;
        },
        async: false
      });

      //var file_name = this.input.val().split(/^C:\\fakepath\\/).pop();

      this.field_url_input[id].val(file_name);

      //new
      this.input[id].val('');

      this.field_url_input[id].prop('readonly', true);

      this.field_clear[id].val('');

      this._showOnlyFieldUrl(id);

      this._autoName(file_name, id);

      this._updateUrlLabel(this.i18n('label_for_upload'), id);
    },

    /* Show only the buttons, hiding all others
     *
     * Returns nothing.
     */
    _showOnlyButtons: function(id) {
      this.fields[id].hide();
      this.button_upload[id]
        .add(this.field_image[id])
        .add(this.button_url[id])
        .add(this.input[id])
        .show();
    },

    /* Show only the URL field, hiding all others
     *
     * Returns nothing.
     */
    _showOnlyFieldUrl: function(id) {
      this.fields[id].hide();
      this.field_url[id].show();
    },

    /* Event listener for when a user mouseovers the hidden file input
     *
     * Returns nothing.
     */
    _onInputMouseOver: function(event) {
      var id = parseInt(event.target.id.slice(-1));
      this.button_upload[id].addClass('hover');
    },

    /* Event listener for when a user mouseouts the hidden file input
     *
     * Returns nothing.
     */
    _onInputMouseOut: function(event) {
      var id = parseInt(event.target.id.slice(-1));
      this.button_upload[id].removeClass('hover');
    },

    /* Event listener for changes in resource's name by direct input from user
     *
     * Returns nothing
     */
    _onModifyName: function() {
      this._nameIsDirty = true;
    },

    /* Event listener for when someone loses focus of URL field
     *
     * Returns nothing
     */
    _onFromWebBlur: function(event) {
      var id = parseInt(event.target.id.slice(-1));
      var url = this.field_url_input[id].val().match(/([^\/]+)\/?$/)
      if (url) {
        this._autoName(url.pop(), id);
      }
    },

    /* Automatically add file name into field Name
     *
     * Select by attribute [name] to be on the safe side and allow to change field id
     * Returns nothing
     */
     _autoName: function(name, id) {
        if (!this._nameIsDirty){
          this.field_name[id].val(name);
        }
     }
  };
});

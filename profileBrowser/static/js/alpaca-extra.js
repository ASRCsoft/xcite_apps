// some extra goodies for alpaca

/* making a Date Range Picker field */
$.alpaca.Fields.DateRangeField = $.alpaca.Fields.DatetimeField.extend({
    getFieldType: function() {
	return 'daterange';
    },
    afterRenderControl: function(model, callback) {
	var self = this;

	if (self.view.type !== "display")
	{
	    if ($.fn.daterangepicker)
	    {
		/* make sure it updates correctly if you want to show placeholder text */
		if (self.options.placeholder) {
		    self.options.picker['autoUpdateInput'] = false;
		};
		self.getControlEl().daterangepicker(self.options.picker);

		// alright the autoupdate is ok again:
		self.getControlEl().data('daterangepicker').autoUpdateInput = true;

		self.picker = self.getControlEl().data('daterangepicker');
		/* if (self.picker && self.options.dateFormat)
		   {
		   self.picker.format(self.options.dateFormat);
		   }
		   if (self.picker)
		   {
		   self.options.dateFormat = self.picker.format();
		   }*/

		// with daterangepicker, trigger change using plugin
		self.control.on("apply.daterangepicker", function(e) {
		    // we use a timeout here because we want this to run AFTER control click handlers
		    setTimeout(function() {
			self.onChange.call(self, e);
			self.triggerWithPropagation("change", e);
		    }, 250);

		});

		// set value if provided
		/* if (self.data) {
		   self.picker.date(self.data);
		   }*/
	    }
	}
	callback();
    },
});
$.alpaca.registerFieldClass('daterange', $.alpaca.Fields.DateRangeField);
// have it use the date-time template be default
$.alpaca.registerDefaultFormatFieldMapping("date-time", "daterange");

/* a selectlist with integrated leaflet map */
$.alpaca.Fields.LeafletSelect = $.alpaca.Fields.SelectField.extend({
    getFieldType: function() {
	return 'leaflet-select';
    },
    clickMarker: function(e) {
	var marker = e.target;
	var marker_val = marker['value'];
	var event = e.originalEvent;
	var shift = event.shiftKey || event.ctrlKey || event.metaKey;
	var selected_sites = this.getValue();
	if (selected_sites) {
	    var marker_is_selected = selected_sites.indexOf(marker_val) != -1;
	} else {
	    var marker_is_selected = false;
	};
	if (shift && marker_is_selected) {
	    this.deselectMarker(marker);
	} else {
	    this.selectMarker(marker, shift);
	};
	if (this.options.multiple && $.fn.multiselect && !this.isDisplayOnly()) {
	    $(this.getControlEl()).multiselect('refresh');
	};
	this.control.change();
    },
    selectMarker: function(marker, shift) {
	/* when the marker is selected the style should
	   change and the corresponding list item should be
	   selected, then a change event is called */
	var selected_vals = this.getValue();
	var marker_val = marker['value'];
	marker.setStyle(this.options.selectedMarker);
	if (shift && selected_vals.indexOf(marker_val) == -1) {
	    selected_vals.push(marker_val);
	} else {
	    selected_vals = [marker_val];
	};
	this.setValue(selected_vals);
    },
    deselectMarker: function(marker) {
	marker.setStyle(this.options.marker);
	var marker_val = marker['value'];
	var new_vals = [];
	$.each(this.getValue(), function(i, val) {
	    if (val != marker_val) {
		new_vals.push(val);
	    };
	});
	this.setValue(new_vals);
    },
    getControlEl: function()
    {
        return this.control.slice(0, 1);
    },
    selectAfterRenderControl: $.alpaca.Fields.SelectField.prototype.afterRenderControl,
    afterRenderControl: function(model, callback)
    {
	var self = this;

	if (this.options.hideSelect) {
	    if (this.options.multiple && $.fn.multiselect && !this.isDisplayOnly()) {
		this.selectAfterRenderControl(model, callback);
		$(this.field).find('button').hide();
	    } else {
		$(this.control[0]).hide();
		this.selectAfterRenderControl(model, callback);
	    };
	} else {
	    this.selectAfterRenderControl(model, callback);
	};
	
	/* initialize the map when added to the display */
	this.on('ready', function() {
	    /* organize the markers */
	    this.markers = L.featureGroup();
	    var locations = this.options.locations;
	    var selected_sites = this.getValue();
	    var markerFun = this.options.markerFunction || L.circleMarker;
	    if (locations) {
		// (this loop will break if locations haven't been provided)
		$.each(this.getEnum(), function(i, site) {
		    if (locations[site]) {
			var marker = markerFun(locations[site], this.options.marker);
			marker['value'] = site;
			marker.on('click', this.clickMarker.bind(this));
			if (selected_sites && selected_sites.indexOf(marker['value']) != -1) {
			    marker.setStyle(this.options.selectedMarker);
			};
			marker.bindTooltip(this.options.optionLabels[i]);
			this.markers.addLayer(marker);
		    };
		}.bind(this));
	    };

	    var map_div = this.containerItemEl[0].getElementsByClassName('alpaca-form-leaflet-select-map')[0];
	    var map_options = this.options.map_options;
	    /* remove existing map if needed */
	    if (this.map) {
		this.map.remove();
		this.map = null;
	    }
	    this.map = L.map(map_div, map_options).fitBounds(this.markers.getBounds().pad(.05));
	    if (this.options.tile) {
		
	    };
	    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2tlcHRpa29zIiwiYSI6ImNqNWU2NjNhYzAwcDEycWpqdTJtNWJmNGYifQ.kxK-j2hWsX46EhH5PnsTfA', {
		maxZoom: 18,
		id: 'mapbox.streets'
	    }).addTo(this.map);
	    this.markers.addTo(this.map);
	}.bind(this));
    },
    onChange: function(e) {
	// ignore events coming from the map
	var target_tag = e.target.tagName;
	if (target_tag == 'SELECT' || target_tag == 'BUTTON') {
	    var selected_sites = this.getValue() || [];
    	    $.each(this.markers.getLayers(), function(i, marker) {
    		/* set the appropriate styles */
    		if (selected_sites.indexOf(marker['value']) == -1) {
    		    marker.setStyle(this.options.marker);
    		} else {
    		    marker.setStyle(this.options.selectedMarker);
    		};
    	    }.bind(this));
	};
	if (this.options.multiple && $.fn.multiselect && !this.isDisplayOnly()) {
	    $(this.getControlEl()).multiselect('refresh');
	};
    },
    selectSetValue: $.alpaca.Fields.SelectField.prototype.setValue,
    setValue: function(val) {
	this.selectSetValue(val);
	// update the map (if it exists)
	if (this.markers) {
	    var selected_sites = this.getValue();
	    $.each(this.markers.getLayers(), function(i, marker) {
		/* set the appropriate styles */
		if (selected_sites && selected_sites.indexOf(marker['value']) != -1) {
		    marker.setStyle(this.options.selectedMarker);
		} else {
		    marker.setStyle(this.options.marker);
		};
	    }.bind(this));
	};
    }
});
$.alpaca.registerFieldClass('leaflet-select', $.alpaca.Fields.LeafletSelect);

/* add the leaflet template to bootstrap-edit */
$.alpaca.registerView({
    "id": 'bootstrap-edit-extra',
    "parent": 'bootstrap-edit',
    "templates": {
	'control-leaflet-select': '<select id="{{id}}" {{#if options.readonly}}readonly="readonly"{{/if}} {{#if options.multiple}}multiple="multiple"{{/if}} {{#if options.size}}size="{{options.size}}"{{/if}} {{#if name}}name="{{name}}"{{/if}}> \
{{#if options.multiple}} \
{{#if options.hideNone}} \
{{else}} \
<option value="">{{{options.noneLabel}}}</option> \
{{/if}} \
{{#each selectOptions}} \
<option value="{{{value}}}" {{#if selected}}selected="selected"{{/if}}>{{text}}</option> \
{{/each}} \
{{else}} \
{{#if options.hideNone}} \
{{else}} \
<option value="">{{{options.noneLabel}}}</option> \
{{/if}} \
{{#each selectOptions}} \
<option value="{{{value}}}" {{#if selected}}selected="selected"{{/if}}>{{text}}</option> \
{{/each}} \
{{/if}} \
</select> \
<div id="map-{{id}}" class="alpaca-form-leaflet-select-map"></div>'
    }
});

/* a few useful variables */
var selected_sites = [];
var instrument = 'lidar';
var mwr_data = ['temp', 'vapor', 'liquid', 'rh'];
/* the data variables that depend on wind information */
var requires_wind = ['barbs', 'hwind', 'zwind', 'xwind', 'ywind'];
/* keeping track of the changes to the selected sites */
var old_sites = [];
var spinner = new Spinner();
/* this variable stores information about the selected
   lidar/scan combinations */
var lidars;

// a bunch of functions to help update the page
var get_date_range = function() {
    return $.getJSON(daterange_url);
};
var get_lidar_scans = function(v) {
    var v = dataset.getValue();
    var min_time = drp.startDate.format('YYYY-MM-DDTHH:mm:ss.SSS[Z]');
    var max_time = drp.endDate.format('YYYY-MM-DDTHH:mm:ss.SSS[Z]');
    var url = scans_url + '?time_min=' +
	min_time + '&time_max=' +
	max_time + '&var=' + v;
    return $.getJSON(url);
};
var update_graphs = function() {
    var selected_sources = sources.getValue();
    var var_str = dataset.getValue();
    /* the start and end dates are stored in the local
       time zone instead of UTC. Rather than converting it,
       I'm just printing out the local time and pretending
       it's UTC */
    var min_time = drp.startDate.format('YYYY-MM-DDTHH:mm:ss.SSS[Z]');
    var max_time = drp.endDate.format('YYYY-MM-DDTHH:mm:ss.SSS[Z]');
    var barbs = form.childrenByPropertyId['barb'].getValue();
    var pbl = form.childrenByPropertyId['pbl'].getValue();
    /* stop if no sources selected */
    if (sources.length == 0) {
	return
    }
    var scan_ids = [];
    $.each(selected_sources, function(i0, index) {
	var i2 = parseInt(index);
	scan_ids.push(lidars[i2]['scan_id']);
    });
    var url = plot_url + '?scan_id=' +
	scan_ids.join() + '&time_min=' +
	min_time + '&time_max=' +
	max_time + '&var=' +
	var_str + '&type=heat';
    if (barbs) {
	url += '&barbs=True';
    };
    if (pbl) {
	url += '&pbl=True';
    };
    spinner.spin();
    graph.css('opacity', .4);
    $('body').append(spinner.el);
    graph.attr("src", url);
};
var disable_options = function() {
    var var_str = dataset.getValue();
    var options = $(sources.control[0].options);
    var var_requires_wind = requires_wind.indexOf(var_str) != -1;
    /* var barbs_selected = barbbox.is(":checked");*/
    if (var_requires_wind) {
	/* disable the invalid choices */
	options.each(function(i, option) {
	    /* disable if mode is not DBS */
	    var mode = lidars[i]['mode'];
	    if (mode != 'dbs') {
		option.disabled = true;
	    };
	});
    } else {
	/* none should be disabled */
	options.each(function(i, option) {
	    /* disable if mode is not DBS */
	    option.disabled = false;
	});
    };
};
var update_map = function() {
    console.log('update_map');
    var selected_sites = [];
    /* get all the selected sites */
    /* get unique selected sites */
    var selected_sources = sources.getValue();
    $.each(selected_sources, function(i, n) {
	var site = lidars[parseInt(n)]['site_name'];
	if (selected_sites.indexOf(site) == -1) {
	    selected_sites.push(site);
	};
    });
    sites.setValue(selected_sites);
    /* to keep track of changes */
    old_sites = selected_sites;
};
function update_var() {
    disable_options();
    // are we looking at lidar or mwr data?
    var v = dataset.getValue();
    var var_instr = (mwr_data.indexOf(v) != -1) ? 'mwr' : 'lidar';
    if (var_instr == instrument) {
	// not going to update the choices in this case
	return $.when();
    } else {
	instrument = var_instr;
	update_lidar_scans();
    };
};
function siteSelect(site) {
    /* update the selected sources in response to
       selecting a site-- I'd rather do this via alpaca
       somehow but it absolutely must be done in response
       to clicking */
    var selected_sources = sources.getValue();
    var selected_sites = sites.getValue();
    /* first remove any sources that need to be removed */
    var new_selected_sources = [];
    $.each(selected_sources, function(i, source) {
	if (selected_sites.indexOf(lidars[parseInt(source)]['site_name']) != -1) {
	    new_selected_sources.push(source);
	};
    });
    $.each(lidars, function(i, lidar) {
	if (lidar['site_name'] == site && selected_sources.indexOf(String(i)) == -1) {
	    new_selected_sources.push(String(i));
	};
    });
    sources.setValue(new_selected_sources);
};
function siteDeselect(site) {
    /* update the selected sources in response to
       deselecting a site-- I'd rather do this via alpaca
       somehow but it absolutely must be done in response
       to clicking */
    var selected_sources = sources.getValue();
    var new_selected_sources = [];
    $.each(selected_sources, function(i, source) {
	if (lidars[parseInt(source)]['site_name'] != site) {
	    new_selected_sources.push(source);
	};
    });
    sources.setValue(new_selected_sources);
};
function markerClick() {
    var new_sites = sites.getValue();
    $.each(old_sites, function(i, old_site) {
	if (new_sites.indexOf(old_site) == -1) {
	    /* site was removed */
	    siteDeselect(old_site);
	};
    });
    $.each(new_sites, function(i, new_site) {
	if (old_sites.indexOf(new_site) == -1) {
	    /* site was added */
	    siteSelect(new_site);
	};
    });
    old_sites = selected_sites;
};

/* setting up some alpaca options */
var drpicker_options = {
    timePicker: true,
    timePicker24Hour: true,
    timePickerIncrement: 5,
    showDropdowns: true,
    locale: {
	format: 'MM/DD/YYYY HH:mm'
    },
    opens: 'left'
};
var var_options = {
    'cnr': 'CNR',
    'drws': 'DRWS',
    'barbs': 'Wind Direction',
    'hwind': 'Horizontal Wind Speed',
    'zwind': 'Vertical Wind Speed',
    'xwind': 'x Wind Speed',
    'ywind': 'y Wind Speed',
    'temp': 'Temperature',
    'vapor': 'Vapor Density',
    'liquid': 'Liquid',
    'rh': 'Relative Humidity'
};
var map_options = {zoomControl: false,
		   maxZoom: 16};
var marker_options = {radius: 6, color: 'blue', weight: 0,
		      opacity: .8, fillOpacity: .8};
var selected_marker_options = {color: 'orange'};

$(document).ready(function() {
    // get urls from django
    form_div = $('#form');
    dataset_url = form_div.attr('data-datasets');
    template_url = form_div.attr('data-template');
    daterange_url = form_div.attr('data-daterange');
    scans_url = form_div.attr('data-scans');
    plot_url = form_div.attr('data-plot');

    // set up the graph image element
    graph = $('#lidar_graph');
    graph.on('load', function() {
	try {
	    spinner.stop();
	} catch(err) {};
	graph.css('opacity', 1);
	$("footer").hide().fadeIn('fast');
    });

    /* create the form */
    a=$("#form").alpaca({
	schema: {
            title: "Data Options",
            type: "object",
            properties: {
		dr: {
		    title: 'Time range (UTC)',
		    type: 'string'
		},
		var: {
                    type: 'string',
                    title: 'Data',
		    default: 'cnr'
		},
		sources: {
                    type: 'string',
                    title: 'Sources'
		},
		sites: {
                    type: 'string',
                    title: 'Sites'
		},
		barb: {
		    title: 'Overlays'
		},
		pbl: {
		}
            }
	},
	options: {
	    /* helper: "<a href=\"{% url 'datasets' %}\" target=\"_blank\">see data definitions</a>",*/
	    focus: false,
	    form: {
		attributes: {
                    action: 'javascript:update_graphs();'
		},
		buttons:{
                    submit: {
			title: 'View Data'
		    }
		},
            },
            fields: {
		dr: {
		    placeholder: 'Loading...',
		    type: 'daterange',
		    picker: drpicker_options
		},
		var: {
                    type: 'select',
		    dataSource: var_options,
		    removeDefaultNone: true,
		    sort: false,
		    helper: "<a href=\"" + dataset_url + "\" target=\"_blank\">see data definitions</a>"
		},
		sources: {
                    type: "select",
		    multiple: true,
		    removeDefaultNone: true
		},
		sites: {
                    type: "leaflet-select",
		    removeDefaultNone: true,
		    multiple: true,
		    map_options: map_options,
		    marker: marker_options,
		    selectedMarker: selected_marker_options,
		    hideSelect: true
		},
		barb: {
		    type: 'checkbox',
		    rightLabel: 'Wind barbs (DBS mode only)'
		},
		pbl: {
		    type: 'checkbox',
		    rightLabel: 'PBL/Residual Layer (Experimental)',
		    hidden: true
		}
            }
	},
	view: {
	    parent: "bootstrap-edit-extra",
	    layout: {
		template: template_url,
		bindings: {
		    var: 'left',
			dr: 'right',
			sources: 'left',
			sites: 'right',
			barb: 'left',
			pbl: 'left'
		}
	    }
	},
	postRender: function(control) {
	    /* is there a graph already? */
	    var has_graph = false;
	    
	    /* get the map div ID so we can add a spinner */
	    var map_div_id = 'map-' + control.childrenByPropertyId['sites'].id;

	    // set up some convenient global variables
	    form = $('#form').alpaca('get');
	    console.log(form);
	    sources = control.childrenByPropertyId['sources'];
	    sites = control.childrenByPropertyId['sites'];
	    dr = control.childrenByPropertyId['dr'];
	    drp = dr.control.data('daterangepicker');

	    /* make needed changes when selected var changes */
	    dataset = control.childrenByPropertyId['var'];

	    update_lidar_scans = function() {
		/* updating the lidar select dropdown list */
		var v = control.childrenByPropertyId['var'].getValue();
		/* can't add wind barbs to radiometer data at the moment
		   so don't allow that */
		/* if (instrument == 'mwr') {
		   barbbox.prop('checked', false);
		   barbbox.prop('disabled', true);
		   } else {
		   barbbox.prop('disabled', false);
		   };*/
		
		/* disable all the options while we update them, and add
		   spinner to the map */
		sources.options.disabled = true;
		sources.refresh();
		
		spinner.spin();
		$('#' + map_div_id).append(spinner.el);
		/* get available scans and make new list */
		/* keep track of the sites-- try to keep these sites
		   selected when updating the choices */
		return get_lidar_scans().done(function(lidars_api) {
		    lidars = lidars_api;
		    var arr = [];
		    var sites_data = [];
		    var site_locations = {};
		    $.each(lidars, function(i, lidar) {
			var value = String(i);
			arr.push({value: value,
				  text: lidar['lidar_name'] + ' (' + lidar['scan_name'] + ')'});
			var site_name = lidar['site_name'];
			if (sites_data.indexOf(site_name) == -1) {
			    sites_data.push(site_name);
			    var latlng = [lidar['latitude'], lidar['longitude']];
			    site_locations[site_name] = latlng;
			};
		    });
		    /* change the available sites */
		    var sites = control.childrenByPropertyId['sites'];
		    sites.options.dataSource = sites_data;
		    sites.options.locations = site_locations;
		    sites.refresh();
		    
		    /* change the selectlist options via alpaca */
		    sources.options.dataSource = arr;
		    sources.options.disabled = false;
		    sources.refresh();
		    
		    
		    /* disable some options if needed (for wind datasets) */
		    disable_options();
		    /* update_map();*/
		    spinner.stop();

		    // get a graph if there isn't one
		    if (!has_graph) {
			sources.setValue(sources.getEnum()[0]);
			$(sources.control).change();
			update_graphs();
			has_graph = true;
		    }
		});
	    };

	    // update the form in response to changes
	    sources.on('change', update_map);
	    dataset.on('change', update_var);
	    sites.on('change', markerClick);
	    dr.on('change', update_lidar_scans);
	    /* print an error message when the graph fails to load */
	    graph.on('error', function(ev) {
		try {
		    spinner.stop();
		} catch(err) {};
		graph.css('opacity', 1);
		graph.attr('alt', 'Error: failed to get the image');
	    });
	    
	    /* get the max and min times for the datetime
	       fields, and set them to default values */
	    get_date_range().done(function(result) {
		/* make sure to clone to avoid
		   accidentally changing the
		   daterangeicker times in other
		   functions!! Use 'clone' to modify the
		   times! */
		var min_date = moment(result[0]);
		var cur_date = moment(result[1]);
		var max_date = cur_date.clone().add(1, 'd');
		drp.minDate = min_date;
		drp.maxDate = max_date;
		drp.setStartDate(cur_date);
		/* Starting the autoupdate here so it
		   only updates once when the page loads! */
		drp.autoUpdateInput = true;
		drp.setEndDate(max_date);
	    });
	}
    });
    console.log(a.alpaca('get'));
});

// this file should contain the controls for the hysplit simArray

// how this should work:
// 1) set up simulation array
// 2) create controls
// 3) connect controls to simulation array

// to set up the simulation array:
// 1) get sites and times
// 2) write hysplit layergroup generating function (takes site, time, fwd/bwd as arguments)
// 3) we're done!

// a layerArray designed specifically for switching between simulation
// results (site x fwd/bwd x time)
L.LayerArray.Simulations2 = L.LayerArray.Simulations.extend({
    // some special SimulationArray functions just for us
    // this object holds all of the site-specific objects
    initialize: function(options) {
	// will need to have: site name, fwd, date, hysplit
	L.LayerArray.Simulations.prototype.initialize.call(this, options);
	// this.options = options;
	this.fwd = this.options.fwd;
	this.date = this.options.date;

	// useful for organizing the controls
	this.times = this.values[2];
	this.heights;

	// keep track of the site/time/fwd indices
	this.site = 0;
	this.time = 0;
	this.fwd = 0;
    },
    setIndex: function(ind) {
	this.ind = ind;
	this.site = ind[0];
	this.fwd = ind[1];
	this.time = ind[2];
    },
    switchTimeVal: function(t) {
	var time_index = this.times.map(Number).indexOf(+t);
	if (this.time == time_index) {
	    // don't do anything
	    return false;
	}
	if (time_index == -1) {
	    throw 'Time not found in switchTimeVal function.'
	}
	this.switchToIndex([this.site, this.fwd, time_index]);
    },
    switchSite: function(site) {
	// check to make sure we actually need to switch sites
	var new_values = this.getIndexValue(this.ind);
	if (site != new_values[0]) {
	    new_values[0] = site;
	    return this.switchToValue(new_values);
	} else {
	    return $.when();
	};
    },
    switchFwd: function(fwd) {
	var new_values = this.getIndexValue(this.ind);
	if (new_values[1] != fwd) {
	    new_values[1] = fwd;
	    this.switchToValue(new_values);
	}
    }
});

L.layerArray.simulations2 = function(options) {
    return new L.LayerArray.Simulations2(options);
};


// make a simulationArray

// function that creates hysplit layergroup based on site, time, and fwd/bwd
data_server_url = 'http://pireds.asrc.cestm.albany.edu:5000';
contour_layer0 = L.layerGroup();
single_trajectory_layer0 = L.layerGroup();
ens_trajectory_layer0 = L.layerGroup();


function Hysplit(start_site_name, start_site_fwd, data_server_url) {
    this.data_server_url = data_server_url ? data_server_url : 'http://pireds.asrc.cestm.albany.edu:5000';
    // this.sites = sites;
    this.contour_layer = L.layerGroup([]);
    this.ens_trajectory_layer = L.layerGroup([]);
    this.single_trajectory_layer = L.layerGroup([]);
    this.origin_layer = L.layerGroup([]);
    this.timedim = L.timeDimension({times: []});
    // make two actionLayers (fwd and bck) to include in the layer controller
    // this.fwd_layer = L.actionLayer({hysplit: this, fwd: true});
    // this.bck_layer = L.actionLayer({hysplit: this, fwd: false});
    this.cur_name = start_site_name;
    this.cur_fwd = start_site_fwd;
    this.dates = [];
    this.cur_date;
    // an multidimensional arrayLayer holding all of the site and
    // fwd/bwd combinations
    this.siteArray;
    // custom simulation ids
    this.custom_id = {};
    this.map;
    this.sites;
    this.cached_sites = {};
    this.site_map;
    this.origin_circle;
    this.time_slider;
}

Hysplit.prototype.getSites = function getSites() {
    return $.getJSON(this.data_server_url + '/sites', function (json) {
	this.sites = json;
    }.bind(this));
}

Hysplit.prototype.getTimes = function getTimes() {
    return $.getJSON(this.data_server_url + '/times', function(json) {
	this.time_json = json;
	this.dates = this.time_json['data'].map(function(x) {return new Date(x[0])});
	this.cur_date = this.dates[0];
    }.bind(this));
}

Hysplit.prototype.addTileLayer = function addTileLayer() {
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        // attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        //     '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        //     'Imagery Â© <a href="http://mapbox.com">Mapbox</a>',
	attribution: false,
        id: 'mapbox.light'
    }).addTo(this.map);
}

Hysplit.prototype.getColor = function(d) {
    return d >= -10 ? '#800000' :
	d >= -11 ? '#ff3200' :
	d >= -12 ? '#ffb900' :
	d >= -13 ? '#b6ff41' :
	d >= -14 ? '#41ffb6' :
	d >= -15 ? '#00a4ff' :
	d >= -16 ? '#0012ff' :
	'#000080';
}

Hysplit.prototype.addLegend = function addLegend() {
    var this2 = this;
    var legend = L.control({position: 'bottomright'});
    var levels = [-17, -16, -15, -14, -13, -12, -11, -10];
    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend'),
            /* grades = [0, 10, 20, 50, 100, 200, 500, 1000],*/
            grades = levels,
            labels = [],
            from, to;
        var units;
	units = 'm<sup>-3</sup>';
        // if (this2.cur_site.heights[this2.cur_site.height] == 0) {
        //     units = 'm<sup>-2</sup>';
        // } else {
        //     units = 'm<sup>-3</sup>';
        // }
	var legend_title = '<h4>Dilution Factor<br>(<span class="_units_here">' + units + '</span>)</h4>';
        for (var i = grades.length - 1; i >= 0; i--) {
            from = grades[i];
            to = grades[i + 1];
            labels.push('<i style="background:' + this2.getColor(from) + '"></i> <b>' +
                        '10<sup>' + from + '</sup>' +
                        (i + 1 < grades.length ? '&ndash;10<sup>' + to + '</sup>' : '+'));
        }
        div.innerHTML = legend_title + labels.join('<br>');
        return div;
    };
    legend.addTo(this.map);
}

Hysplit.prototype.updateOrigin = function updateOrigin(latlon) {
    if (this.origin_layer.getLayers().length == 0) {
	// add the origin point
	var cm_orig_options = {radius: 5, color: '#ff9000',
    			       weight: 2, fillOpacity: .6};
	var origin = L.circleMarker(latlon, cm_orig_options);
	// origin.on('mouseover', function(e) {this.mouseoverMarker(e)});
	// origin.on('mouseout', function (e) {this.mouseoutMarker(e)});
	this.origin_layer.addLayer(origin);
    } else {
	this.origin_layer.getLayers()[0].setLatLng(latlon);
    }
    this.map.flyTo(latlon);
}

Hysplit.prototype.fwd_str = function fwd_str() {
    if (this.cur_fwd) {
	return 'Forward';
    } else {
	return 'Backward';
    }
}

Hysplit.prototype.makeSimChooserOptions = function() {
    var site_options = {};
    var site_locations = {};
    for (i=0; i < this.sites.length; i++) {
	site = this.sites[i];
	site_options[site['stid']] = site['name'];
	site_locations[site['stid']] = [site['latitude'], site['longitude']];
    };
    var map_options = {zoomControl: false,
		       maxZoom: 16,
		       attributionControl: false};
    var marker_options = {radius: 6, color: 'blue', weight: 0,
			  opacity: .8, fillOpacity: .8};
    var selected_marker_options = {color: 'orange'};
    var utc_times = this.dates.map(function(x) {
	var raw_time = moment(x);
	return raw_time.subtract(raw_time.utcOffset(), 'm');
    });
    var min_time = moment.min(utc_times);
    var max_time = moment.max(utc_times);
    return {
	"schema": {
            // "title": "Simulation Info",
            "type": "object",
            "properties": {
		"site": {
		    "title": "Release Site",
                    "type": "string",
		    default: 'VOOR'
		},
		"fwd": {
		    "title": "Direction",
                    "type": "string",
		    "enum": ['true', 'false'],
		    default: 'true',
		    hideNone: true
		},
		time: {
                    "title": "Release/Reception Time (UTC)",
		    "format": "datetime",
		    enum: utc_times.map(function(x) {return x.format("YYYY-MM-DD HH:00")})
		},
		duration: {
                    "title": "Release Duration (hours)",
		    "type": "string",
		    default: 1,
		    readonly: true
		},
		"height": {
		    "title": "Release/Reception Height (m AGL)",
                    "type": "string",
		    default: 10,
		    readonly: true
		},
            }
	},
	"options": {
	    fields: {
		fwd: {
		    "type": "select",
		    optionLabels: ["Forward", "Backward"],
		    hideNone: true,
		    "events": {
			// selectlist emits change events
			"change": function() {
			    h1.siteArray.switchFwd(this.getValue() == 'true');
			},
			// if this is a radio field have to use the click event
			"click": function() {
			    h1.siteArray.switchFwd(this.getValue() == 'true');
			},
                    }
		},
		site: {
		    "type": "leaflet-select",
		    dataSource: site_options,
		    locations: site_locations,
		    map_options: map_options,
		    marker: marker_options,
		    selectedMarker: selected_marker_options,
		    hideNone: true,
		    "events": {
			"change": function() {
			    h1.siteArray.switchSite(this.getValue()).then(function() {
				var new_latlon = this.options.locations[this.getValue()];
				h1.updateOrigin(new_latlon);
			    }.bind(this));
			},
                    }
		},
		duration: {
		    "type": "number",
		    hidden: true
		},
		"height": {
		    "type": "number",
		    hidden: true
		},
		time: {
		    "picker": {
			"format": "YYYY-MM-DD HH:00",
			defaultDate: max_time,
			enabledDates: utc_times,
			minDate: min_time,
			maxDate: max_time,
			enabledHours: [0, 12]
		    },
		    "events": {
			// slightly different event from datetimepicker package
			"dp.change": function(ev) {
			    var raw_time = ev.date;
			    // fix annoying timezone issues
			    var new_time = raw_time.add(moment().utcOffset(), 'm').toDate();
			    h1.siteArray.switchTimeVal(new_time);
			},
		    }
		}
	    }
	},
	view: "bootstrap-edit-extra"
    }
}

Hysplit.prototype.simInfoStart2 = function() {
    // organizing the simulation info
    var info_text = '<h4>Choose Simulation</h4>';
    info_text += '<div id="simchooser"></div>';
    return info_text;
}


Hysplit.prototype.addSimInfo = function() {
    /* simulation info box */  

    this.sim_info = L.control({position: 'topright'});
    var hysplit = this;
    this.sim_info.onAdd = function (map) { 
        this._div = L.DomUtil.create('div', 'info accordion');
        // Disable clicking when user's cursor is on the info box
        // (because we need to keep the lat/lon from earlier mouse
        // clicks!)
        L.DomEvent.disableClickPropagation(this._div);
        $(this._div).accordion({
            collapsible: true,
            heightStyle: "content",
            active: false,
	    activate: function() {
		// hysplit.site_map.invalidateSize();
		// fix the alpaca map
		var form = $('#simchooser').alpaca('get');
		var sites = form.childrenByPropertyId['site'];
		sites.map.invalidateSize();
		sites.map.fitBounds(sites.markers.getBounds().pad(.05));
	    }
        });
	// add current simulation info
	$(this._div).append(hysplit.simInfoStart2());

	// adding HYSPLIT info
	var hysplit_text = '<h4>About HYSPLIT</h4>';
	hysplit_text += '<div id="hysplit_info"><p>HYSPLIT uses wind fields to calculate particle trajectories and dispersion of gases. Visit the <a class="normala" href="https://www.arl.noaa.gov/hysplit/hysplit/">NOAA website</a> for more information.</p>';
	hysplit_text += '<p>For these simulations, HRRR forecasts provide the wind fields and New York State Mesonet sites serve as starting locations. The simulations run twice daily, starting from midnight and 12pm UTC, and we calculate both forward and backward trajectories.</p></div>';
	$(this._div).append(hysplit_text);

	// reset the accordion
	$(this._div).accordion();
        // this.update();
        return this._div;
    };
    // this.sim_info.update = this.updateSimInfo.bind(this);
    this.sim_info.addTo(this.map);
    $(this.sim_info._container).accordion('refresh')
    // set up the lat/lon action
    // this.map.on('click', function(e) {
    //     var latlng = e.latlng;
    //     var lat = latlng.lat;
    //     var lon = latlng.lng;
    //     document.querySelector('#userLat').value = lat;
    //     document.querySelector('#userLng').value = lon;
    // });
    // $("#simchooser").alpaca(sim_chooser_options);
    $("#simchooser").alpaca(this.makeSimChooserOptions());

    // need to make a few changes to the datetimepicker here!!
}

Hysplit.prototype.addLayerControl = function() {
    var this2 = this;
    var overlayMaps = {
    	'Dispersion': contour_layer0,
	'Single Trajectory': single_trajectory_layer0,
        'Ensemble Trajectories': ens_trajectory_layer0
    };
    // make sure to add the contour layer to the map by default
    contour_layer0.addTo(this.map);
    L.control.layers(null, overlayMaps, {position: 'topleft'}).addTo(this.map);
    // L.control.groupedLayers(null, overlayMaps, {position: 'topleft'}).addTo(this.map);
}

Hysplit.prototype.addTimeSlider = function addTimeSlider() {
    var time_options = {timeDimension: this.timedim, loopButton: true,
			// timeSlider: false, speedSlider: false,
			// minSpeed: 4,
                        timeSliderDragUpdate: true,
                        playReverseButton: true};
    this.time_slider = L.control.timeDimension(time_options);
    this.time_slider.addTo(this.map);
}

Hysplit.prototype.initialize = function initialize(divid) {
    var ajax_sites = this.getSites();
    var ajax_times = this.getTimes();
    $.when(ajax_sites, ajax_times).done(function() {
	var site_name = this.cur_name;
	var site_fwd = this.cur_fwd;
	// get all the site names
	var fwd_values = [true, false];
	var dates;
	makeHysplit = function(ind, vals) {
	    var site = vals[0];
	    var time = vals[2];
	    var fwd = vals[1];
	    var site_id = this.sites[ind[0]]['id'];
	    var time_id = this.time_json['index'][ind[2]];
	    var meta_url = data_server_url + '/metadata?site_id=' +
		site_id + '&time_id=' + time_id + '&fwd=' + fwd;
	    var deferred = new $.Deferred();
	    return $.getJSON(meta_url).then(function(results) {
		// make the hysplit layer
		var json = results['metadata'];
		var times = json['times'].map(function(text) {return new Date(text)});
		var heights = json['heights'];
		var hysplit_options = {metadata: json,
				       contour_layer: contour_layer0,
				       single_trajectory_layer: single_trajectory_layer0,
				       ens_trajectory_layer: ens_trajectory_layer0,
				       timedim: this.timedim,
				       n_ahead: 1,
				       hysplit: this};
		var hysplit = L.layerGroup.hysplit(hysplit_options);
		
		var sim_id = results['id'];

		try {
		    // get the ensemble trajectories if they exist
		    var trajectories = json['trajectories'];
		    var ens_trajectory_layer = L.geoJSON(trajectories, {
			onEachFeature: onEachTrajectory,
			dashArray: "10, 6, 4, 6",
			// dashOffset: (Math.random() * 10) + 'px',
			weight: 2,
			opacity: .4
		    });
		    var traj_options = {timeDimension: this.timedim,
					fwd: fwd};
		    hysplit.trajectories = L.timeDimension.layer.geoJson2(ens_trajectory_layer, traj_options);
		} catch(err) {};
		try {
		    // get the trajectory if it exists
		    var trajectory = json['trajectory'];
		    var single_trajectory_layer = L.geoJSON(trajectory, {
			// style: hysplit.singleTrajStyle,
			onEachFeature: onEachTrajectory,
			color: '#3355ff'
		    });
		    var traj_options = {timeDimension: this.timedim,
					fwd: fwd};
		    hysplit.trajectory = L.timeDimension.layer.geoJson2(single_trajectory_layer, traj_options);
		} catch(err) {};
		var makeContours = function(ind) {
		    if (ind.some(function(x) {return x < 0})) {
			throw "Negative index in makeLayer";
		    };
		    var contour_url = data_server_url + '/contours?sim_id=' +
			sim_id + '&height=' + ind[1] + '&time=' + ind[0];
		    return $.getJSON(contour_url).then(function(topojson) {
			return L.topoJson(topojson, {
			    style: contourStyle,
			    onEachFeature: function(f, l) {onEachFeature(f, l)},
			    smoothFactor: .5
			});
		    });
		}.bind(hysplit);
		var ls_options = {values: [hysplit.times, hysplit.heights],
				  makeLayer: makeContours};
		hysplit.contours = L.layerArray.contours(ls_options);
		var td_options = {timeDimension: this.timedim,
				  dim: 0};
		hysplit.td_layer = L.timeDimension.layer.layerArray(hysplit.contours, td_options);

		return hysplit;
	    }.bind(this));
	}.bind(this);
	// the dimension values of the 3-dimensional siteArray
	var site_names = this.sites.map(function(x) {return x['stid']})
	var site_dim_values = [site_names, [true, false], this.dates];
	var siteArray_options = {values: site_dim_values,
				 contour_layer: contour_layer0,
				 single_trajectory_layer: single_trajectory_layer0,
				 ens_trajectory_layer: ens_trajectory_layer0,
				 timedim: this.timedim,
				 makeLayer: makeHysplit};
	this.siteArray = L.layerArray.simulations2(siteArray_options);
	var map_options = {layers: [this.contour_layer],
			   attributionControl: false};
	this.map = L.map(divid, map_options).setView([43, -74.5], 7);
	this.addTileLayer();
	// this.addSiteSelector();
	this.origin_layer.addTo(this.map);
	this.addLayerControl();
	this.addTimeSlider();
	this.siteArray.addTo(this.map);
	this.changeSite(this.cur_name, this.cur_fwd, this.cur_date);
	this.addLegend();
    }.bind(this));
}

Hysplit.prototype.update_info = function update_info() {
    // if (this.sim_info) {
    // 	this.sim_info.update();
    // } else {
    // 	this.addSimInfo();
    // }
    if (!this.sim_info) {
	this.addSimInfo();
    }
}

Hysplit.prototype.changeSite = function changeSite(name, fwd, date, custom) {
    custom = (typeof custom === 'undefined') ? false : custom;
    // in case custom results are currently being shown
    if (this.custom) {
	this.cur_site.remove();
	this.custom = false;
    }
    if (custom) {
	// if custom, get the results manually
	var fwd_str = fwd ? 'fwd' : 'bwd';
        var sim_id = this.custom_id[fwd_str];
	var site_options = {name: 'Custom',
			    sim_id: sim_id,
			    fwd: fwd,
			    date: date,
			    contour_layer: this.contour_layer,
			    ens_trajectory_layer: this.ens_trajectory_layer,
			    single_trajectory_layer: this.single_trajectory_layer,
			    getColor: this.getColor,
			    hysplit: this,
                            metadata_url: this.data_server_url + '/metadata?sim_id=' + sim_id};
	var results = L.customSiteLayer(site_options);
	results.loadData().done(function() {
	    // remove the current layer
	    this.siteArray.clearLayers();
	    this.cur_site = results;
	    this.cur_site.addTo(this.map);
	    this.cur_name = 'Custom';
	    this.cur_fwd = this.cur_site.fwd;
	    this.updateOrigin(results.data['latitude'], results.data['longitude'])
	    this.custom = true;
	    this.update_info();
	}.bind(this));
    } else {
	// in case it's not currently displayed
	this.siteArray.addTo(this.map);
	this.cur_name = name;
	this.cur_fwd = fwd;
	this.cur_date = date;
	// let the siteArray do the switching
	var vals = [name, fwd, date];
	return this.siteArray.switchToValue(vals).done(function() {
	    this.cur_site = this.siteArray.cache[this.siteArray.valToArrayInd(vals)];
	    this.update_info();
	    this.updateOrigin([this.cur_site.data['latitude'],
			      this.cur_site.data['longitude']])
	}.bind(this));
    }
}

Hysplit.prototype.switchSite = function(stid) {
    this.changeSite(stid, this.cur_fwd, this.cur_date);
}

Hysplit.prototype.changeFwd = function changeFwd(fwd) {
    var new_fwd = fwd || !this.cur_fwd;
    this.changeSite(this.cur_name, new_fwd, this.cur_date);
}

Hysplit.prototype.changeDate = function changeDate(date) {
    this.changeSite(this.cur_name, this.cur_fwd, date)
}

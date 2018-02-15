//JS file 
var newDateRange = {
    locale: {
	format: 'MM/DD/YYYY'
    }
};
var vars = {
    FC_mass: 'FC_mass',
    LE: 'LE',
    H: 'H',
    Rn: 'Rn',
    TAU: 'TAU',
    Bowen_ratio: 'Bowen_ratio',
    USTAR: 'USTAR',
    TKE: 'TKE',
    ZL: 'ZL',
    MO_LENGTH: 'MO_LENGTH',
    U: 'U',
    V: 'V',
    W: 'W',
    T_SONIC: 'T_SONIC',
    CO2: 'CO2',
    H2O: 'H2O',
    SW_IN: 'SW_IN',
    SW_OUT: 'SW_OUT',
    LW_IN: 'LW_IN',
    LW_OUT: 'LW_OUT',
    G_6cm: 'G_6cm'
};

//change the actual units 
var units = {
    FC_mass: 'mg m-2s-1',
    LE: 'W m-2',
    H: 'W m-2',
    Rn: 'W m-2',
    TAU: 'kg m-1 s-2',
    Bowen_ratio: '',
    USTAR: 'm s-1',
    TKE: 'm2 s-2',
    ZL: '',
    MO_LENGTH: '',
    U: 'm s-1',
    V: 'm s-1',
    W: 'm s-1',
    T_SONIC: '°C',
    CO2: 'μmolCO2 mol-1 (ppm)',
    H2O: 'mmolCO2 mol-1',
    SW_IN: 'W m-2',
    SW_OUT: 'W m-2',
    LW_IN: 'W m-2',
    LW_OUT: 'W m-2',
    G_6cm: 'W m-2'
};



var loc = {
    BELL:[ 43.78962,-76.11373 ],
    BKLN:[ 40.631762,-73.953678 ],
    BURT:[ 43.31699,-78.74903 ],
    CHAZ:[ 44.89565,-73.46461 ],
    FRED:[ 42.41817,-79.3666 ],
    ONTA:[ 43.25941,-77.37331 ],
    OWEG:[ 42.02571,-76.25543 ],
    PENN:[ 42.65578,-76.98746 ],
    QUEE:[ 40.734335,-73.815856 ],
    REDF:[ 43.62218,-75.87769 ],
    REDH:[ 42.00168,-73.88391 ],
    SCHU:[ 43.116996,-73.578284 ],
    SOUT:[ 41.040081,-72.465864 ],
    STAT:[ 40.604014,-74.148499 ],
    VOOR:[ 42.65242,-73.97562 ],
    WARS:[ 42.77993,-78.20889 ],
    WHIT:[ 43.485073,-73.423071 ]
    
}

var sitesNew2 = {

    BELL:'BELL',
    BKLN:'BKLN',
    BURT:'BURT',
    CHAZ:'CHAZ',
    FRED:'FRED',
    ONTA:'ONTA',
    OWEG:'OWEG',
    PENN:'PENN',
    QUEE:'QUEE',
    REDF:'REDF',
    REDH:'REDH',
    SCHU:'SCHU',
    SOUT:'SOUT',
    STAT:'STAT',
    VOOR:'VOOR',
    WARS:'WARS',
    WHIT:'WHIT'
    
}
var map_options = {zoomControl: false,
		   maxZoom: 16};
var marker_options = {radius: 6, color: 'blue', weight: 0,
		      opacity: .8, fillOpacity: .8};
var selected_marker_options = {color: 'orange'};
/* creating the form */
$(document).ready(function() {
    $("#form").alpaca({
	schema: {
            title: " ",
            type: "object",
            properties: {
		daterange: {
		    title: 'Time range (UTC)',
		    type: 'string'
		},
		variables: {
                    type: 'string',
                    title: 'Parameters:'
		    //default: 'CO2'
		},
		sitesNew2: {
                    type: 'string',
                    title: 'Select Site'
		},
		// sites: {
                //     type: 'string',
                //     title: 'Sites'
		// },
            }
	},
	options: {
	    focus: false,
	    form: {
		attributes: {
                    action: 'javascript:sendDate();'
		},
		buttons:{
                    submit: {
			title: 'View Data'
		    },
		    reset: {
			click: function(){
			    //console.log(this)
			    var form = $('#form').alpaca('get');
			    
			    var sitesNew3 = form.childrenByPropertyId['sitesNew2'];
			    sitesNew3.setValue([]);
			    sitesNew3.getControlEl().multiselect('refresh');

			    var vars = form.childrenByPropertyId['variables'];
			    vars.setValue([]);
			    vars.control.multiselect('refresh');
			    $('#parent').empty();
			    $("html").removeClass("waiting");
			    
			}
		    }
		}
            },
            fields: {
		daterange: {
		    placeholder: 'Please select a date range',
		    type: 'daterange',
		    
		    picker: newDateRange
		},
		
		variables: {
                    type: 'select',
		    dataSource: vars,
		    multiple: true,
		    multiselect: {includeSelectAllOption: true},
		    removeDefaultNone: true,
		    sort: false,
		    
		},
		sitesNew2: {
                    type: "leaflet-select",
		    multiple: true,
		    removeDefaultNone: true,
		    multiselect: {includeSelectAllOption: true},
		    dataSource: sitesNew2,
		    locations: loc,
		    marker: marker_options,
		    selectedMarker: selected_marker_options,
		    helper: "<a href=\"http://pireds.asrc.cestm.albany.edu/~xcite/fluxV3/helper.html\" target=\"_blank\">Reference Page</a>"
		},

		// sitesNew2: {
                //     type: "leaflet-select",
		//     removeDefaultNone: true,
		//     multiple: true,
		//     map_options: map_options,
		//     /* markerFunction: L.marker,*/
		//     marker: marker_options,
		//     selectedMarker: selected_marker_options,
		//     /* hideSelect: true*/
		// }
            }
	},
	view: {
	    parent: "bootstrap-edit-extra",
	    "layout": {
		"template": '#moveBut2',
		"bindings": {
		    "daterange": "#left",
                    "variables": "#left",
		    "sitesNew2": "#left",
                    
		},
		templates:{
		    form: '#moveBut'
		}
            }
	    
	},
    })
});


/* Highcharts.setOptions({
 *     global : {
 *         useUTC : false
 *     }
 * });*/


var base_url = 'http://pireds.asrc.cestm.albany.edu:9097/';
var datepicker = $('#datepicker');
var datepicker2 = $('#datepicker2');
//for spinner
var respNum=0;
var spin = 0;

date_options = {dateFormat: 'yy/mm/dd'};

//datepicker.datepicker(date_options);
//datepicker2.datepicker(date_options);

function dateFun(){
    var x = document.getElementById("date").action;
    document.getElementById("date").innerHTML = x;

    var x = document.getElementById("date").action;
    document.getElementById("date").innerHTML = x;
    //formObject.action = dateURL;
}

function getDate(){
    // minDate = datepicker[0].value;
}

//testing
// Listen for click on toggle checkbox
$('#select-all').click(function(event) {   
    if(this.checked) {
	// Iterate each checkbox
	$(':checkbox').each(function() {
	    this.checked = false;
	    //$('span[title="' + title + '"]').remove();
	    //var ret = $(".hida");
	    //$('.dropdown dt a').append(ret);
	    $('.multiSel').text("");
	    //document.getElementById("myForm").reset();
	    $('#parent').empty();
	});
    }
});

var visible1 = false;
$("#d1 dt a").on('click', function() {
    $("#d1 dd ul").slideToggle('fast');
    visible1 = true;
});

//make dropdown go away if clicked anywhere on page
//id="ul_top_hypers"
$("html").click(function(event){ 
    if (visible1 && (event.target.id == "date" || event.target.id == "parent")) {
	$("#d1 dd ul").hide();
    }
});


function getSelectedValue(id) {
    return $("#" + id).find("dt a span.value").html();
};

$(document).bind('click', function(e) {
    var $clicked = $(e.target);
    if (!$clicked.parents().has("d1")) $(".dropdown dd ul").hide();
});

$('.mutliSelect input[type="checkbox"]').on('click', function() {

    var title = $(this).closest('.mutliSelect').find('input[type="checkbox"]').val(),
	title = $(this).val() + ",";

    if ($(this).is(':checked')) {
	var html = '<span title="' + title + '">' + title + '</span>';
	$('.multiSel').append(html);
	$(".hida").hide();
    } else {
	$('span[title="' + title + '"]').remove();
	var ret = $(".hida");
	$('.dropdown dt a').append(ret);

    }

    
    
});

//end testing

//dropdown 2
// Listen for click on toggle checkbox
$('#select-all2').click(function(event) {   
    if(this.checked) {
	// Iterate each checkbox
	$(':checkbox').each(function() {
	    this.checked = false;
	    //$('span[title="' + title + '"]').remove();
	    //var ret = $(".hida2");
	    //$('.dropdown dt a').append(ret);
	    $('.multiSel2').text("");
	    //document.getElementById("myForm").reset();
	    $('#parent').empty();
	});
    }
});

var visible = false;
$("#d2 dt a").on('click', function() {
    $("#d2 dd ul").slideToggle('fast');
    visible = true;
});


//make dropdown go away if clicked anywhere on page
$("body").mouseup(function(event){ 
    if (visible && event.target.id == "date" ) {
	$("#d2 dd ul").hide();
    }
});

function getSelectedValue(id) {
    return $("#" + id).find("dt a span.value").html();
};

$(document).bind('click', function(e) {
    var $clicked = $(e.target);
    if (!$clicked.parents().has("#d2")) $(".dropdown dd ul").hide();
});

$('.mutliSelect2 input[type="checkbox"]').on('click', function() {

    var title = $(this).closest('.mutliSelect2').find('input[type="checkbox"]').val(),
	title = $(this).val() + ",";

    if ($(this).is(':checked')) {
	var html = '<span title="' + title + '">' + title + '</span>';
	$('.multiSel2').append(html);
	$(".hida2").hide();
    } else {
	$('span[title="' + title + '"]').remove();
	var ret = $(".hida2");
	$('#d2 dt a').append(ret);

    }

    
});

//dropdown 2 end

function sendDate(){
    //waiting spinner while data loads for curser
    $('#parent').empty();
    $("html").addClass("waiting");
    respNum = 0;
    
    var form = $('#form').alpaca('get');
    var datepicker = form.childrenByPropertyId['daterange'].control.data('daterangepicker');
    //var datepicker2 = $('#datepicker2');
    
    curDateF = datepicker.startDate.format('YYYY/MM/DD');
    //curDateF = datepicker[0].value;
    lastDate = datepicker.endDate.format('YYYY/MM/DD');
    //maxDate = datepicker2[0].value;
    
    //var sites = document.getElementById('ul_top_hypers');
    //var sitesStr = sites.options[sites.selectedIndex].text;
    //for the sites
    var sites = document.getElementsByClassName("multiSel");
    console.log(sites);

    var objectHTMLCollection = document.getElementsByClassName("multiSel"),
	string = [].map.call( objectHTMLCollection, function(node){
	    return node.textContent || node.innerText || "";
	}).join("");

    console.log(string);
    console.log(objectHTMLCollection);

    //for the parameters
    var pars = document.getElementsByClassName("multiSel2");
    console.log(sites);

    var objectHTMLCollection2 = document.getElementsByClassName("multiSel2"),
	string2 = [].map.call( objectHTMLCollection2, function(node){
	    return node.textContent || node.innerText || "";
	}).join("");

    console.log(string2);
    console.log(objectHTMLCollection2);

    //var sitesStr = sites.options[sites.selectedIndex].text;

    //console.log(sitesStr);

    var div = document.createElement('div')
    k=0

    var unit;
    var sites = form.childrenByPropertyId['sitesNew2'].getValue();
    var vars = form.childrenByPropertyId['variables'].getValue();
    for (var site of sites){
	//test = item.innerText.split(",");
	//len = item.childNodes.length;
	for(var par of vars){
	    
	    dateURL = base_url + 'plot?dates=' + curDateF + '&dates=' + lastDate + '&site=' + site + '&par='+par;
	    
	    $('#parent').append('<div id="first'+k+'"></div>');

	    
	    id = "first"+k;
	    console.log(id);
	    unit = units[par]
	    graphing(dateURL, id, site, par,unit);
	    k+=1
	    
	    console.log("current unit is "+unit);
	}
	spin = sites.length * vars.length;
	/* if(spin == k){
	   $("html").removeClass("waiting");
	   }*/
    }    

    
}

//$("html").removeClass("waiting");
//function for making multiple graphs
function graphing(dateURL, id, site, par,unit){

    

    $.ajax({
	method: "GET",
	url: dateURL,
    }).done(function( response ) {

	//getMaxMin(dateURL, response, id, site, par, unit)

	//plotly
	graph = response["data"];
	layout = response["layout"];
	console.log(id);
	console.log(response);

	respNum+=1;
    //var datepicker2 = $('#datepicker2');
    console.log("numSpings "+spin);
    console.log("respNum"+respNum);
    
    if (respNum == spin){
	$("html").removeClass("waiting");
    }
        //var ids = id;
        // for(var i in graphs) {
            Plotly.newPlot(id, // the ID of the div, created above
                           [graph],
			   layout,
			  );
        // }
	
	
	//$('#csv').text(response);
	//response has json code
	//heatMap(response, id, site, par);
    })
	.fail(function(jqXHR){
	    if(jqXHR.status==500 || jqXHR.status==0){
		$('#errorDiv').text("DATE OUT OF RANGE!!!").delay(2000).fadeOut();
		// internal server error or internet connection broke
		alert("NOTE: You selected a date thats out of range for site: " + site+"! Please try again!");
		//heatMap(response, id, site, par);
		//get ride of spinner
		$("html").removeClass("waiting");
		
	    }

	});
    
};

function getMaxMin(dateURL, response, id, site, par, unit){
    //response = document.getElementById('csv').innerHTML
    d3.csv(dateURL, function (data) {
	console.log(data)

	data.forEach(function(d) {
	    d.Temperature = +d.Temperature;
	});

	var max = d3.max(data, function(d) { return d.Temperature; });
	console.log("maxNew is "+ max)

	var min = d3.min(data, function(d) { return d.Temperature; });
	console.log("minNew is "+ min)

	$('#csv').text(response);
	//response has json code
	heatMap(response, id, site, par, max, min, unit);
    })
}



function heatMap(response, id, site, par, max, min, unit){
    //var datepicker = $('#newDateRange').data('daterangepicker');

    respNum+=1;
    //var datepicker2 = $('#datepicker2');
    console.log("numSpings "+spin);
    console.log("respNum"+respNum);
    
    if (respNum == spin){
	$("html").removeClass("waiting");
    }

    
    var form = $('#form').alpaca('get');
    var datepicker = form.childrenByPropertyId['daterange'].control.data('daterangepicker');

    
    curDateF = datepicker.startDate.toDate();
    //curDateF = datepicker[0].value;
    lastDate = datepicker.endDate.toDate();
    
    //heatmap stuff below
    Highcharts.chart(id, {

	global: {
	    useUTC: false
	},
	
	data: {
	    csv: document.getElementById('csv').innerHTML
	    //csv: '/home/xcite/flux/myData.csv'
	},

	chart: {
	    type: 'heatmap',
	    //margin: [60, 10, 80, 50] //[60, 10, 80, 50]
	},
	//rowsize: .5,

	boost: {
	    useGPUTranslations: true
	},

	title: {
	    text: 'Highcharts heat map for site '+site+' showing '+par+' '+ unit+' data',
	    align: 'left',
	    x: 40
	},

	subtitle: {
	    text: par+'  variation by day and half hour for '+ site + ' on selected date range above',
	    align: 'left',
	    x: 40
	},


	//	 var minDate = getDate();
	xAxis: {
	    type: 'datetime',
	    //tickPixelInterval: 1,
	    //   min: Date.UTC(2017, 09, 01),
	    /* min: (new Date(minYY, minMM-1, minDD)).getTime(),
	       max: (new Date(maxYY, maxMM-1, maxDD)).getTime(),*/

	    min: curDateF.getTime(),
	    max: lastDate.getTime(),

	    
	    
	    labels: {
		//align: 'center',
		//x: 00,
		//y: 25,
		//format: '{value:%e}' // long month
	    },
	    showLastLabel: false, //changed from false
	    tickLength: 16
	},

	yAxis: {
	    title: {
		text: null
	    },
	    labels: {
		format: '{value}:00'
	    },
	    minPadding: 0,
	    maxPadding: 0,
	    startOnTick: false,
	    endOnTick: false,
	    tickPositions: [0, 6, 12, 18, 24], //[0, 6, 12, 18, 24]
	    tickWidth: 0.5,
	    
	    min: 0,
	    max: 24, //from 23
	    reversed: false
	},

	colorAxis: {
	    stops: [
		[0, '#3060cf'],
		//[0.25, '#99ffbb'],
		[0.5, '#fffbbc'],
		[0.8, '#c4463a'],
		[1, '#c4463a']
	    ],
	    min: min,//Math.min('{value}'),
	    max: max,//Math.max('{value}'),
	    startOnTick: true,
	    endOnTick: true, //cahnged from false false
	    labels: {
		
		format: '{value} '
	    }
	},

	series: [{
	    boostThreshold: 100,
	    borderWidth: 0,
	    nullColor: '#EFEFEF',
	    //data:
	    //[ [0.0.-0.7] ] day hour co2 
	    colsize: 24 * 36e5, // one day
	    rowsize: 0.5,
	    //find out what point is below ex point.x
	    tooltip: {
		headerFormat: par+' Data<br/>',
		//day month, year then time in 24 hours then temp in deg C
		pointFormat: '{point.x:%e %b, %Y} {point.y}:00: <b>{point.value} </b>'+unit
	    },
	    turboThreshold: 0//Number.MAX_VALUE // #3404, remove after 4.0.5 release
	}]

	
    });

}

//Highcharts.setOptions({ global: { useUTC: false } });


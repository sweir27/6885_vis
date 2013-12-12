$(function() {
// var map = L.map('map').setView([30, 0], 2);



$.get("/api/get_me_the_locations/", function(data) {
    // sample_data = data
    // console.log(data)
    heatmap_locations(data)
}).done(function() {
    // console.log('success!')
});

});

function heatmap_locations(testData) {
    var baseLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 18
    });

    window.heatmapLayer = L.TileLayer.heatMap({
        radius: 5,
        opacity: 0.8,
        gradient: {
            0.45: "rgb(0,0,255)",
            0.55: "rgb(0,255,255)",
            0.65: "rgb(0,255,0)",
            0.95: "yellow",
            1.0: "rgb(255,0,0)"
        }
    });

    window.heatmapLayer.addData(testData.data);

    map = new L.Map('map', {
        center: new L.LatLng(30, 0),
        zoom: 2,
        layers: [baseLayer, window.heatmapLayer]
    });

    // make accessible for debugging
    layer = window.heatmapLayer;
}

function update_heatmap(testData) {
    // var baseLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    //     maxZoom: 18
    // });

    window.map.removeLayer(window.heatmapLayer)

    window.heatmapLayer = L.TileLayer.heatMap({
        radius: 5,
        opacity: 0.8,
        gradient: {
            0.45: "rgb(0,0,255)",
            0.55: "rgb(0,255,255)",
            0.65: "rgb(0,255,0)",
            0.95: "yellow",
            1.0: "rgb(255,0,0)"
        }
    });

    window.heatmapLayer.addData(testData.data);

    window.map.addLayer(window.heatmapLayer)

    // var map = new L.Map('map', {
    //     center: new L.LatLng(30, 0),
    //     zoom: 2,
    //     layers: [baseLayer, newHeatmapLayer]
    // });

    // make accessible for debugging
    // layer = heatmapLayer;
}

var bleep={
            max: 46,
            data: [
                {lat: 33.5363, lon:-117.044, value: 1},
                {lat: 33.5608, lon:-117.24, value: 1},
                {lat: 42, lon:-71, value: .2},
                {lat: 44, lon:-63, value: .4},
                {lat: 32, lon:34, value: .7},
                {lat: 49, lon:-119, value: .8},
                {lat: 59, lon:10, value: .1},
                {lat: -14, lon:75, value: .6}
            ]
        };
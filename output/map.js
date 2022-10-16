
function init(){

	const map = L.map('map').setView([51.505, -0.09], 13);
	L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	const polylines = lines.map(function (line) {
		const color = (line[1]['colour'] != undefined) ? line[1]['colour'] : '#999999';
		const points = line[2].map(function (point) {
			return new L.LatLng(point[2][1], point[2][0]);
		});
		return new L.Polyline(points, {
			color: color,
			weight: 4,
			opacity: 0.7,
			smoothFactor: 1,
		});
	});

	const features = L.featureGroup(polylines);
	features.addTo(map);
	map.fitBounds(features.getBounds())
}

$(document).ready(init);

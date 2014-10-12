#!/usr/bin/env python
# coding: utf-8


class GoogleHeatMap(object):

	def __init__(self, data):
		self.data = data


	def make_data(self):
		n = len(self.data)
		self.s = '[\n'
		for i, row in enumerate(self.data):
			self.s += '{location: new google.maps.LatLng(%s, %s), weight: %s},\n' % (row[0], row[1], row[2])
			if i == n-1:
				self.s += '{location: new google.maps.LatLng(%s, %s), weight: %s}\n];' % (row[0], row[1], row[2])
		return self.s


	def make_js(self):

		self.js = """
	<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>
	<script>
	  var map, pointarray, heatmap;

	  var myData = %s

	  function initialize() {
	    var mapOptions = {
	      zoom: 10,
	      center: new google.maps.LatLng(35.70, 139.60),
	      mapTypeId: google.maps.MapTypeId.SATELLITE
	    };

	    map = new google.maps.Map(document.getElementById('map-canvas'),
	     mapOptions);

	    var pointArray = new google.maps.MVCArray(myData);

	   	heatmap = new google.maps.visualization.HeatmapLayer({
	      data: pointArray,
	      dissipating: false,
	      radius: 1
	    });

	    heatmap.setMap(map);
	  }

	  function toggleHeatmap() {
	    heatmap.setMap(heatmap.getMap() ? null : map);
	  }

	  function changeGradient() {
	    var gradient = [
	      'rgba(0, 255, 255, 0)',
	      'rgba(0, 255, 255, 1)',
	      'rgba(0, 191, 255, 1)',
	      'rgba(0, 127, 255, 1)',
	      'rgba(0, 63, 255, 1)',
	      'rgba(0, 0, 255, 1)',
	      'rgba(0, 0, 223, 1)',
	      'rgba(0, 0, 191, 1)',
	      'rgba(0, 0, 159, 1)',
	      'rgba(0, 0, 127, 1)',
	      'rgba(63, 0, 91, 1)',
	      'rgba(127, 0, 63, 1)',
	      'rgba(191, 0, 31, 1)',
	      'rgba(255, 0, 0, 1)'
	    ]
	    heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
	  }

	  function changeRadius() {
	    heatmap.set('radius', heatmap.get('radius') ? null : 3);
	  }

	  function changeOpacity() {
	    heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
	  }

	  google.maps.event.addDomListener(window, 'load', initialize);
	</script>

		""" % self.make_data()

		return self.js


	def show_html(self):

			self.html = """
		<!DOCTYPE html>
		<html>
		  <head>
		    <meta charset="utf-8">
		    <title>Heatmaps</title>
		    <style>
		      html, body, #map-canvas {
		        height: %s;
		        margin: 0px;
		        padding: 0px
		      }
		      #panel {
		        position: absolute;
		        top: 5px;
		        left: %s;
		        margin-left: -180px;
		        z-index: 5;
		        background-color: #fff;
		        padding: 5px;
		        border: 1px solid #999;
		      }
		    </style>

		    %s

		  </head>

		  <body>
		    <div id="panel">
		      <button onclick="toggleHeatmap()">Toggle Heatmap</button>
		      <button onclick="changeGradient()">Change gradient</button>
		      <button onclick="changeRadius()">Change radius</button>
		      <button onclick="changeOpacity()">Change opacity</button>
		    </div>
		    <div id="map-canvas"></div>
		  </body>
		</html>
			""" % ("100%", "50%", self.make_js())

			return self.html


if __name__ == '__main__':

	import csv

	data = []
	with open("data.csv", "rU") as f:
		reader = csv.reader(f)
		for row in reader:
			data.append([row[0], row[1], row[2]])

	g = GoogleHeatMap(data)

	open('heatmap.html', 'wb').write(g.show_html())
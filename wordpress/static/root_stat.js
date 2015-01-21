function sites () {
	$("#sites-container").toggle();
}

function site_tree() {
	$("#site-tree").toggle();
}

function site_bubble() {
	$("#site-bubble").toggle();
}

function tree_visual (data) {
	d3.select("#site-tree")
			.style("height", "600px");

	var canvas = 
	d3.select("#site-tree")
		.append("svg")
			.attr("id", "tree-visual")
			.attr("width", $("#site-tree").innerWidth())
			.attr("height", $("#site-tree").innerHeight())
		.append("g")
			.attr("id", "tree-container");
			
	var tree = 
		d3.layout.tree()
			.size( [$("#site-tree").innerWidth()*0.9, 400] );

	var nodes = tree.nodes(data);
	var links = tree.links(nodes);

	var tooltip = d3.select("#site-tree").append("div").attr("id", "tooltip").style("opacity", 0);

	var node = 
	canvas.selectAll("nodes")
		.data(nodes)
		.enter()
		.append("g")
			.attr("class", "node")
			.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")"; })
			.on("mouseover", function(d) {
				tooltip.transition()
					.duration(100)
					.style("opacity", 0.9);
				tooltip.html(d.title+".<br/>"+d.subtitle+".<br/>Published : "+d.published.slice(0, 10))
					.style("left", d3.event.pageX+"px")
					.style("top", d3.event.pageY+"px");
			})
			.on("mouseout", function(d) {
				tooltip.transition()
					.duration(100)
					.style("opacity", 0);
			})
			.on("dblclick", function(d){
				window.location.href="/wordpress/stats?url="+d.url+"&level="+d.level;
			});

	node.append("circle")
			.attr("r", 10)
			.attr("fill", "steelblue");

	canvas.attr("transform", "translate( 0, 50)");

	var diagonal = d3.svg.diagonal();

	canvas.selectAll(".link")
		.data(links)
		.enter()
		.append("path")
			.attr("class", "link")
			.attr("fill", "none")
			.attr("stroke", "red")
			.attr("d", diagonal);
}

function bubble_visual (root) {

	var margin = 20,
	    diameter = 1000;

   var tooltip = d3.select("#site-bubble").append("div").attr("id", "tooltip").style("opacity", 0);

	var color = d3.scale.linear()
	    .domain([-1, 5])
	    .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
	    .interpolate(d3.interpolateHcl);

	var pack = d3.layout.pack()
	    .padding(2)
	    .size([diameter - margin, diameter - margin])
	    .value(function(d) { return 1; })

	var svg = d3.select("#site-bubble").append("svg")
	    .attr("width", diameter)
	    .attr("height", diameter)
	  .append("g")
	    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");


	var focus = root,
	  nodes = pack.nodes(root),
	  view;

	var circle = svg.selectAll("circle")
	  .data(nodes)
	.enter().append("circle")
	  .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
	  .style("fill", function(d) { return d.children ? color(d.depth) : null; })
	  .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); })
	  .on("mouseover", function(d) {
				tooltip.transition()
					.duration(100)
					.style("opacity", 0.9);
				tooltip.html(d.title+".<br/>"+d.subtitle+".<br/>Published : "+d.published.slice(0, 10))
					.style("left", d3.event.pageX+"px")
					.style("top", d3.event.pageY+"px");
			})
			.on("mouseout", function(d) {
				tooltip.transition()
					.duration(100)
					.style("opacity", 0);
			})
			.on("dblclick", function(d){
				window.location.href="/wordpress/stats?url="+d.url+"&level="+d.level;
			});

	var text = svg.selectAll("text")
	  .data(nodes)
	.enter().append("text")
	  .attr("class", "label")
	  .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
	  .style("display", function(d) { return d.parent === root ? null : "none"; })
	  .text(function(d) { return d.level === "page" ? d.title : ""; });

	var node = svg.selectAll("circle,text");

	  d3.select("#site-bubble")
	      .style("background", color(-1))
	      .on("click", function() { zoom(root); });

	  zoomTo([root.x, root.y, root.r * 2 + margin]);

	  function zoom(d) {
	    var focus0 = focus; focus = d;

	    var transition = d3.transition()
	        .duration(d3.event.altKey ? 7500 : 750)
	        .tween("zoom", function(d) {
	          var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
	          return function(t) { zoomTo(i(t)); };
	        });

	    transition.selectAll("text")
	      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
	        .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
	        .each("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
	        .each("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
	  }

	  function zoomTo(v) {
	    var k = diameter / v[2]; view = v;
	    node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
	    circle.attr("r", function(d) { return d.r * k; });
	  }

	d3.select(self.frameElement).style("height", diameter + "px");
}
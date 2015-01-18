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

	var tooltip = d3.select("#site-tree").append("div").attr("id", "tree-tooltip").style("opacity", 0);

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
				tooltip.html(d.title+"<br>Published : "+d.published.slice(0, 10))
					.style("left", d3.event.pageX+"px")
					.style("top", d3.event.pageY+"px");
			})
			.on("mouseout", function(d) {
				tooltip.transition()
					.duration(100)
					.style("opacity", 0);
			})
			.on("dblclick", function(d){
				window.location.href="/wordpress/stats?url="+d.url+"&level=page";
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

function posts() {
	if (document.getElementById("post-container").style.display == "block"){
		document.getElementById("post-container").style.display = "none";
	}
	else {
		document.getElementById("post-container").style.display = "block";
	}
}

function site_tree() {
	if (document.getElementById("site-tree").style.display == "block"){
		d3.select("#site-tree").style("display", "none");
	}
	else {
		d3.select("#site-tree").style("display", "block");
	}
}
define([
	"d3.js",
	"CompressedGraph.js",
	"d3-context-menu.js",
	"Simulation.js"
	],
function(d3,CGraph,d3ContextMenu,Simu){
	"use strict";
return function GraphModel(ct,fr){
	var graph_obj,
        json,
		svg,
		svg_content,
		transform,
		zoom,
		width,
		height,
		node_base_radius = 50,
		simulation,
		tr_duration = 2250,
		__forceLayout = "FORCE_LAYOUT",
		old_scale = null;
	//init the graph UI
	(function _init(ct,fr){
		var size = initPageLayout(ct,fr);//add page dom structure
		initSvg(size);//init spv container
		initForceLayout();//init force layout
		initTopMenu();//add top menu
		initSideMenu();//add side menu
	}(ct));
	/* add the full page dom to the defined container
	 * @input ct : the dom element root
	 * @return : the page size.
	 */
	function initPageLayout(ct,file_reader){
		d3.select((ct!="body"?"#":"")+ct).on('keydown',keyHandler)
			.append("div").attr("id","main_container");//page main container
		var main_ct = d3.select("#main_container");
		if(ct=="body")main_ct.style("width","100vw").style("height","100vh");
		else{
			var size = d3.select("#"+ct).node().getBoundingClientRect();
			main_ct.style("width","100% !important").style("height","100% !important");
		}
		main_ct.style("min-width","100%").style("min-height","100%");
		main_ct.append("div").attr("id", "top_chart");//top menu
		main_ct.append("div").attr("id","bottom_top_chart");//separator between menu and page core
		var container = main_ct.append("div").attr("id", "container");//page core
		var slide_menu = container.append("div").attr("id","side_menu");//main div of side menu
		slide_menu.append("div")
			.attr("id","side_content");
		slide_menu.append("div")//add a close button
			.classed("close_side_menu",true)
			.on("click",tabMenuOpCl)
			.html("&#x25c0;")
			.classed("unselectable",true);	
		var sliding_frame = container.append("div").attr("id", "sliding_frame");//main div of graph
		sliding_frame.append("div").attr("id","drag_bar_cont")//add the vertical separator container
			.append("div").attr("id","drag_bar").on("click",tabMenuOpCl);//add a drag bar for the menu
		var graph_frame = sliding_frame.append("div").attr("id", "graph_frame");//SVG container
		d3.select("body").append("div")//add the description tooltip
			.attr("id","__tooltip")
			.classed("__tt_bottom",true)
			.classed("__tt_left",true);
		tt_hide();
		return graph_frame.node().getBoundingClientRect();
	}
	function tt_show(d){
		let main_c = d3.select("#__tooltip");
		let contain = d3.select("body");
		let content = {title:d.id,content:{}};
		//console.log(d);
		if(d.children && d.children.length>0) content.content["children"]= d.children.map(e => e.id);
		if(d._children && d._children.length>0)content.content["children"]=d._children.map(e => e.id);
		if(graph_obj.getNAtt(d.id)){
			graph_obj.getNAtt(d.id).forEach(e => content.content[e]=graph_obj.getNAtt(d.id,e));
		}
			let ct = "<b><h3><center>"+content.title+"</center></b></h3>";
			let lst = Object.keys(content.content);
			lst.forEach(function(e){
				ct+="<b>"+e+" : </b>";
				if(content.content[e] && content.content[e].length>0){
					ct+="<ul>";
					content.content[e].forEach(function(v){ct+="<li>"+v+"</li>"});
					ct+="</ul>";
				}
			});
			main_c.style("display","initial").html(ct);
		}
		function tt_hide(){
			let main_c = d3.select("#__tooltip");
			main_c.style("display","none");
		}
	
	
	
	
	
	/* open and close side menu.
	 * switch function.
	 */
	function tabMenuOpCl(){
		var side = d3.select("#side_menu"),
			size = side.style("width") != "0px" ? "0px" : "15.6%";
		side.style("min-width", size);
		d3.select("#sliding_frame").style("margin-left", size);
		side.style("width", size);
		var sz = d3.select("body").node().getBoundingClientRect().width;
		if(size != "0px") sz-=(sz*15.6)/100;
		svg.attr("width", sz);
		updateScale();
	}
	/* handle all key event on the page */
	function keyHandler(){
		switch(d3.event.key){
			case 'w':
				var ref=d3.select("#top_chart");
				ref.style("display",function(){ return ref.style("display")!="none"?"none":null});
				d3.select("#bottom_top_chart").style("display",function(){ return ref.style("display")});
				if(ref.style("display")=="none"){
					d3.select("#sliding_frame").style("margin-left", "0px");
					d3.select("#side_menu").style("min-width", "0px").style("width","0px");
					
					d3.select("#container").style("height","100%");
				}else{
					d3.select("#container").style("height","95%");
				}
				d3.select("#drag_bar_cont").style("display",function(){ return ref.style("display")});
				var size = d3.select("#graph_frame").node().getBoundingClientRect();
					svg.attr("width", size.width);
					svg.attr("height",size.height);
				updateScale();
			break;
			case 's':
				if(simulation.alpha()!=0){
					endForce();
					svg.selectAll("g.node").each(function(d){d.vx=0;d.vy=0;d.fx=d.x;d.fy=d.y});
				}
				else{
					var sl = d3.select("#lyt_select"),
						si,s;
					if(sl.size()>0){
						si = sl.property("selectedIndex");
						s = d3.select("#lyt_select").selectAll("option").filter(function (d, i) { return i === si }).datum();
						if(s==__forceLayout)
							svg.selectAll("g.node").each(function(d){d.fx=null;d.fy=null});
					}else{
						svg.selectAll("g.node").each(function(d){d.fx=null;d.fy=null});
					}
					reload_force();
				} 
			case 'c':
				updateScale();
		}
	}
	/* handle all zoom event on the svg */
	function zoomHandler(){
		svg_content.attr("transform", d3.event.transform);
	}
	/* init the svg content
	 * @input size : the svg size
	 * init markers for edges
	 * init context menu event
	 * show 3dsx logo
	 * define initial zoom.
	 */
	function initSvg(size){	
		height = size.height;
		width = size.width;
		svg = d3.select(graph_frame).append("svg:svg")
			.attr("id", "graph_view")
			.attr("height", height)
			.attr("width", width);
		transform = d3.zoomIdentity;
		svg_content = svg.append("g").classed("svg_zoom_content",true);//the internal zoom and drag object for svg
		zoom = d3.zoom()
			//.scaleExtent([0.02, 1.1])
			.on("zoom", zoomHandler);
		zoom.filter(function(){ return !d3.event.button && !d3.event.shiftKey});		
		svg.classed("svg-content-responsive", true);
			svg.append("svg:defs").selectAll("marker")
			.data(["arrow_end"])      // Different link/path types can be defined here
			.enter().append("svg:marker")    // This section adds the arrows
			.attr("id", function(d){return d;})
			.attr("refX", 0)
			.attr("refY", 3)
			.attr("markerWidth", 10)
			.attr("markerHeight", 10)
			.attr("orient", "auto")
			.attr("markerUnits","strokeWidth")
			//.attr("position","80%")
			.append("svg:path")
			.attr("d","M0,0 L0,6 L9,3 z");
		svg.on("contextmenu",d3ContextMenu(function(){return svgMenu();}));//add context menu
		svg.call(zoom);
        svg.call(d3.drag().on("drag", dragHandler).on("end", selectionHandlerEnd).on("start",selectionHandlerStart));
		svg.on("click",svgClickHandler);
		svg_content.append("svg:image")
			.attr("width",800)
			.attr("height",800)
			.attr("x",function(){return size.width/2-400})
			.attr("y",function(){return size.height/2-400})
			.attr("xlink:href","logo.png");
	}
	function svgMenu(){}
	function dragHandler(){}
	function selectionHandlerEnd(){}
	function selectionHandlerStart(){}
	function svgClickHandler(){
		
	}
	function initForceLayout(){
		simulation = d3.forceSimulation()
			.force("link", d3.forceLink()
							.id(function(d) {return d})
							.strength(function(d){
								return 1;
							})
							.distance(function(d){
								return 5;
							}))
			.force("charge", d3.forceManyBody()
								.distanceMax(node_base_radius*30)
								.strength(-500)
								.distanceMin(node_base_radius/10))
			.force("center", d3.forceCenter(width / 2, height / 2))
			.force("collision",d3.forceCollide(node_base_radius+10));
		simulation.on("tick",move);//this function is called on each tick function
		simulation.on("end",forceSave);
		simulation.stop().alpha(0);//stop the simulation until we want to start it.
	}
	function endForce(){
		simulation.stop().alpha(0);
		forceSave();
	}
	function forceSave(){
		console.log("simulation ended");
		updateScale();
		svg_content.selectAll("g.node").each(function(d){d.ox=d.x;d.oy=d.y});
		old_scale=scaleCalc();
	}
	function initTopMenu(){
		var top_menu = d3.select("#top_chart");
		top_menu.append("div")
			.attr("id","tab_menu")
			.classed("top_menu",true)
				.append("div")
				.attr("id","scrolling_list");//the list of son of the specified node
		var container = top_menu.append("div")
			.attr("id","mod_menu")
			.classed("mod_menu",true);
		container.append("input")//add the file input
				.classed("mod_el",true)
				.attr("type","file")
				.attr("id","import_f")
				.property("multiple",true)
				.on("change",loadData);
		container.append("div")//add the export button
				.attr("id","export")
				.classed("mod_el",true)
				.classed("mod_div",true)
				.on("click",exportFile)
				.html("Export")
				.classed("unselectable",true);
	}
	function exportFile(){
		
	}
	function updateTopList(){
		var hlist = d3.select("#scrolling_list");
		hlist.selectAll("*").remove();
		var layout = graph_obj.getGraphs();
		if(layout.length>1){ layout.splice(layout.indexOf("_ALL"),1);
		var slt = hlist.selectAll(".tab_menu_el").data(layout);
		slt.exit().remove();
		slt.enter().append("div")
			.classed("tab_menu_el",true)
			.classed("unselectable",true)
			.attr("id",function(d){return d})
			.on("click",function(d){return graphChange(d)})
			.text(function(d){
				return d.length>14?d.substring(0,12).concat("..."):d;
			});
		}		
	}
	/* color in blue the currently selected node of the scrolling tab menu
	 * @input : id : the new selected node
	 * @call : graphUpdate event
	 */
	function graphChange(id){
		if(graph_obj.getCurrentGraph()==id) return;
		if(id) graph_obj.chGraph(id);
		d3.select("#scrolling_list").selectAll(".tab_menu_el")
			.style("color","rgb(251, 249, 200)")//show the correct menu element
			.style("background",function(d){
				return d==graph_obj.getCurrentGraph()?"linear-gradient(to bottom, #3fa4f0 0%, #0f71ba 100%)":"none";
			});
		if(!id)
			updateGraphLayout(graph_obj.getDefaultLayout());
		else
			updateGraphLayout();
	}
	function initSideMenu(){

	}
	function updateGraphLayout(lyt){
		var graph = graph_obj.getMiniGraph();//get the minified graph.
		//console.log(graph);
		updateDefs(graph.nodes);//add def for images
		updateLayout(lyt);
		update(graph);
		updateFilters();
		updateDepthSlider();
		chLayout();
	}
	function updateLayout(d_lyt){
		var default_l;
		if(d_lyt) default_l = d_lyt;
		else if(d3.select("#lyt_select").size()>0){
			var si = d3.select("#lyt_select").property("selectedIndex"),
				s = d3.select("#lyt_select").selectAll("option").filter(function (d, i) { return i === si }).datum();
			if(s && graph_obj.getCoordList().indexOf(s)!=-1)
				default_l =s;
			else default_l = __forceLayout;
		}else default_l = __forceLayout;
		d3.select("#layout").remove();
		if(!graph_obj.getCoordList() || graph_obj.getCoordList().length==0 ) return;
		var content = d3.select("#side_content"),
			layout = graph_obj.getCoordList(),
			lyt = content.append("div")
					.attr("id","layout")
					.classed("side_div",true);
		lyt.append("html").classed("side_el",true).text("Choose layout");
		let	selector = lyt.append("select")
			.attr("id","lyt_select")
			.classed("side_select",true)
			.on("change",chLayout);
		if(layout.length>0)
			layout=layout.filter(function(e){
				return graph_obj.getBBox(e)!=null;
			});
		layout.unshift(__forceLayout);
		selector.selectAll("option")
			.data(layout)
			.enter()
			.append("option")
				.text(function(d){return d})
				.each(function(d,i){if(d==default_l){d3.select(this).attr("selected",true);}});
	}
	function chLayout(){
		var sl = d3.select("#lyt_select"),
			si,s;
		if(sl.size()>0){
			si = sl.property("selectedIndex");
			s = d3.select("#lyt_select").selectAll("option").filter(function (d, i) { return i === si }).datum();
		}else s=__forceLayout;
		if(simulation.alpha()!=0)
			endForce();
		var nodes = svg_content.selectAll('g.node');
		if(s==__forceLayout){
            d3.selectAll(".simu_button").remove();
            d3.select("#simulation").remove();
            d3.select("#quit_simulation").remove();
            d3.select("#simu_svg").remove();
            d3.selectAll("div1").remove();
            d3.selectAll(".node")
                .attr("opacity",1);
            updateTopList();
			if(nodes.size()<10000){
				var scl = scaleCalc();
				nodes.each(function(d){
					d.fx=null;
					d.fy=null;
					if(d.ox){
						d.x=d.ox*old_scale[4];
						d.y=d.oy*old_scale[4];
					}
				});
				if(old_scale)
					updateScale(old_scale);
				reload_force();	
			}else alert("Too Much node, simulation may crash !!!!");
		}else{
            d3.select("#simulation").remove();
            d3.select("#quit_simulation").remove();
			move(
				function(d){
					var coord = graph_obj.getCoord(d.id,s);
					if(!coord || coord.length==0) coord = [d.x,d.y];
					return coord;
				},function(d){
					var coord =graph_obj.getCoord(d.id,s);
					if(!coord || coord.length==0) return;
					d.fx=coord[0];
					d.fy=coord[1];
					d.x=coord[0];
					d.y=coord[1];
			},updateScale(null,graph_obj.getBBox(s)));

            var content = d3.select("#side_menu");
            content.append("input")
                .attr("id","simulation")
                .classed("side_div",true)
            	.attr("type","button")
				.attr("value","Simulation")
				.on("click",ChSimu);

            content.append("input")
                .attr("id","quit_simulation")
                .classed("side_div",true)
                .attr("type","button")
                .attr("value","Quit Simulation")
                .on("click",chLayout_simu);


		}				
	}
	function chLayout_simu(){
		d3.selectAll(".simu_button").remove();
		d3.select("#simulation").remove();
		d3.select("#quit_simulation").remove();
        d3.select("#simu_svg").remove();
        d3.selectAll("div1").remove();
        d3.selectAll(".node")
            .attr("opacity",1);
        chLayout();
        updateTopList();
	}

	function fileExist(url){
		var img = new Image();
		img.src = url;
		console.log(img);
		return img.height != 0;
	}
	function updateDepthSlider(){
		d3.select("#depth_slide").remove();
		if(graph_obj.getNLevel()<1)return;
		var sld = d3.select("#side_content").append("div")
					.attr("id","depth_slide")
					.classed("side_div",true);
		sld.append("html").classed("side_el",true).text("Nodes level");
		var sld_ct = sld.append("form"),
			slider_div = sld_ct.append("div").classed("sl_rng",true),
			range_div = sld_ct.append("div").classed("sl_rng",true);
		slider_div.append("label").text("level").classed("side_el",true);
		slider_div.append("input")
			.attr("type","range")
			.property("max",graph_obj.getNLevel())
			.property("min",1)
			.property("value",1)
			.attr("id","depth_slider")
			.property("step",1)
			.on("change",depthShow);
		range_div.append("label").text("range").classed("side_el",true);
		range_div.append("input")
			.attr("id","min_depth")
			.attr("type","text")
			.property("value",1)
			.classed("side_in_t",true)
			.on("change",depthShow);
		range_div.append("input")
			.attr("type","text")
			.attr("id","max_depth")
			.classed("side_in_t",true)
			.property("value",graph_obj.getNLevel())
			.on("change",depthShow);
	}
	function depthShow(){
		console.log("triggered");
		var obj = d3.select(this);
		if(obj.attr("id")=="depth_slider"){
			var depth = obj.property("value");
			d3.selectAll(".node").each(function(d){
				if(graph_obj.getDepth(d.id)!=depth-1){
					hideLinkedEdges(d.id,true);
					d3.select(this).style("visibility","hidden");
				}else{
					hideLinkedEdges(d.id,false);
					d3.select(this).style("visibility","visible");
				}
			});
		}
		else{
			var min_depth = d3.select("#min_depth").property("value"),
				max_depth = d3.select("#max_depth").property("value");
				console.log(min_depth,max_depth);
			d3.selectAll(".node").each(function(d){
				if(graph_obj.getDepth(d.id)<=min_depth-1 || graph_obj.getDepth(d.id)>max_depth){
					hideLinkedEdges(d.id,true);
					d3.select(this).style("visibility","hidden");
				}else{
					hideLinkedEdges(d.id,false);
					d3.select(this).style("visibility","visible");
				}
			});
		}
	}
	function updateFilters(){
		//console.log(graph_obj.getFilters());
		d3.select("#filters").remove();
		if(!graph_obj.getFilters()) return;
		var content = d3.select("#side_content"),
			filters = graph_obj.getFilters(),
			flt = content.append("div")
					.attr("id","filters")
					.classed("side_div",true);
		flt.append("html").classed("side_el",true).text("Choose filter");			
		let	selector = flt.append("select")
				.attr("id","flt_select")
				.classed("side_select",true)
				.on("change",showFilters);
		selector.selectAll("option")
			.data(filters)
			.enter()
			.append("option")
				.text(function(d){return d})
				.attr("selected",function(d,i){return i==0});
		showFilters();
	}
	function showFilters(){
			var si = d3.select("#flt_select").property("selectedIndex"),
				sl = d3.select("#flt_select").selectAll("option").filter(function (d, i) { return i === si }).datum(),
				s = graph_obj.getNAttValList(sl);
			if(!s || s.length==0)
				s = graph_obj.getEAttValList(sl);
			s = s.filter(function(e){
					return d3.select("."+e).size()!=0;
				});
			d3.select("#filter_box").remove();
			if(s && s.length>0){
				var frm = d3.select("#filters").append("div").attr("id","filter_box")
					.selectAll("input").data(s).enter().each(function(d){
						var in_div = d3.select(this).append("div")
							.classed("check_div",true)
							.style("width",s.length>10?"48%":"100%")
							.style("float",s.length>10?"left":"none");
						in_div.append("input")
							.attr("type","checkbox")
							.classed("side_check",true)
							.on("change", showFiltered)
							.property("checked",function(d){
								var slt = d3.select("."+d);
								if(!slt || slt.size()==0) return true;
								return slt.style("visibility")=="visible";
							})
							.attr("value",function(d){return d});
						in_div.append("label")
							.text(function(d){return d})
							.classed("side_el",true)
							.style("font-size",s.length>10?"80%":"100%")
					});
			}
		}
	function showFiltered(){
		var chx = d3.select(this),
			st = chx.property("checked"),
			val = chx.attr("value"),
			obj_l = d3.selectAll("."+val);
		obj_l.each(function(d){
			d3.select(this).style("visibility",st?"visible":"hidden");
			if(d.source) d.self_hide=!st;
			else hideLinkedEdges(d.id,!st);
		})
	}
	
	function hideLinkedEdges(n_id,bool){
		d3.selectAll(".link").filter(function(d){
			if(bool){
				return d.source.id==n_id || d.target.id==n_id;
			}else{
				if(d.self_hide)return false;
				if(d.source.id==n_id){
					return d3.selectAll(".node").filter(dd => dd.id==d.target.id).style("visibility")==("visible");
				}else if(d.target.id==n_id){
					return d3.selectAll(".node").filter(dd => dd.id==d.source.id).style("visibility")==("visible");
				}else return false;
			}
		}).style("visibility",function(d){ return (bool || d.self_hide)?"hidden":"visible"});
	}
	function updateDefs(nodes){
		console.log("loading images...");
		//svg.select("defs").selectAll("pattern").remove();
		addPattern("logo.png",-1,null);
		console.log("images loaded");
	}
	var garbage_pattern=[];
	function addPattern(path,selection,el,flag){
		var pattern = svg.select("defs").append("pattern")
			.attr("id","i_"+(el?el.id:"-1"))
			.attr("height","100%")
			.attr("width","100%")
			.attr("x",-node_base_radius)
			.attr("y",-node_base_radius)
			.attr("patternUnits","userSpaceOnUse");
		pattern.append("svg:image")
			.attr("width","100px")
			.attr("height","100px")
			.attr("x", 0)
			.attr("y",0)
			.classed("node_img",true)
			.attr("xlink:href",path)
			.on("error",function(){
				if(!flag){
					pattern.remove();
					addPattern("../../data/"+path.split("/").slice(1).join("/"),selection,el,true);
					return;
				}
				if(el){
					el.img = "i_-1";
					loadImg(selection,"i_-1");
					garbage_pattern.push("#i_"+el.id);
				}
				pattern.remove();
			})
			.on("load",function(){
				if(el){el.img = "i_"+el.id;
				loadImg(selection,"i_"+el.id);}
				});
			
		//return i;
	}
	function clickHandler(){
		
	}
	/* move all nodes and edges according to the force layout
	 */
	function move(f_n,callback,end_cb){
		var nodes = svg_content.selectAll("g.node");
		if(callback) nodes = nodes.transition().on("end",callback).duration(tr_duration);
		nodes.attr("transform", function(d) {
			var coord = f_n?f_n(d):[d.x,d.y],
				nx = coord[0],
				ny = coord[1];
			if(!coord) return;
			return "translate(" + nx + "," + ny + ")"; 
		});
		var links = svg_content.selectAll(".link");
		if(callback) links = links.transition().duration(tr_duration);
			links.attr("d", function(d) {
				var x1 = (f_n?f_n(d.source)[0]:d.source.x),
					y1 = (f_n?f_n(d.source)[1]:d.source.y),
					x2 = (f_n?f_n(d.target)[0]:d.target.x),
					y2 = (f_n?f_n(d.target)[1]:d.target.y),
					dx = x2 - x1,
					dy = y2 - y1,
					dr = Math.sqrt(dx * dx + dy * dy),
					drx = dr,
					dry = dr,
					xRotation = 0,
					largeArc = 0,
					sweep = 1;
					// Self edge.
				if ( x1 === x2 && y1 === y2 ) {
					xRotation = -45;
					largeArc = 1;
					drx = 40;
					dry = 30;
					x2 = x2 + 1;
					y2 = y2 + 1;
				} 
				return "M"+x1+","+y1+"A"+drx+","+dry+" "+xRotation+","+largeArc+","+sweep+" "+x2+","+y2;
			});	
		if(end_cb)
			svg_content.transition().on("end",end_cb).duration(tr_duration+1);
	}
	function simpleMove(n_id,x,y){
		var node = svg_content.select("#"+n_id).attr("transform",function(d){
			d.x=x;d.y=y;
		return "translate(" + x + "," + y + ")"; 
		});
		/*var s_edges = graph_obj.getEBySource(n_id),
			t_edges = graph_obj.getEByTarget(n_id),
			c_edges = graph_obj.getChildren(n_id).map(c => "__e"+c+"_"+n_id).concat(t_edges),
			p_edges = graph_obj.getParents(n_id).map(p => "__e"+n_id+"_"+p).concat(s_edges);
		console.log(s_edges,t_edges,c_edges,p_edges);	*/
		var links = svg_content.selectAll(".link");
			links.attr("d", function(d) {
				var x1 = (d.source.x),
					y1 = (d.source.y),
					x2 = (d.target.x),
					y2 = (d.target.y),
					dx = x2 - x1,
					dy = y2 - y1,
					dr = Math.sqrt(dx * dx + dy * dy),
					drx = dr,
					dry = dr,
					xRotation = 0,
					largeArc = 0,
					sweep = 1;
					// Self edge.
				if ( x1 === x2 && y1 === y2 ) {
					xRotation = -45;
					largeArc = 1;
					drx = 40;
					dry = 30;
					x2 = x2 + 1;
					y2 = y2 + 1;
				} 
				return "M"+x1+","+y1+"A"+drx+","+dry+" "+xRotation+","+largeArc+","+sweep+" "+x2+","+y2;
			});	
	}
	function reload_force(){
		//d3.selectAll(".edge_label").remove();
		if(simulation.nodes().length>0)
			simulation.alpha(1).restart();	
	}
	/* handling dragging event on nodes
	 * @input : d : the node datas
	 */
	function dragged(d) {
		//console.log("here");
		if(d3.event.type!="drag")return;
		d3.select(this).attr("x", d.fx = d3.event.x).attr("y", d.fy = d3.event.y);	
		if(simulation.alpha()==0)
			simpleMove(d.id,d.fx,d.fy);		
	}
	function collaps(){
		//console.log("here");
		if(!d3.event.shiftKey) return;
		var d=d3.select(this).datum();
		if(d.children){
			getNodesToHide(d,true);
			d._children = d.children;
			d.children=null;
		}else if(d._children){
			d.children = d._children;
			d._children=null;
			getNodesToHide(d,false);
		}
		d3.select(this).selectAll("circle").style("stroke-dasharray", function(d) {
					return d._children ? "15, 10, 5, 10" : "none";
				})
				.style("stroke-width", function(d) {
					return d._children ? "5px" : "3px";
				})
	}
	function getNodesToHide(n_d,bool){
		if(n_d.children){
			svg_content.selectAll(".node").filter(function(d){return n_d.children.indexOf(d)!=-1})
				.style("visibility",bool?"hidden":"visible")
				.each(function(ch){
					hideLinkedEdges(ch.id,bool);
					getNodesToHide(ch,bool);
				});
		}
	}
	function rmNode(selection,d){
		svg.select("defs").select("#i_"+d.img).remove();
		selection.remove();
		
	}
	function addNode(selection,d){
		var node_g = selection.append("g");
		node_g.classed("node",true)
			.call(typeCheckN,d)
			//.on("click.handle",function(d){})
			.on("click.collaps",collaps)
			.attr("id",function(d){return d.id})
//NO DRAG NODES in the SVG//.call(d3.drag().on("drag", dragged).filter(function(){ return !d3.event.button && !d3.event.shiftKey}))
			.on("mouseover",function(d){tt_show(d)})
			.on("mouseout",tt_hide)
			.insert("circle")
				.attr("r", node_base_radius)
				.style("stroke-dasharray", function(d) {
					return d._children ? "15, 10, 5, 10" : "none";
				})
				.style("stroke-width", function(d) {
					return d._children ? "5px" : "3px";
				})
				.style("stroke","black");
		if(graph_obj.getNAtt(d.id,"img") && graph_obj.getNAtt(d.id,"img").length>0){
			var path = graph_obj.getDataFolder();
			if(path) path+="/";	
			else{
				var win = window.location,
				pt = win.pathname.split("/");
				pt.splice(-1,1);
				path=pt.join("/")+"../../data/";
			} 
			addPattern(path+graph_obj.getNAtt(d.id,"img")[0],node_g,d);
		}else{			
			node_g.insert("text")
				.classed("nodeLabel",true)
				.attr("x", 0)
				.attr("dy", ".35em")
				.attr("text-anchor", "middle")
				.text(function(d) {
					var str="";
					if(graph_obj.getNAtt(d.id,"name").length>0)
						str=graph_obj.getNAtt(d.id,"name")[0];
					else str = d.id;
					if(str.length >node_base_radius/7.2)
						str=str.substring(0,8).concat("...");
					return str;
				})
				.attr("font-size", function(){return(node_base_radius/4)+"px"})
				.style("fill","black")
				.style("stroke","black");
		}
	}
	function loadImg(selection,i_id){
		selection.insert("circle")
				.style("fill",function(d){return 'url(#'+i_id+') #fff'})
				.attr("r", node_base_radius)
				.style("stroke","none");
	}
	
	
	function addEdge(selection,d){
		selection.insert("path",":first-child")
			.classed("link",true)
			.classed("hierarchy", function(d){return d._linkType == "hierarchy"})
			.attr("id",function(d){return d.id})
			.attr("marker-mid", function(d){return !graph_obj.edgeExist(d.id) || graph_obj.getDir(d.id)?"url(#arrow_end)":null})
			.call(typeCheckE,d);
	}
	function typeCheckE(selection,d){
		var flt= graph_obj.getFilters();
		if(!flt) return;
		for(var i=flt.length-1;i>=0;i--){
			//console.log(graph_obj.getEAtt(d.id,flt[i]));
			if(graph_obj.getEAtt(d.id,flt[i]).length>0){
				graph_obj.getEAtt(d.id,flt[i]).forEach(function(e){
					selection.classed(e, true);
				});
			}
				
		}
	}
	function typeCheckN(selection,d){
		var flt= graph_obj.getFilters();
		if(!flt) return;
		for(var i=flt.length-1;i>=0;i--){
			//console.log(graph_obj.getNAtt(d.id,flt[i]));
			if(graph_obj.getNAtt(d.id,flt[i]).length>0){
				graph_obj.getNAtt(d.id,flt[i]).forEach(function(e){
					selection.classed(e, true);
				});
			}
				
		}
	}
	/* define a color set according to the size of an array
	 * and the element position in the array
	 * @input : nb : the element index
	 * @input : tot : the size of the array
	 * @input : neg : return the color as negative
	 * @return : a color in hex format
	 */
	function setColor(nb,tot,neg){
		if(neg){
			//calculate color luminosity
			var tmp = ((0xFFFFFF/tot)*(nb+1)).toString(16).split(".")[0];
			var ret =(parseInt(tmp[0]+tmp[1],16)*299+parseInt(tmp[2]+tmp[3],16)*587+parseInt(tmp[4]+tmp[5],16)*114)/1000;
			//if brigth : return black, else return white
			if(ret <150) return (0xFFFFFF).toString(16);
			else return (0x000000).toString(16);
		}
		return "#"+(((0xFFFFFF/tot)*(nb+1)).toString(16).split(".")[0]);
	}
	function scaleCalc(bnd){
		if(!graph_obj) return;
		//console.log("here",bnd);
		var bound =bnd?bnd:svg_content.node().getBBox();
		//console.log(bnd);
        var xrate = svg.attr("width") / (bound.width);
		var yrate = svg.attr("height") / (bound.height);
		var xorigine = bound.x;
		var yorigine = bound.y;
		var rate = Math.min(xrate, yrate);
		//rate = Math.max(rate, 0.02);
		//rate = Math.min(1.1, rate);
		//rate *= 0.9;
		var centerX = (svg.attr("width") - (bound.width) * rate) / 2;
		var centerY = (svg.attr("height") - (bound.height) * rate) / 2;
		return [xorigine,yorigine,centerX,centerY,rate];
	}
	function updateScale(sc,bbox){
		//console.log("rescale0",sc,bbox);
		var scl = sc?sc:scaleCalc(bbox);
		//console.log("rescale",scl);
		if(!scl)return;
		let	xorigine = scl[0],
			yorigine = scl[1],
			centerX = scl[2],
			centerY = scl[3],
			rate = scl[4];
		var upd = svg;
		upd=upd.transition().duration(tr_duration);
		upd.call(zoom.transform, transform.translate(-xorigine * rate + centerX, -yorigine * rate + centerY).scale(rate));
	}

    function ChSimu(){
        Simu.TSNE_simulation(json);
    }

	this.loadData = loadData;
	function loadData(fl){
		console.log("loading");
		var file=document.getElementById("import_f").files;
		if(typeof(file)=="undefined" || file == null || file.length==0) return;
		var file_reader = new FileReader();
		file_reader.onloadend = function(e){
            //json = JSON.parse(e.target.result);
			d3.text(e.target.result,function(g){json=JSON.parse(g)});
			d3.json(e.target.result,function(err,g){
				if(err) return console.error(err);
				if(svg_content.selectAll("*").size()>0){
					svg_content.selectAll("*").remove();
					svg.select("defs").selectAll("pattern").remove();
				}

				graph_obj = new CGraph(g);
				//graph_obj.log();
				updateTopList();
				graphChange();
			});
		};
        //file_reader.readAsText(file.item(0));
		if(!fl)
			for(var i=file.length-1;i>=0;i--)
				file_reader.readAsDataURL(file[i]);
		else file_reader.readAsDataURL(fl);
	}

	function update(graph) {
		simulation.stop();
	// Assigns the x and y position for the nodes
	// Compute the new tree layout.
	//svg_content.selectAll("g.node").remove();
		graph.hie.forEach(function(e){e["_linkType"]="hierarchy"});
		var nodes=graph.nodes,
			links=graph.hie.concat(graph.edges);
  
	// ****************** Nodes section ***************************

	// Update the nodes...
  
		var node = svg_content.selectAll(".node")
			.data(nodes, function(d) {return d.id });
		node.style("visibility","visible");
		node.exit().each(function(d){d3.select(this).call(rmNode,d)});
		node.enter()
			.each(function(d){d3.select(this).call(addNode,d)});
	  
	// ****************** links section ***************************

	// Update the links...
		var link = svg_content.selectAll(".link")
			.data(links, function(d) { return d.id; });
		link.style("visibility","visible");
		//console.log(link);
		link.exit().remove();
		link.enter().each(function(d){d3.select(this).call(addEdge,d)});
		simulation.nodes(svg_content.selectAll('g.node').data());
		simulation.force("link").links(svg_content.selectAll(".link").data());
		simulation.stop().alpha(0);
	}
	
	
}});

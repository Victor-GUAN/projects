define([
	"CompressedGraph.js",
	"d3.js"
],function(OpGraph,d3){
	(function init(){
		
		/*graph.log();
		graph.addGraph("test");
		let n1=graph.addNode(),
			n2=graph.addNode(),
			e1=graph.addEdge(n1,n2);
		graph.log();*/
		d3.select("body").append("input")
			.attr("type","file")
			.attr("id","import_f")
			.on("change",loadData);
	}());
	
	
	
	function loadData(){
		console.log("loading");
		var file=document.getElementById("import_f").files;
		if(typeof(file)=="undefined" || file == null || file.length==0) return;
		var file_reader = new FileReader();
		file_reader.onloadend = function(e){
			d3.json(e.target.result,function(err,g){
				if(err) return console.error(err);
				let graph = new OpGraph(g);
				graph.log();
			});
		};
		file_reader.readAsDataURL(file[0]);

	}
});